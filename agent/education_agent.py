"""
Vegan Education Agent — reviews content and corrects misrepresentations of veganism.
"""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    Docx2txtLoader,
)

INSTRUCTIONS_PATH = Path(__file__).parent.parent / "AGENT_INSTRUCTIONS.md"
INPUT_DIR = Path(__file__).parent.parent / "input"
OUTPUT_DIR = Path(__file__).parent.parent / "output"


def load_instructions() -> str:
    return INSTRUCTIONS_PATH.read_text()


def load_content_file(path: Path) -> str:
    """Load text from .txt, .md, .pdf, or .docx files."""
    suffix = path.suffix.lower()
    if suffix in (".txt", ".md"):
        return path.read_text()
    elif suffix == ".pdf":
        loader = UnstructuredPDFLoader(str(path))
        docs = loader.load()
        return "\n\n".join(d.page_content for d in docs)
    elif suffix == ".docx":
        loader = Docx2txtLoader(str(path))
        docs = loader.load()
        return "\n\n".join(d.page_content for d in docs)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def review_content(content: str, model: str = "gpt-4o") -> str:
    """Send content to the agent for review and return corrected output."""
    llm = ChatOpenAI(model=model, temperature=0)

    messages = [
        SystemMessage(content=load_instructions()),
        HumanMessage(content=f"Please review the following content:\n\n---\n\n{content}"),
    ]

    response = llm.invoke(messages)
    return response.content


def process_file(input_path: Path) -> Path:
    """Review a file and write the result to the output directory."""
    content = load_content_file(input_path)
    result = review_content(content)

    output_path = OUTPUT_DIR / (input_path.stem + "_reviewed.md")
    output_path.write_text(result)
    print(f"Reviewed: {input_path.name} -> {output_path.name}")
    return output_path


def process_all_inputs():
    """Process every supported file in the input/ directory."""
    supported = {".txt", ".md", ".pdf", ".docx"}
    files = [f for f in INPUT_DIR.iterdir() if f.suffix.lower() in supported]

    if not files:
        print("No files found in input/. Drop .txt, .md, .pdf, or .docx files there.")
        return

    for f in files:
        process_file(f)

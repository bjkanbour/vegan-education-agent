"""
Vegan Education Agent — reviews content and corrects misrepresentations of veganism.
"""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredPDFLoader,
    Docx2txtLoader,
)

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"
SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "system_prompt.txt"
INPUT_DIR = Path(__file__).parent.parent / "input"
OUTPUT_DIR = Path(__file__).parent.parent / "output"


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text()


def load_knowledge_base() -> str:
    """Concatenate all knowledge base docs into a single context string."""
    docs = []
    for md_file in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        docs.append(f"## {md_file.stem}\n\n{md_file.read_text()}")
    return "\n\n---\n\n".join(docs)


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

    system_prompt = load_system_prompt()
    knowledge = load_knowledge_base()

    full_system = (
        system_prompt
        + "\n\n## Reference Knowledge Base\n\n"
        + knowledge
    )

    messages = [
        SystemMessage(content=full_system),
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
    print(f"Reviewed: {input_path.name} → {output_path.name}")
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

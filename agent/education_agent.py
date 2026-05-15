"""
Vegan Education Agent — reviews content and corrects misrepresentations of veganism.
"""

from pathlib import Path
import anthropic
import docx2txt
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

INSTRUCTIONS_PATH = Path(__file__).parent.parent / "AGENT_INSTRUCTIONS.md"
KB_DIR = Path(__file__).parent.parent / "knowledge_base"
INPUT_DIR = Path(__file__).parent.parent / "input"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8192

_client: anthropic.Anthropic | None = None
_system_prompt: str | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def _build_system_prompt() -> str:
    instructions = INSTRUCTIONS_PATH.read_text()
    kb_files = sorted(KB_DIR.glob("*.md"))
    sections = [f"### {f.name}\n\n{f.read_text()}" for f in kb_files]
    kb_block = "\n\n---\n\n".join(sections)
    return (
        f"{instructions}\n\n"
        "---\n\n"
        "## Knowledge Base — Full Document Contents\n\n"
        "The following are the complete contents of your knowledge base files. "
        "They are your internal authority. Use them when generating corrections. "
        "Do not cite or reference them explicitly in output.\n\n"
        f"{kb_block}"
    )


def _get_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is None:
        _system_prompt = _build_system_prompt()
    return _system_prompt


def load_content_file(path: Path) -> str:
    """Load text from .txt, .md, .pdf, or .docx files."""
    suffix = path.suffix.lower()
    if suffix in (".txt", ".md"):
        return path.read_text()
    elif suffix == ".pdf":
        doc = fitz.open(str(path))
        return "\n\n".join(page.get_text() for page in doc)
    elif suffix == ".docx":
        return docx2txt.process(str(path))
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def review_content(content: str) -> str:
    """Send content to the agent for review and return corrected output."""
    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=_get_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": f"Please review the following content:\n\n---\n\n{content}",
            }
        ],
    )
    return response.content[0].text


def process_file(input_path: Path) -> Path | None:
    """Review a file and write the result to the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        content = load_content_file(input_path)
    except Exception as e:
        print(f"  Skipped {input_path.name}: could not load ({e})")
        return None

    try:
        result = review_content(content)
    except Exception as e:
        print(f"  Failed  {input_path.name}: API error ({e})")
        return None

    output_path = OUTPUT_DIR / (input_path.stem + "_reviewed.md")
    output_path.write_text(result)
    print(f"  Reviewed {input_path.name} -> {output_path.name}")
    return output_path


def process_all_inputs():
    """Process every supported file in the input/ directory."""
    supported = {".txt", ".md", ".pdf", ".docx"}
    files = sorted(f for f in INPUT_DIR.iterdir() if f.suffix.lower() in supported)

    if not files:
        print("No files found in input/. Drop .txt, .md, .pdf, or .docx files there.")
        return

    processed, skipped = 0, 0
    for f in files:
        if process_file(f) is not None:
            processed += 1
        else:
            skipped += 1

    print(f"\nDone. {processed} reviewed, {skipped} skipped.")

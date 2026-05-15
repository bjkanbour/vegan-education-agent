"""
Vegan Education Agent — reviews content and corrects misrepresentations of veganism.
"""

import logging
import os
from pathlib import Path

import anthropic
import docx2txt
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

INSTRUCTIONS_PATH = Path(__file__).parent.parent / "AGENT_INSTRUCTIONS.md"
KB_DIR = Path(__file__).parent.parent / "knowledge_base"
INPUT_DIR = Path(__file__).parent.parent / "input"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("ANTHROPIC_MAX_TOKENS", "8192"))

_client: anthropic.Anthropic | None = None
_system_prompt: str | None = None

_total_input_tokens = 0
_total_output_tokens = 0


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = anthropic.Anthropic(api_key=api_key, max_retries=3)
    return _client


def _build_system_prompt() -> str:
    """Build the full system prompt from instructions + all KB files."""
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
    """Return the cached system prompt, building it on first call."""
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
    global _total_input_tokens, _total_output_tokens

    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=[
            {
                "type": "text",
                "text": _get_system_prompt(),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Please review the following content:\n\n---\n\n{content}",
            }
        ],
    )

    if response.stop_reason == "max_tokens":
        logger.warning("Response truncated (stop_reason=max_tokens) — output is incomplete.")

    if not response.content or response.content[0].type != "text":
        raise ValueError(
            f"Unexpected API response: stop_reason={response.stop_reason}, "
            f"content={response.content!r}"
        )

    usage = response.usage
    _total_input_tokens += usage.input_tokens
    _total_output_tokens += usage.output_tokens
    logger.info(
        "Tokens — input: %d, output: %d (cache_read: %s, cache_write: %s)",
        usage.input_tokens,
        usage.output_tokens,
        getattr(usage, "cache_read_input_tokens", "n/a"),
        getattr(usage, "cache_creation_input_tokens", "n/a"),
    )

    return response.content[0].text


def process_file(input_path: Path) -> Path | None:
    """Review a file and write the result to the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        content = load_content_file(input_path)
    except Exception as e:
        logger.error("Skipped %s: could not load (%s: %s)", input_path.name, type(e).__name__, e)
        return None

    try:
        result = review_content(content)
    except Exception as e:
        logger.error("Failed %s: API error (%s: %s)", input_path.name, type(e).__name__, e)
        return None

    output_path = OUTPUT_DIR / (input_path.stem + "_reviewed.md")
    output_path.write_text(result)
    logger.info("Reviewed %s -> %s", input_path.name, output_path.name)
    return output_path


def process_all_inputs() -> None:
    """Process every supported file in the input/ directory."""
    global _total_input_tokens, _total_output_tokens
    _total_input_tokens = 0
    _total_output_tokens = 0

    supported = {".txt", ".md", ".pdf", ".docx"}
    files = sorted(f for f in INPUT_DIR.iterdir() if f.suffix.lower() in supported)

    if not files:
        logger.info("No files found in input/. Drop .txt, .md, .pdf, or .docx files there.")
        return

    processed, skipped = 0, 0
    for f in files:
        if process_file(f) is not None:
            processed += 1
        else:
            skipped += 1

    logger.info(
        "Done. %d reviewed, %d skipped. Total tokens — input: %d, output: %d.",
        processed,
        skipped,
        _total_input_tokens,
        _total_output_tokens,
    )

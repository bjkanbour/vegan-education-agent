# Vegan Education Agent

An AI agent that reviews written content and corrects language that misrepresents veganism — restoring it to its accurate definition as an abolitionist movement against animal exploitation.

## What This Agent Does

Veganism is widely misrepresented. Common distortions include framing it as:
- A diet or lifestyle choice
- A harm-reduction or suffering-reduction movement
- An anti-cruelty or kindness/compassion movement
- A general peace or wellness philosophy
- Interchangeable with "plant-based"

This agent reads content and corrects those misrepresentations against the authoritative definition:

> **"The doctrine that man should live without exploiting animals."**
> — Leslie J. Cross & The Vegan Society (1950)

Veganism is a **moral principle** — abolitionist, deontic, and concerned with ending all animal exploitation.

## Supported Input Formats

- `.txt` — plain text
- `.md` — markdown (articles, blog posts)
- `.pdf` — documents
- `.docx` — Word documents

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

## Usage

**Review inline text:**
```bash
python main.py --text "Veganism is a plant-based diet focused on reducing animal suffering."
```

**Review a single file:**
```bash
python main.py --file path/to/article.md
```

**Batch-review all files in `input/`:**
```bash
# Drop .txt / .md / .pdf / .docx files into input/
python main.py
# Reviewed output appears in output/
```

## Output Format

For each piece of content, the agent returns:
1. **Original excerpt** — the problematic phrase
2. **Issue** — what is misrepresented and why
3. **Corrected version** — accurate rewrite
4. **Explanation** — one-sentence distinction
5. **Revised Full Text** — the entire content with all corrections applied

## Knowledge Base

The agent's full knowledge base is loaded into context on every run. All 19 files in `knowledge_base/` are included:

| File | Contents |
|------|----------|
| `1951_veganism_defined_leslie_cross.md` | Cross's original 1951 definition — highest authority |
| `1954_surge_of_freedom_leslie_cross.md` | Cross's extended philosophical account of liberation |
| `what_veganism_is.md` | Authoritative definition and core principles |
| `what_veganism_isnt.md` | Common misrepresentations addressed |
| `CORE_PRINCIPLES.md` | Abolitionist stance, deontic framework |
| `PHILOSOPHICAL_DISTINCTIONS.md` | Veganism vs. welfare, utilitarianism, rights |
| `principled_framework_v1_2.md` | Full principled framework document |
| `vegan_principles_and_philosophy.md` | Philosophical foundations |
| `CORRECTION_STYLE_GUIDE.md` | How to write corrections |
| `approved_prohibited_terminology.md` | Approved and prohibited terms |
| `language_and_messaging_for_liberation.md` | Messaging guidance for liberation framing |
| `role_of_language_in_upholding_oppression.md` | How language normalises exploitation |
| `COMMUNICATION_GUIDELINES.md` | How to frame educational responses |
| `communication_framework.md` | Tone and educational approach |
| `ARGUMENT_RESPONSES.md` | Responses to common counter-arguments |
| `rejecting_utilitarian_vegan_advocacy.md` | Why utilitarian framing undermines the position |
| `ACTIVIST_TRAINING_MODULE.md` | Movement and advocacy framing |
| `VISION_AND_MOVEMENT.md` | Systemic change vision |
| `how_vegan_society_lost_the_plot.md` | History of definitional drift in the movement |

## Source Repository

Knowledge base imported from [vegan-activist-ai](https://github.com/bjkanbour/vegan-activist-ai).

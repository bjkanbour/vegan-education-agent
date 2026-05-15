# Vegan Education Companion

Editorial **companion repository** for rewriting [ADAPTT](https://adaptt.org/aboutadaptt.html) (and similar) content through an **abolitionist, anti-exploitation** lens. This repo holds the **knowledge base** and **unified agent instructions** you attach in Cursor.

**Offline scaffold:** `scripts/adaptt-rewrite-batch.mjs --prepare` emits one **review Markdown stub per migrated shard** under the ADAPTT site (`content/rewrite-reviews/`) so you can log summaries and pasted HTML while you rewrite in Cursor (no keys, no network). See [**docs/RUNBOOK.md**](docs/RUNBOOK.md).

The **ADAPTT** site lives in its own repo (`ADAPTT/site`). Use a sibling clone and symlink **`projects/adaptt/site` → `../../../ADAPTT/site`** from this repo root so the scaffold script resolves the checkout. Ship edits on your dedicated rewrite branch; see [**docs/RUNBOOK.md**](docs/RUNBOOK.md).

## Mental model

| Location | Role |
|----------|------|
| This repo (`vegan-education-agent`) | `AGENT_INSTRUCTIONS.md`, `knowledge_base/`, prompts in `docs/` |
| ADAPTT checkout (elsewhere on disk) | Source pages you edit **in place**; git history ships the work |

Using Cursor together with ADAPTT: open a multi-root workspace with both folders so subagents can edit ADAPTT files while `@` referencing this repo’s instructions and KB.

## Quick start with Cursor

1. Clone ADAPTT and this repo side by side (recommended), for example `~/Projects/ADAPTT` and `~/Projects/vegan-education-agent`.

2. In Cursor: **File → Add Folder to Workspace…** add **both** roots so `@` mentions can pull from companion files while editing ADAPTT.

3. Create a long-lived rewrite branch on ADAPTT (see [**docs/RUNBOOK.md**](docs/RUNBOOK.md)).

4. Open [**docs/SUBAGENT_PROMPTS.md**](docs/SUBAGENT_PROMPTS.md): copy **pass (a)** then **pass (b)** for each page or chunk. Track claims in [**docs/PROGRESS.md**](docs/PROGRESS.md).

5. In every task, `@` attach:

   - `AGENT_INSTRUCTIONS.md`
   - whatever slice of `knowledge_base/` the task needs (for example `@knowledge_base/approved_prohibited_terminology.md`)

For a quick sanity check of tone and structure, see [**docs/EXAMPLE_REWRITE_OUTPUT.md**](docs/EXAMPLE_REWRITE_OUTPUT.md) (synthetic before/after). For a **profane register** sample that keeps blunt language while fixing the lens, see [**docs/EXAMPLE_REWRITE_OUTPUT_VULGAR.md**](docs/EXAMPLE_REWRITE_OUTPUT_VULGAR.md) (strong language).

### Optional project rules

[`.cursor/rules/abolition-editorial.mdc`](.cursor/rules/abolition-editorial.mdc) restates baseline constraints so they stay visible in-session.

## What “good” means

- Veganism framed as **recognition** that no human has the right to exploit other animals (abolitionist, duty-based), not as a diet fad, kindness club, or harm-reduction scoreboard.
- **Exploitation** (ownership, use, breeding for our purposes) named as the structural wrong; **suffering** repositioned as **evidence** of that wrong, not a substitute foundation.
- **Welfare framing** challenged as a category error where it appears: gentle conditions still leave the wrong intact.
- Prose tightened or expanded for **impact** using the editorial principles in `AGENT_INSTRUCTIONS.md`; avoid cosmetic rewrites where the passage is already aligned.

Full doctrine and examples stay in **`AGENT_INSTRUCTIONS.md`** and **`knowledge_base/`**; skim [**docs/RUNBOOK.md**](docs/RUNBOOK.md) for workflow and merge gates.

## Knowledge base

Nineteen reference documents in `knowledge_base/` (founding definitions, philosophy, correction style, terminology, argument patterns, movement context). They are meant to be **referenced**, not pasted into ADAPTT as attributions.

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

Imported from [**vegan-activist-ai**](https://github.com/bjkanbour/vegan-activist-ai).

## Contributing

Improve instructions or KB markdown here when you refine the project line. Prefer small PRs per theme (terminology-only, doctrine clarification, prompts runbook tweak).

# ADAPTT abolitionist rewrite runbook

This companion repo supplies **instructions and a knowledge base**; the editable ADAPTT website lives in its **own** git checkout. Rewrites ship from that repo on a dedicated branch using Cursor agents.

## Prerequisites

- **Companion repo** (this project): defines `AGENT_INSTRUCTIONS.md`, `knowledge_base/`, and prompts under `docs/`.
- **ADAPTT checkout**: sibling clone or separate folder you control upstream for.
- **Cursor**: multi-root workspace recommended (see main `README.md`).

## Workspace layout (recommended default)

Clone ADAPTT and this repo side by side, for example:

- `~/Projects/ADAPTT`
- `~/Projects/vegan-education-agent`

Then add both folders to one Cursor workspace so agents can `@` reference KB files without copying prose into prompts.

Optional later: vendor ADAPTT as a submodule under `external/adaptt` if you prefer a single `git clone` for everything (extra maintenance).

## Branch strategy

1. From `main` (or upstream default branch) on ADAPTT, create a long-lived rewrite branch:

   `abolitionist-rewrite-YYYY-MM` or `abolitionist-rewrite-v2`

2. All agents work on **that same branch** until a merge milestone (section complete, site build green, review done).

3. Prefer **small commits** with clear scope: one page, one section, or one directory per commit when feasible. Put ideological intent in the commit body when helpful (for example “reframe dairy as property relationship,” “close welfare exit in intro”).

4. Merge to ADAPTT’s default branch via your normal PR or maintainer workflow when the milestone is satisfied.

## How to carve work for parallel Cursor subagents

- **Atomic claim**: assign one subagent to **one file** or **one small directory** nobody else is touching. Record the assignment in [`docs/PROGRESS.md`](PROGRESS.md).
- **Do not** run broad “reformat everything” passes in parallel; that causes merge conflicts.
- **Preserve structure** the site depends on: heading hierarchy, anchor IDs, internal links, front matter, component includes, and build-specific markers. Fix links only with a coordinated plan.
- **No drive-by edits** outside the claimed paths unless the agent finds a broken build and the human agrees to expand scope.

## Ordering work

1. **Inventory**: list high-traffic pages and navigation order; decide whether to process top-down (home, entry points) or by theme (dairy, eggs, fish, etc.).
2. **Scout then rewrite**: use [`docs/SUBAGENT_PROMPTS.md`](SUBAGENT_PROMPTS.md) pass (a) then (b) on each chunk.
3. **Consistency pass**: after a batch, run pass (c) on the same paths or the whole branch for terminology alignment with `knowledge_base/approved_prohibited_terminology.md`.

## Quality gates before merge

- **Principle hierarchy** (from `AGENT_INSTRUCTIONS.md`): exploitation and liberation first; accountability; structural over symptomatic; suffering as evidence; practical consequences downstream only.
- **Welfare exit closed** where the page discusses conditions: even gentle conditions do not dissolve the wrong of use and ownership.
- **Avoid** diet-only, identity-only, utilitarian-only, or “plant-based” substitution for veganism as a principle.
- **Em dash**: generated or pasted agent prose should follow the hard constraint in `AGENT_INSTRUCTIONS.md` (no em dash in agent output).
- Run **ADAPTT’s own** build or link checks if the project provides them.
- Spot-read for **tone**: sharp and educational, not merely policed wording.

## Offline review stubs (no API)

With sibling checkouts (for example `~/Projects/vegan-education-agent` and `~/Projects/ADAPTT`), symlink the site into this repo from the companion root:

```bash
mkdir -p projects/adaptt
ln -sf ../../../ADAPTT/site projects/adaptt/site
```

Then **from this repo root**:

```bash
node scripts/adaptt-rewrite-batch.mjs --prepare
# Pilot: append --limit 5
# Other checkout: --site /absolute/path/to/ADAPTT/site
```

This writes **`site/content/rewrite-reviews/<shard>.review.md`** only: metadata plus plaintext extraction of current `contentHtml`, with empty sections for you to fill while editing shards in Cursor (see [`SUBAGENT_PROMPTS.md`](SUBAGENT_PROMPTS.md)). It does **not** call any external service and does **not** modify `content/migrated-pages/`.

## When something is out of scope

- Founding quotations and historical sources: follow `AGENT_INSTRUCTIONS.md` scope rules (quote as written; context, not “correction”).
- Sanctuary or direct rescue narratives: distinguish from baseline non-exploitation as in the instructions.

## Tracking

Maintain [`docs/PROGRESS.md`](PROGRESS.md) so parallel agents do not collide and you can resume after breaks.

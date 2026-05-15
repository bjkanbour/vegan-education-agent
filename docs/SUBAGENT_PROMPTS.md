# Copy-paste prompts for Cursor subagents

Use with a **multi-root** workspace so you can `@` include:

- `AGENT_INSTRUCTIONS.md` (this repo)
- Relevant files from `knowledge_base/` (especially `approved_prohibited_terminology.md`, `CORRECTION_STYLE_GUIDE.md`, `what_veganism_is.md`)

Default mode for ADAPTT: **publish-ready replacement prose in the source file**, not a standalone audit memo, unless the human asks otherwise.

---

## Pass (a): Scout / inventory

Use when you first open a page or folder.

```text
You are revising ADAPTT content for an abolitionist, anti-exploitation lens.

Context:
@AGENT_INSTRUCTIONS.md
@knowledge_base/what_veganism_is.md
@knowledge_base/what_veganism_isnt.md

Task: Read the attached ADAPTT file(s) only. Do not edit yet.

Deliver:
1. A short list of passages that misframe veganism (diet/lifestyle, suffering-only, welfare-as-answer, utilitarian reasoning, identity tourism, consumer framing, etc.), each with the error type name from AGENT_INSTRUCTIONS.
2. Where the piece already lands the structural recognition well; leave those alone per minimum viable edit.
3. Three concrete emotional or narrative upgrades that would increase ideological impact without changing facts the author relies on.

End with “Ready for pass (b)” and nothing else.
```

---

## Pass (b): Rewrite (in place)

Use after pass (a), or alone if the file is small and you already know the issues.

```text
You are rewriting this ADAPTT page in place for abolitionist clarity and greater emotional force.

Context:
@AGENT_INSTRUCTIONS.md
@knowledge_base/CORRECTION_STYLE_GUIDE.md
@knowledge_base/approved_prohibited_terminology.md

Rules:
- Output is the full updated file content (or direct apply edits in the editor), ready to publish. Do not produce an excerpt-only audit unless I ask.
- Preserve site structure: headings, anchors, links, tables, front matter, and any build markers.
- Apply minimum viable edit where the prose is already aligned; deepen impact where it is not.
- Close welfare exits where conditions are discussed: the wrong is the relationship of use, not only bad conditions.
- Land the core recognition in plain language at least once where the piece turns from evidence to obligation.
- When the piece confronts the audience, keep sharp **second-person** accountability (`you`, specific acts of use) and end with a clear **forward summons** (meet the recognition, refuse the next act of use, rise to the demand, organise where relevant), not only abstract diagnosis. Do not sand off direct address into passive analyst voice unless the source genre is already detached.
- Do not use em dashes in any new or rewritten prose (use comma, semicolon, or restructure).

Task: Apply these rules to: [PATH OR PASTE FILE]

After editing, give a 3-bullet summary of what changed ideologically (not typos).
```

---

## Pass (c): Terminology and consistency sweep

Use after a batch of rewrites on a branch.

```text
Consistency pass on abolitionist language.

Context:
@AGENT_INSTRUCTIONS.md
@knowledge_base/approved_prohibited_terminology.md
@knowledge_base/role_of_language_in_upholding_oppression.md

Task: For [PATH OR DIRECTORY], scan for prohibited framing and weak substitutes. Fix with smallest edits that preserve voice. Do not introduce em dashes in new prose.

Deliver:
1. List of files touched
2. For each file, up to five one-line notes on what was normalized (for example “removed plant-based as synonym for veganism,” “shifted purchase framing to act of use”)

If a phrase is acceptable in historical quotation, leave it and note “quoted source unchanged.”
```

---

## Optional: Human-facing review packet

When a maintainer wants an audit without changing files yet:

```text
Same as pass (a), but expand item 1 into a table: excerpt | issue type | suggested rewrite direction (not full rewrite). Do not edit the repository.
```

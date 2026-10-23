---
name: harness2
description: >
  Token-efficient cross-session memory, friction digestion, and harness evolution
  (Harness²) for Antigravity. Use when asked to "/harness2", "reflect on this session",
  "cache this lesson", "promote this script", or validate/evolve a workspace harness.
---

# Harness² — Token-Efficient Self-Improvement & Memory (`E:\harness2`)

Adapted from Google Research's **Harness²** and redesigned natively around Antigravity's progressive disclosure (`<skills>`) and lifecycle hooks (`~/.gemini/config/hooks.json`).

## 1. Automatic Background Memory (Throttled Hook)

Configured in [`~/.gemini/config/hooks.json`](file:///C:/Users/USER/.gemini/config/hooks.json) and powered by [`E:\harness2\agy_memory.py`](file:///E:/harness2/agy_memory.py):

- **`PreInvocation` (`hook-pre`):**
  - Fires **only** on `invocationNum == 1` (first model call of a user prompt; 0 tokens mid-turn).
  - Deduplicates per `conversationId` (`E:\harness2\library\seen_sessions.json`) so a lesson is injected **at most once per conversation**.
  - Matches prompt keywords against `E:\harness2\library\index.json` and emits at most 2 bullets (**hard cap: 320 chars / ~80 tokens**) as an `ephemeralMessage` that **auto-drops after the turn**.
- **`PostToolUse` (`hook-post`):**
  - **0 prompt tokens.** Whenever a tool call returns an `"error"`, appends a compact record to `E:\harness2\library\friction.jsonl` (capped at 200 lines).

## 2. Cost-Hierarchy Routing (Where Knowledge Belongs)

Never bloat `AGENTS.md` / `GEMINI.md` when a cheaper tier enforces the behavior:

1. **0 Prompt Tokens (Mechanical):** Promote deterministic checks or parsers into `scripts/<name>.py` or `E:\harness2\library\scripts\<name>.py`, or enforce tool guards via `.agents/hooks.json`.
2. **0–80 Transient Tokens (Cue Cache):** Store 1-line `INV` (environment/tooling) and `DOM` (domain) lessons in `E:\harness2\library\index.json` via `record`.
3. **On-Demand Progressive Disclosure (~50 tokens):** Put multi-step domain runbooks in `.agents/skills/<name>/SKILL.md` (with required `name` and `description` frontmatter; **never** duplicate skill trigger lines into `AGENTS.md`).
4. **Always-On Rules (`AGENTS.md` / `GEMINI.md` / `.agents/rules/*.md`):** Capped at 24 KB per file. Never duplicate [`karpathy-guidelines.md`](file:///C:/Users/USER/.gemini/config/rules/karpathy-guidelines.md) or global skills.

## 3. CLI Commands (`E:\harness2\agy_memory.py`)

```powershell
# 1. Digest recent tool failures (or a session transcript.jsonl) in <400 tokens
python E:\harness2\agy_memory.py digest

# 2. Record/promote a deduplicated lesson (+ optional verified Python script)
python E:\harness2\agy_memory.py record --dim INV --domain windows-env --cues "keyword1,keyword2" --lesson "Concise 1-line rule" --evidence "What failed -> what fixed it" --script path\to\helper.py

# 3. Query persistent cue memory manually
python E:\harness2\agy_memory.py recall "keywords"

# 4. Validate a workspace's Antigravity harness & check always-on char delta
python E:\harness2\agy_memory.py validate <workspace_dir> --diff <base_dir>
```

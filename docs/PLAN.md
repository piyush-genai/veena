# docs/PLAN.md — Session 1 Plan
# Scope: 2-week thin-slice sprint + parallel Phase 0 schedule
# Status: AWAITING OWNER APPROVAL — no code until approved
# Last updated: 2026-10-10

---

## Explicit Assumptions and Unknowns

The following values were not provided and are marked UNKNOWN. The plan cannot
be calendar-stamped until Q3 is filled in. Shape of the plan is correct; dates
are placeholders.

| Item | Value | Source |
|---|---|---|
| Owner weekly focused hours | **UNKNOWN** — fill in before next session | Q3 blank |
| Veena role (primary vs side project) | **UNKNOWN** — fill in before next session | Q3 blank |
| Income situation / hard deadlines | **UNKNOWN** — ask next session | Q3 blank |
| Active goals (2-3, with deadlines) | **UNKNOWN** — Tier 0 seed will be sparse | Q4 blank |
| Active projects besides Veena | **UNKNOWN** — Astra mentioned but status unconfirmed | Q4 partial |
| Tier 1 model (Phase 1) | LLaMA 3.1 8B **placeholder** — ADR-001 not finalized | Q5 decision |

**Rule:** any UNKNOWN item that affects behavior is marked in Tier 0 as a
`(Preference)-[:UNKNOWN]` node or left as a blank goal/project node. Veena
must not invent values.

---

## Architectural Decisions Locked for This Plan

From Session 1 owner answers (see ADR-006, ADR-007):

- **Parallel execution:** thin-slice sprint and Phase 0 study run concurrently.
  Thin-slice implementation is Claude Code's work; Phase 0 exercises are the
  owner's.
- **Tripwire (hard):** by **2026-11-01**, Ollama + Tier 1 candidate model
  running locally + ECE calibration harness executed against it. If missed,
  all thin-slice feature work freezes until done. Rationale: frontier models
  don't expose logprobs; G3 calibration cannot run without the local model.
- **Inference:** frontier-backed (Claude API) behind a `ModelRouter` interface.
  Local Tier 1 plugs into the same router at the tripwire.
- **Privacy:** Tier 0 context leaves the machine only through `AllowlistFilter`.
  Default allowlist: goals, projects, communication preferences. Everything
  else excluded unless explicitly unlocked.

---

## Thin-Slice Sprint — 2 Weeks

**Target deliverable:** Veena delivers a morning brief every weekday that
reflects the owner's active goals and projects, without being prompted.

**Technology stack for the slice:**
- Tier 0: Neo4j (Docker, local) — schema from ARCHITECTURE.md §2.2, seeded
  with known data and UNKNOWN nodes where data is missing
- Inference: Claude API via `ModelRouter`
- Context: `AllowlistFilter` → Neo4j query → assembled context dict
- Orchestration: LangGraph (single minimal graph)
- Delivery: terminal print (no voice, no notification system yet — Design Law 6)

**Three tools in scope (assumption — confirm or override):**
1. `TimeAwareTool` — current date/time, day of week (needed for morning brief scheduling)
2. `WebFetchTool` — fetch a URL and return clean text (needed for "any updates on X?" queries)
3. `FileTool` — read/append to local plaintext notes file (owner maintains a running notes file; Veena should be able to read it and add to it)

If this tool set is wrong, say so before approving. Adding tools later is cheap; the LangGraph node interface is the same for all of them.

---

### Week 1 — Infrastructure and Data Layer

**Goal:** Neo4j running, schema deployed, seed data loaded, `ModelRouter` +
`AllowlistFilter` implemented and tested in isolation.

#### Milestone 1.1 — Tier 0 Schema and Docker (Days 1–2)
- Neo4j Docker container running with persistent volume
- Schema from ARCHITECTURE.md §2.2 deployed (Cypher constraints and indexes)
- Seed script: creates owner `Person` node, placeholder `Goal` nodes
  (status=UNKNOWN), placeholder `Project` nodes (status=UNKNOWN), and known
  `Preference` nodes (direct, no flattery, lead with risk, recommend one option
  with reasoning, challenge weak ideas)
- Connection test: `python -c "from neo4j import GraphDatabase; ..."` passes
- **Acceptance:** `MATCH (p:Person {name: 'Piyush'}) RETURN p` returns the node

#### Milestone 1.2 — ModelRouter and AllowlistFilter (Days 2–4)
- `ModelRouter` class: thin interface that accepts `(system_prompt, user_prompt,
  context_dict)` and returns `str`. Backend configured via env var
  (`VEENA_BACKEND=claude`). No other logic.
- `AllowlistFilter` class: accepts a raw Tier 0 context dict, returns a filtered
  dict containing only allowlisted keys. Allowlist is a config file, not
  hardcoded. Default: `{goals, projects, communication_preferences}`.
- Unit tests: AllowlistFilter rejects unknown keys; ModelRouter returns a string.
- **Acceptance:** `AllowlistFilter(raw_tier0).filter()` returns a dict with only
  allowed keys; a round-trip through `ModelRouter` with a simple prompt returns
  non-empty text.

#### Milestone 1.3 — Three Tool Nodes (Days 4–6)
- `TimeAwareTool.run()` → `{"date": "2026-10-10", "day": "Saturday", ...}`
- `WebFetchTool.run(url)` → clean text string (requests + BeautifulSoup, no JS)
- `FileTool.read(path)` / `FileTool.append(path, text)` → str / None
- Each tool is a LangGraph-compatible node: `(state: dict) -> dict`
- Unit tests for each tool in isolation.
- **Acceptance:** all three tools pass their unit tests; tools are importable
  from `veena/tools/`.

#### Milestone 1.4 — Tier 0 Query Interface (Days 6–7)
- `Tier0Reader` class implementing:
  - `get_active_goals() -> list[Goal]`
  - `get_active_projects() -> list[Project]`
  - `get_communication_preferences() -> dict[str, str]`
- Returns UNKNOWN-annotated objects where data is missing (not empty lists).
- **Acceptance:** each method returns a typed result (even if all nodes are
  UNKNOWN); Cypher queries match ARCHITECTURE.md §2.4 patterns.

---

### Week 2 — Proactive Engine and Morning Brief

**Goal:** Veena delivers one morning brief autonomously, on schedule, every
weekday.

#### Milestone 2.1 — LangGraph Orchestration Graph (Days 8–9)
- Minimal LangGraph graph:
  ```
  [tier0_reader] → [allowlist_filter] → [tool_runner] → [briefing_gen] → [delivery]
  ```
- `briefing_gen` node: assembles context from Tier 0 (filtered) + TimeAwareTool
  output, sends to `ModelRouter`, returns brief text.
- `delivery` node: prints to terminal with timestamp. No file logging yet —
  Design Law 6.
- **Acceptance:** manually triggering the graph produces a non-empty brief in
  the terminal.

#### Milestone 2.2 — Morning Brief Trigger (Days 9–11)
- Temporal trigger: if current time is between 07:00–09:00 and no brief has
  been delivered today, trigger the graph.
- `brief_delivered_today` state: checked via a local state file
  (`~/.veena/state.json`). Simple key-value, not a database.
- Delivery channel: terminal. If terminal is not open, brief is queued and
  delivered on next terminal open. (Simple: write to `~/.veena/pending_brief.txt`
  and print on next import.)
- **Acceptance:** running `python -m veena.proactive` at 07:30 delivers a brief;
  running it again at 08:00 does NOT deliver a second brief.

#### Milestone 2.3 — Brief Quality Baseline (Days 11–12)
- Owner reviews three consecutive morning briefs against a checklist:
  - [ ] Mentions at least one active goal (or notes UNKNOWN)
  - [ ] Mentions at least one active project (or notes UNKNOWN)
  - [ ] Does not invent facts not in Tier 0
  - [ ] Tone matches communication preferences (direct, risk-first)
  - [ ] Under 300 words
- This is a manual qualitative review, not an automated test. Its purpose is
  to establish a quality baseline before the brief becomes habitual.
- **Acceptance:** all five checklist items pass on at least 2 of 3 briefs.

#### Milestone 2.4 — Week 2 Integration and Smoke Tests (Days 13–14)
- End-to-end test: fresh Docker container, run seed script, run proactive
  engine, verify brief is generated.
- Tier 0 fact update test: add a goal manually via a seed script, verify it
  appears in the next brief.
- AllowlistFilter audit: log what Tier 0 keys were sent to the API in each
  brief; verify nothing outside the allowlist appears in the log.
- **Acceptance:** all three tests pass; no excluded Tier 0 key appears in the
  API call log.

---

## Phase 0 Parallel Schedule

**Owner's work. Claude Code does not implement these exercises.**

The schedule below assumes UNKNOWN hours/week. Weeks are relative to the start
of Phase 0 study, not to the thin-slice sprint calendar. Adjust the start dates
once Q3 is filled in.

| Week | Owner Milestones | Gate |
|---|---|---|
| Week 1 | Transformer from scratch (Karpathy videos + Shakespeare training). Write answers to 5 critical questions in `docs/phase0_notes.md`. | Perplexity < 1.6 on validation set |
| Week 2 | **Before running the EWC demo:** blank out `EWC._compute_fisher()` and `EWC.penalty()` in the demo script (see `docs/review_notes.md` Finding #1). Implement both methods from scratch. Then run the 4-λ experiment sweep. Record table and plot. | Numbers recorded; trade-off written in 3 paragraphs |
| Week 3 | QLoRA fine-tune on TinyLlama. Write 50 Q&A pairs manually first. Compare fine-tuned vs base on those 50. | Fine-tuned model on disk; training loss curve saved |
| Week 4 | CL survey (arXiv:2404.16789, Sections 1,3,4,5). Personal 1-page summary. Full environment setup (Ollama, ChromaDB, Neo4j Docker, SageMaker test job). | All environment items green per ROADMAP.md §0.6–0.7 |
| Week 5 | Begin ADR-001 evaluation: run 20 owner-written prompts against candidate 7-9B models under Ollama. Record results. Write ADR-001 with current model set. Begin ADR-002 (ChromaDB vs FAISS). | ADR-001 written with current models; ADR-002 written |
| Week 6 | Exit gate self-audit. Fix any incomplete items. Write `docs/phase1_prep.md`. | All Phase 0 exit gate items TRUE |

**Tripwire checkpoint (blocks thin-slice feature work if missed):**
By **2026-11-01**: Ollama + Tier 1 candidate model running locally + ECE
calibration harness executed. This falls in Week 3-4 of the schedule above.

---

## Thin-Slice Scope Boundary — What Is NOT in This Plan

The following are explicitly out of scope for the 2-week sprint and the parallel
Phase 0 period. They belong to later phases.

| Out of Scope | Belongs To | Reason |
|---|---|---|
| Tier 3 (ChromaDB episodic buffer) | Phase 2 | Requires MemMan; MemMan requires calibration measurement first (G3) |
| MemMan classification | Phase 2 | Requires understanding confidence calibration; that requires local model + logprobs |
| Sleep cycle engine | Phase 3 | Requires Tier 2; Tier 2 requires Tier 1 frozen |
| DPO feedback loop | Phase 3 | Requires correction capture infra + quality gate + manual review |
| Correction capture | Phase 2 | Tier 3 prerequisite |
| Voice / TTS delivery | Phase 5 | Design Law 1: brain before body |
| REST API (FastAPI) | Phase 2+ | No external consumers yet; CLI is sufficient |
| Tier 0 automatic fact extraction | Phase 2 | Requires MemMan; manual Tier 0 updates are sufficient for the thin slice |
| Web UI | Not planned | Terminal is the interface until Phase 3.5 at earliest |
| AWS deployment | Phase 1+ | Local-first until Phase 0 exit gate is green |

---

## Risks Specific to This Plan

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| UNKNOWN Tier 0 data makes morning brief useless | HIGH | The brief is just "your goals are unknown; your projects are unknown" | Fill in Q4 before end of session or at session start — even 2 goals is enough for a useful brief |
| Tripwire missed (local model not running by 2026-11-01) | MEDIUM | G3 calibration blocked; thin-slice feature work freezes | Owner's Phase 0 Weeks 3-4 must prioritize Ollama setup; Claude Code scaffolds the ECE harness in Week 2 of the sprint |
| AllowlistFilter has a bug and leaks sensitive Tier 0 data | LOW | Privacy violation | Audit log on every API call showing exactly what was sent; owner reviews first 10 briefs manually |
| Tool scope wrong (wrong 3 tools chosen) | MEDIUM | Wasted implementation | Owner approves or overrides tool list before coding begins |
| Phase 0 takes longer than 6 weeks (unknown hours) | UNKNOWN | Phase 1 delayed; tripwire threatened | Cannot quantify without Q3 hours; revisit schedule once Q3 is filled |

---

## Owner Approval Gate

**Before any code is written, the owner must confirm:**

1. [ ] Tool selection approved: TimeAwareTool, WebFetchTool, FileTool (or provide overrides)
2. [ ] Q4 minimum viable Tier 0 seed data provided: at least 1 goal, 1 project, preferences already known
3. [ ] Q3 hours and income context provided (affects whether 2-week calendar is realistic)
4. [ ] This plan approved as written (or with specific change requests)

Once all four are checked, implementation begins with Milestone 1.1.

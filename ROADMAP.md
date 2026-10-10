# Project Veena — Master Roadmap
# Version: 0.1 | Current Phase: 0 — Foundations
# Update this file after completing every task. This is the single source of truth for project progress.

---

## Status Legend
- 🔄 IN PROGRESS
- ✅ DONE  
- ⏳ NOT STARTED
- ❌ BLOCKED (add blocker note)
- ⚠️ AT RISK (add risk note)
- 🔁 REVISIT (needs rework)

---

## Current Phase: Phase 0 — Foundations 🔄
**Target completion:** Week 6  
**Hard exit gate:** All Phase 0 items checked before Phase 1 begins. No exceptions.

---

## PHASE 0 — Foundations (Weeks 1–6)

**Mission:** Understand what you are building at a mechanistic level before writing production code. Every hour here saves three hours in Phase 3.

### Conceptual Milestones

#### 0.1 — Transformer from Scratch
- [ ] Watch Karpathy "Let's build GPT from scratch" (YouTube, ~2.5hr)
- [ ] Implement bigram model → positional encoding → single-head attention → multi-head → transformer blocks
- [ ] Train on Shakespeare dataset, get perplexity below 1.5
- [ ] Write in your own words: what exactly are the weights? What does a forward pass compute?
- [ ] Answer in writing: "What happens to old weights when I train on new data?"
- [ ] **Checkpoint:** Can implement attention from scratch without reference materials

#### 0.2 — Catastrophic Forgetting Demonstration
- [ ] Run `phase0_foundations/catastrophic_forgetting_demo.py` WITHOUT --ewc flag
- [ ] Record: peak Task A accuracy, final Task A accuracy, forgetting percentage
- [ ] Run WITH --ewc flag, record same metrics
- [ ] Compare results in a written note (2-3 paragraphs)
- [ ] Experiment: try lambda_ewc values [100, 500, 5000] — what happens to Task B accuracy?
- [ ] Answer in writing: "Why does high lambda hurt Task B? What is the stability-plasticity trade-off?"
- [ ] **Checkpoint:** Numbers recorded. Trade-off understood at a mechanistic level.

#### 0.3 — EWC from Scratch
- [ ] Read: Kirkpatrick et al. 2017 (arXiv 1612.00796) — full paper, ~12 pages
- [ ] Implement EWC yourself (the catastrophic_forgetting_demo.py has a scaffold)
- [ ] Understand: what is the Fisher Information Matrix and why does EWC use it?
- [ ] Understand: where does EWC's quadratic approximation fail?
- [ ] **Checkpoint:** Can explain EWC to someone else, including its limitations

#### 0.4 — QLoRA Fine-Tuning
- [ ] Read: QLoRA paper (Dettmers et al. 2023) — at minimum abstract, Section 2, Section 4
- [ ] Install full HuggingFace stack (see requirements/phase0.txt)
- [ ] Fine-tune TinyLlama (1.1B) — NOT LLaMA 3.1 8B yet — on 500 custom Q&A pairs
  - [ ] Write 50 Q&A pairs manually first (understand your data)
  - [ ] Use datasets library to format the rest
  - [ ] SFTTrainer (TRL) with LoraConfig
  - [ ] Compare fine-tuned vs base model on your 50 manual questions
- [ ] Answer in writing: "Which matrices were modified? What does rank r=16 mean geometrically?"
- [ ] Answer in writing: "How does this map to Tier 1 (frozen) + Tier 2 (LoRA adapters) in Veena?"
- [ ] **Checkpoint:** Fine-tuned model on disk. Training loss curve saved. Can explain LoRA geometrically.

#### 0.5 — Continual Learning Survey
- [ ] Read arXiv 2404.16789 — Sections 1, 3, 4, 5 (skip hardware-specific sections)
- [ ] Write personal 1-page summary: 4 families of CL solutions + when each applies
- [ ] Identify: where does Veena's architecture sit within this taxonomy?
- [ ] Skim: arXiv 2603.09892 (MSSR Framework) — abstract + architecture section only
- [ ] **Checkpoint:** Can place Veena's approach in the CL landscape with citations

---

### Environment Setup

#### 0.6 — Local Development Environment
- [ ] Python 3.11+ virtual environment created
- [ ] `pip install -r requirements/phase0.txt` — zero errors
- [ ] PyTorch installed with CUDA or MPS (verify: `torch.cuda.is_available()`)
- [ ] Ollama installed: `ollama run llama3.1 "Hello"` responds correctly
- [ ] ChromaDB running: test insert + query works
- [ ] Neo4j running locally (Docker): connection test passes
- [ ] Jupyter notebook server running

#### 0.7 — AWS Environment
- [ ] AWS CLI configured with correct IAM profile
- [ ] SageMaker Studio domain created
- [ ] S3 buckets created:
  - [ ] `veena-corpus` — training data
  - [ ] `veena-models` — model checkpoints  
  - [ ] `veena-artifacts` — experiment outputs
  - [ ] `veena-logs` — CloudWatch log exports
- [ ] IAM role: SageMaker execution role with S3 read/write on veena-* buckets
- [ ] Test: run SageMaker training job (any HuggingFace example), retrieve output from S3
- [ ] CloudWatch: basic dashboard created with one custom metric
- [ ] Budget alert: set at $50/month hard limit to prevent surprise bills

---

### Documentation
- [x] `CLAUDE.md` — standing rules created (Session 1, 2026-10-10)
- [x] `AGENTS.md` — standing rules created, identical to CLAUDE.md (Session 1, 2026-10-10)
- [x] `docs/VISION.md` — vision, goals, non-goals from briefing (Session 1, 2026-10-10)
- [x] `docs/decisions/ADR-001.md` — LLaMA 3.1 8B vs Mistral 7B — written, PENDING owner decision
- [x] `docs/decisions/ADR-002.md` — ChromaDB vs FAISS — written, PENDING owner decision
- [x] `docs/decisions/ADR-003.md` — EWC lambda — written, PENDING measurement in Phase 3
- [x] `docs/decisions/ADR-004.md` — Neo4j vs RDFLib — written, PENDING owner decision
- [x] `docs/decisions/ADR-005.md` — DPO quality gate — written, PENDING owner decision
- [x] `docs/decisions/ADR-006.md` — Sequencing: vertical slice vs Phase 0 gate — **ACCEPTED: parallel with tripwire 2026-11-01**
- [x] `docs/decisions/ADR-007.md` — Capability layer — **ACCEPTED: frontier-backed, hybrid-ready, AllowlistFilter required**
- [x] `docs/review_notes.md` — code review of catastrophic_forgetting_demo.py (Session 1, 2026-10-10)
- [x] `docs/PLAN.md` — 2-week thin-slice sprint + parallel Phase 0 schedule — **AWAITING OWNER APPROVAL**
- [ ] `docs/phase0_notes.md` — personal notes from all Phase 0 reading + experiments

---

### Phase 0 Exit Gate
**Do not proceed to Phase 1 until ALL of these are TRUE:**

| Gate | Status |
|---|---|
| Can implement attention from scratch | ⏳ |
| Catastrophic forgetting numbers recorded and understood | ⏳ |
| EWC implemented and stability-plasticity trade-off documented | ⏳ |
| QLoRA fine-tune completed on TinyLlama | ⏳ |
| CL Survey sections 1,3,4,5 read with personal summary written | ⏳ |
| Ollama + LLaMA 3.1 8B running locally | ⏳ |
| SageMaker end-to-end test passed | ⏳ |
| ChromaDB + Neo4j running locally | ⏳ |
| ADR-001 and ADR-002 written and decided | ⏳ |

---

## PHASE 1 — Frozen Core / Tier 1 (Weeks 7–12) ⏳

**Mission:** Build and freeze Veena-Core v0.1 — a domain-grounded model that will serve as the immutable foundation for everything else.

### 1.1 — Corpus Pipeline
- [ ] Wikipedia EN dump downloaded (use HuggingFace `datasets` library: `load_dataset("wikipedia", "20220301.en")`)
- [ ] Wikipedia cleaning pipeline: remove stubs (< 500 words), remove disambiguation pages, deduplicate
- [ ] Gutenberg books selected (target: 200+ books across science, philosophy, history, technical)
- [ ] Gutenberg cleaning pipeline: remove Project Gutenberg header/footer boilerplate, fix encoding
- [ ] ArXiv papers: cs.LG + cs.AI subset, 2018–2024, PDF → text pipeline
- [ ] Domain manuals: curated and formatted (define domain scope first)
- [ ] Final corpus: deduplicated, tokenized, pushed to S3 `veena-corpus`
- [ ] Corpus stats documented: total tokens, source breakdown, domain distribution

### 1.2 — SageMaker Training Job
- [ ] Training script: `phase1_frozen_core/training/train_qlora.py` — typed, documented
- [ ] SageMaker job configuration: instance type (g5.2xlarge target), spot instances, checkpoint config
- [ ] Hyperparameter sweep: r ∈ [8, 16, 32], alpha, dropout (use SageMaker HPO)
- [ ] First training run on 10% corpus (sanity check — catch bugs cheaply)
- [ ] Full training run on complete corpus
- [ ] Training loss curve: saved, no instability or divergence
- [ ] Checkpoint: best checkpoint identified and saved to S3 `veena-models`

### 1.3 — Evaluation
- [ ] HellaSwag: score baseline (LLaMA 3.1 8B untuned) vs Veena-Core
- [ ] MMLU: 5 relevant subsets — score baseline vs Veena-Core
- [ ] Custom domain eval: 100 hand-written questions — Veena-Core must perform well
- [ ] Regression check: general knowledge NOT degraded vs baseline (< 2% drop)
- [ ] Qualitative review: 50 manual prompts, rate outputs

### 1.4 — Deployment and Freezing
- [ ] Convert to GGUF format for Ollama
- [ ] Ollama: `veena-core` model running locally and responding correctly
- [ ] FastAPI inference endpoint: `POST /generate` — working, latency benchmarked
- [ ] Tier 1 access layer (`FrozenCoreInterface`) implemented — no write operations
- [ ] SHA-256 checksum of Tier 1 weights recorded and stored (for regression test)
- [ ] **Tier 1 declared FROZEN. Access layer enforced. No further weight updates.**

### Phase 1 Exit Gate
| Gate | Status |
|---|---|
| Corpus pipeline produces clean, tokenized data in S3 | ⏳ |
| QLoRA training run completes without instability | ⏳ |
| Veena-Core passes evaluation suite (no >2% regression) | ⏳ |
| Model running locally via Ollama | ⏳ |
| Tier 1 access layer enforced | ⏳ |
| Tier 1 weight checksum recorded | ⏳ |

---

## PHASE 2 — Episodic Memory / Tier 3 (Weeks 13–20) ⏳

**Mission:** Veena learns new facts in-session and retains them cross-session, without touching Tier 1.

### 2.1 — ChromaDB Episodic Buffer
- [ ] ChromaDB collection created with hard cap enforcement (50,000 embeddings)
- [ ] Embedding model benchmarked: all-MiniLM-L6-v2 vs alternatives (quality + speed)
- [ ] Overflow prevention: buffer rejects inserts at cap; triggers MemMan eviction review
- [ ] Persistence: buffer survives process restarts (verify explicitly)
- [ ] Buffer stats endpoint: fill %, sample type distribution, oldest sample timestamp

### 2.2 — MemMan (Memory Manager)
- [ ] Hard sample detector: correction events, low-confidence outputs, Tier 0 contradictions
- [ ] Differential sample scorer: novelty via cosine similarity threshold (< 0.7 = novel)
- [ ] Redundancy detector: cosine similarity ≥ 0.85 = redundant candidate
- [ ] Conflict resolution logic: HARD > DIFFERENTIAL > REDUNDANT
- [ ] **MemMan evaluation loop:**
  - [ ] Sample 200 items from buffer
  - [ ] Human-rate 50 random samples: correct classification?
  - [ ] Compute precision/recall per class
  - [ ] Alert if HARD precision < 0.80
- [ ] MemMan stress test: 10,000 samples injected, verify cap not exceeded, verify type distribution

### 2.3 — RAG Pipeline
- [ ] Dual-retrieval: Tier 1 (base knowledge) + Tier 3 (episodic) queried in parallel
- [ ] Context merger: combine retrieved chunks with conflict detection
- [ ] Query router: scoring logic for when Tier 3 overrides Tier 1 (recency + correction events)
- [ ] Tier 0 context injection: personal facts prepended to all generation calls
- [ ] Latency benchmark: p50, p95, p99 measured and documented
- [ ] LangGraph orchestration: full interaction graph with all nodes connected

### 2.4 — Integration Tests
- [ ] Cross-session test: fact in session A → restart → fact retrieved in session B
- [ ] Tier 1 isolation test: verify Tier 1 checksum unchanged after 100 interactions
- [ ] MemMan adversarial test: inject 1000 identical samples → verify all discarded as redundant

### Phase 2 Exit Gate
| Gate | Status |
|---|---|
| Buffer hard cap enforced and tested | ⏳ |
| MemMan eval loop built and baseline recorded | ⏳ |
| Cross-session memory test passes | ⏳ |
| RAG pipeline latency p95 < 3 seconds | ⏳ |
| Tier 1 checksum unchanged after 100 interactions | ⏳ |

---

## PHASE 3 — Sleep Cycles / Tier 2 (Weeks 21–30) ⏳

**Mission:** Corrections become permanent. Knowledge consolidates. Buffer never overflows.

### 3.1 — EWC Integration
- [ ] Avalanche EWCStrategy configured for Tier 2
- [ ] Fisher Information computed on Tier 1 training data (protect foundational knowledge patterns)
- [ ] Lambda tuning: sweep [0.1, 0.4, 1.0, 4.0] — find stability without plasticity collapse
- [ ] Forgetting benchmark: accuracy on Tier 1 eval suite after N sleep cycles

### 3.2 — Sleep Cycle Engine
- [ ] Sleep state machine: ACTIVE → SLEEP_SCHEDULED → SLEEPING → VALIDATING → ACTIVE
- [ ] Sleep triggers: buffer_fill >= 80% OR scheduled_time
- [ ] Buffer lock: no new writes during sleep phase
- [ ] Replay loop: episodic buffer interleaved with consolidated memory samples
- [ ] Weight update: EWC-regularized backward pass on Tier 2
- [ ] Pre-update checkpoint: always snapshot Tier 2 before any update
- [ ] Regression suite: runs automatically after each update
- [ ] Rollback: if regression suite fails, restore Tier 2 checkpoint and alert
- [ ] Buffer clear: atomic, only after validation passes

### 3.3 — Ebbinghaus Replay Scheduler
- [ ] Stability score per sample (float 0.0–1.0)
- [ ] Replay interval: I_min * e^(k * stability) — k tuned empirically
- [ ] Stability update logic: increase after successful replay, decrease after failed recall
- [ ] Promotion to CONSOLIDATED: stability >= 0.95 → remove from scheduler
- [ ] Scheduler state: persists across process restarts and sleep cycles

### 3.4 — DPO Feedback Loop
- [ ] Correction capture: every correction event produces (rejected, preferred) pair
- [ ] Quality gate: manual review of all pairs before DPO training (no automated bypass)
- [ ] DPO training script: TRL DPOTrainer, typed and documented
- [ ] Behavioral regression test: DPO update does not degrade general capability
- [ ] End-to-end test: correction → sleep → wake → verify correction persists across sessions

### 3.5 — Endurance Tests
- [ ] 10-cycle test: 10 sleep cycles, monitor accuracy delta per cycle
- [ ] 30-cycle simulation: verify no monotonic degradation trend
- [ ] Buffer overflow simulation: aggressive sample injection → verify sleep triggers correctly
- [ ] Scheduler edge case: 1000+ fully consolidated samples → verify scheduler handles gracefully

### Phase 3 Exit Gate
| Gate | Status |
|---|---|
| Full sleep cycle runs end-to-end without manual intervention | ⏳ |
| Regression suite auto-runs and rolls back on failure | ⏳ |
| DPO correction persists after sleep cycle (verified) | ⏳ |
| 30-cycle endurance test shows no monotonic degradation | ⏳ |
| Tier 1 checksum still unchanged | ⏳ |

---

## PHASE 3.5 — Proactive Engine (Weeks 28–33) ⏳

**Mission:** Veena initiates. This is what makes it TRISS, not a chatbot.

### 3.5.1 — Tier 0 Initial Build
- [ ] Neo4j schema deployed (from ARCHITECTURE.md Section 2.2)
- [ ] Initial Tier 0 populated: Piyush's current goals, active projects, key preferences
- [ ] Tier 0 updater: LangGraph node that writes new personal facts on every interaction
- [ ] Tier 0 query interface: `get_active_goals()`, `get_project_status()`, `get_behavioral_patterns()`

### 3.5.2 — Proactive Engine
- [ ] Background LangGraph graph: state_reader → trigger_evaluator → briefing_gen → delivery
- [ ] Trigger registry: TEMPORAL, THRESHOLD, GOAL_DRIFT, INACTIVITY, PATTERN_MATCH
- [ ] Morning brief: every weekday, Veena delivers active goals + project status + flags
- [ ] Inactivity trigger: no project activity for 3+ days → flag
- [ ] Goal drift trigger: trajectory vs target mismatch → flag
- [ ] Proactive engine runs without blocking Active Phase interactions

### Phase 3.5 Exit Gate
| Gate | Status |
|---|---|
| Tier 0 populated and queryable | ⏳ |
| Morning brief delivered automatically (no prompt) | ⏳ |
| At least 3 trigger types working in production | ⏳ |

---

## PHASE 4 — Neuro-Symbolic Layer (Weeks 34–48) ⏳

**Mission:** Surgical fact updates. Multi-step task reliability. HippoRAG 2 memory upgrade.

### 4.1 — Neo4j Full Integration
- [ ] Production Neo4j instance (Docker, persistent volume)
- [ ] Entity extraction pipeline: interactions → named entities → graph nodes
- [ ] Relationship extraction: interactions → relationships → graph edges
- [ ] Conflict resolution: new fact contradicts existing → resolution strategy
- [ ] LangGraph KG query node: parallel to Tier 1 + Tier 3 retrieval

### 4.2 — HippoRAG 2
- [ ] Replace raw ChromaDB with HippoRAG 2 graph-based memory
- [ ] Node decay: older nodes decay in retrieval weight on exponential schedule
- [ ] Concept linkage: related concepts linked at insert time
- [ ] Benchmark: HippoRAG 2 vs raw ChromaDB on multi-hop retrieval queries

### 4.3 — Neuro-Symbolic Imitation Learning (arXiv 2503.21406)
- [ ] Implement NS imitation learning pipeline
- [ ] Multi-step task evaluation suite (50 tasks)
- [ ] Target: ≥75% success rate on multi-step tasks
- [ ] Baseline comparison: same tasks with pure neural → document improvement

### Phase 4 Exit Gate
| Gate | Status |
|---|---|
| KG fact update does NOT require retraining | ⏳ |
| Multi-step task success ≥ 75% | ⏳ |
| HippoRAG 2 multi-hop retrieval outperforms raw ChromaDB | ⏳ |

---

## PHASE 5 — Embodiment (Future) 🔮

Not planned until Phase 4 is stable for 90+ consecutive days.

- Hardware selection (Jetson Orin NX / Raspberry Pi 5 cluster / custom)
- STT: Whisper (local)
- TTS: Coqui XTTS or Piper
- Vision: camera + CLIP or LLaVA integration
- Sensorimotor feedback loop
- Physical deployment chassis
- Ambient presence mode (always-listening, low-power)

---

## Architecture Decision Records

| ID | Decision | Status | File |
|---|---|---|---|
| ADR-001 | LLaMA 3.1 8B vs Mistral 7B | ⏳ Pending | docs/decisions/ADR-001.md |
| ADR-002 | ChromaDB vs FAISS | ⏳ Pending | docs/decisions/ADR-002.md |
| ADR-003 | EWC lambda initial value | ⏳ Pending | docs/decisions/ADR-003.md |
| ADR-004 | Neo4j vs RDFLib (Tier 0 proto) | ⏳ Pending | docs/decisions/ADR-004.md |
| ADR-005 | DPO quality gate threshold | ⏳ Pending | docs/decisions/ADR-005.md |
| ADR-D01 | DPO vs PPO | ✅ Decided: DPO | docs/decisions/ADR-D01.md |
| ADR-D02 | Local vs cloud inference primary | ✅ Decided: Local | docs/decisions/ADR-D02.md |

---

## Risk Register

| Risk | Severity | Phase | Mitigation | Status |
|---|---|---|---|---|
| Adaptive SVD instability at 8B | HIGH | Phase 3 | EWC primary; SVD secondary; monitor Fisher norms | Watching |
| MemMan silent degradation | HIGH | Phase 2+ | Dedicated eval loop with weekly human review | Watching |
| HippoRAG 2 research-grade maturity | MEDIUM | Phase 4 | +2 week buffer; implement adapter layer | Watching |
| Sleep cycle timing wrong | MEDIUM | Phase 3 | Empirical tuning; endurance tests; rollback | Watching |
| DPO pair quality → corruption | HIGH | Phase 3 | Manual quality gate on 100% of pairs | Watching |
| AWS cost overrun | MEDIUM | Phase 1 | Spot instances; $50/month budget alert | Active |
| Tier 0 schema rigidity | MEDIUM | Phase 3.5 | Design for extensibility from first schema version | Watching |
| Phase 0 skipped or rushed | HIGH | Phase 0 | Exit gate enforced — no Phase 1 start without all gates green | Active |

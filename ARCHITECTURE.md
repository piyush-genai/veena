# Project Veena — Architecture Specification
# Version: 0.1 | Status: Living Document | Phase: 0

---

## Document Purpose

This is the authoritative technical specification for Veena's cognitive architecture.
It is a living document — updated as design decisions are made and validated.
Every component, interface, and data flow is described here.
When this document conflicts with a conversation, this document wins.

---

## 1. System Overview

```
╔══════════════════════════════════════════════════════════════════════╗
║                         VEENA COGNITIVE ARCHITECTURE                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ┌─────────────────────────────────────────────────────────────┐    ║
║  │  TIER 0 — PERSONAL IDENTITY GRAPH              [NEO4J]      │    ║
║  │  Piyush's goals · projects · preferences · relationships    │    ║
║  │  Behavioral patterns · correction history · life narrative  │    ║
║  │  Always current · Never consolidated away · Always grows    │    ║
║  └──────────────────────────┬──────────────────────────────────┘    ║
║                             │ personal context                      ║
║  ┌──────────────────────────▼──────────────────────────────────┐    ║
║  │  TIER 1 — FROZEN CORE                    [READ ONLY]        │    ║
║  │  LLaMA 3.1 8B / Mistral 7B — QLoRA fine-tuned              │    ║
║  │  Wikipedia · Gutenberg · Domain manuals                     │    ║
║  │  SACRED — never modified post-deployment                    │    ║
║  └──────────────────────────┬──────────────────────────────────┘    ║
║                             │                                       ║
║  ┌──────────────────────────▼──────────────────────────────────┐    ║
║  │  TIER 2 — CONSOLIDATED SEMANTIC WEIGHTS  [SLEEP ONLY]       │    ║
║  │  EWC-protected weight updates                               │    ║
║  │  Adaptive SVD surgical modification (secondary)             │    ║
║  │  LoRA skill adapters (swappable)                           │    ║
║  └──────────────────────────┬──────────────────────────────────┘    ║
║                             │ consolidation (sleep cycle only)      ║
║  ┌──────────────────────────▼──────────────────────────────────┐    ║
║  │  TIER 3 — EPISODIC BUFFER               [HARD CAP: 50K]    │    ║
║  │  ChromaDB vector store                                      │    ║
║  │  MemMan: hard samples + differential → KEEP                 │    ║
║  │           redundant → DISCARD                               │    ║
║  │  Cleared after each Sleep Cycle                             │    ║
║  └─────────────────────────────────────────────────────────────┘    ║
║                                                                      ║
║  ┌────────────────────────────────────────────────────────────┐     ║
║  │  ORCHESTRATION LAYER                    [LANGGRAPH]        │     ║
║  │  Active Phase agent · Sleep Cycle engine                   │     ║
║  │  Proactive Engine (background, trigger-driven)             │     ║
║  │  Tool nodes: AWS · calendar · code · files · web          │     ║
║  └────────────────────────────────────────────────────────────┘     ║
║                                                                      ║
║  ┌────────────────────────────────────────────────────────────┐     ║
║  │  NEURO-SYMBOLIC LAYER (Phase 4)         [NEO4J + HIPPORAG] │     ║
║  │  Knowledge graph for surgical fact updates                 │     ║
║  │  HippoRAG 2 graph-based episodic memory                   │     ║
║  └────────────────────────────────────────────────────────────┘     ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 2. Tier 0 — Personal Identity Graph

### 2.1 Purpose
Tier 0 is what separates Veena from a powerful general AI. It holds Veena's model of Piyush — his goals, state, preferences, and patterns. Without Tier 0, Veena answers questions. With Tier 0, Veena knows who it's answering for and why.

### 2.2 Graph Schema (Neo4j)

```
NODE TYPES:
  (Person)        — Piyush + people in his life
  (Goal)          — Short/medium/long-term goals
  (Project)       — Active projects with status
  (Preference)    — Communication, technical, behavioral preferences
  (Pattern)       — Behavioral patterns observed over time
  (Correction)    — Every time Piyush corrected Veena
  (Event)         — Significant events (decisions, milestones)
  (Skill)         — Technical and non-technical skills

RELATIONSHIP TYPES:
  (Person)-[:HAS_GOAL {priority, deadline, status}]->(Goal)
  (Goal)-[:REQUIRES]->(Goal)           # goal dependencies
  (Goal)-[:SUPPORTED_BY]->(Project)
  (Person)-[:WORKING_ON {phase, since}]->(Project)
  (Person)-[:PREFERS {strength: 0.0-1.0}]->(Preference)
  (Person)-[:EXHIBITS {frequency, confidence}]->(Pattern)
  (Person)-[:KNOWS {relationship_type}]->(Person)
  (Correction)-[:CORRECTED]->(Person)  # who gave the correction
  (Pattern)-[:DERIVED_FROM {n_observations}]->(Event)
```

### 2.3 Update Protocol
- Tier 0 is updated **surgically** — specific node/edge writes, never full rewrites
- Any new personal fact about Piyush triggers an immediate Tier 0 write
- Behavioral patterns require N_MIN = 5 observations before promotion to Tier 0
- Conflicts (new fact contradicts existing): log both, flag for Piyush to resolve
- Tier 0 is **never** cleared or consolidated — it only grows

### 2.4 Query Patterns
```cypher
-- Get active high-priority goals
MATCH (p:Person {name: "Piyush"})-[r:HAS_GOAL]->(g:Goal)
WHERE g.status = "active" AND r.priority = "high"
RETURN g ORDER BY r.deadline

-- Get recent corrections (for DPO pair generation)
MATCH (c:Correction)-[:CORRECTED]->(p:Person {name: "Piyush"})
WHERE c.timestamp > datetime() - duration("P7D")
RETURN c ORDER BY c.timestamp DESC

-- Get behavioral patterns with high confidence
MATCH (p:Person {name: "Piyush"})-[e:EXHIBITS]->(pat:Pattern)
WHERE e.confidence > 0.7
RETURN pat, e.frequency
```

---

## 3. Tier 1 — Frozen Core

### 3.1 Model Selection: LLaMA 3.1 8B vs Mistral 7B

| Factor | LLaMA 3.1 8B | Mistral 7B |
|---|---|---|
| Context window | 128K tokens | 32K tokens |
| License | Community (Meta) | Apache 2.0 |
| Benchmark performance | Marginally higher | Competitive |
| Long-context tasks | Superior | Adequate |
| GGUF support (Ollama) | ✅ Full | ✅ Full |
| QLoRA fine-tuning | ✅ Well-documented | ✅ Well-documented |
| **Recommendation** | **Primary target** | Fallback if licensing issues |

**Decision pending — document in ADR-001 before Phase 1.**

### 3.2 Training Corpus Plan

| Source | Content | Size (est.) | Processing |
|---|---|---|---|
| Wikipedia (EN) | General world knowledge | ~20GB raw | Filter stubs, deduplicate |
| Project Gutenberg | Literature, technical texts | ~60K books | Clean OCR artifacts |
| ArXiv (cs.LG, cs.AI) | ML/AI research | Selected papers | PDF → text pipeline |
| Domain manuals | Technical reference | TBD | Manual curation |

**Total target corpus:** ~15–25GB clean text (post-processing)

### 3.3 QLoRA Configuration (Starting Point — Tune in Phase 1)

```python
LoRA hyperparameters to sweep:
  r (rank):        [8, 16, 32]       # Start with 16
  lora_alpha:      [16, 32, 64]      # Typically 2x rank
  lora_dropout:    [0.05, 0.1]
  target_modules:  ["q_proj", "v_proj", "k_proj", "o_proj"]
  
Training:
  learning_rate:   2e-4
  batch_size:      4 (with gradient accumulation steps=4 → effective 16)
  epochs:          3
  lr_scheduler:    cosine
  bf16:            True (SageMaker A10G/A100)
```

### 3.4 Evaluation Suite
- **HellaSwag** — commonsense reasoning
- **MMLU** — broad knowledge (select 5 relevant subsets)
- **TruthfulQA** — factual accuracy
- **Custom domain eval** — 100 hand-written prompts from corpus domain
- **Regression baseline:** Must not degrade >2% vs base model on general benchmarks

### 3.5 Tier 1 Access Layer
```python
# Tier 1 is wrapped in a read-only access class
# Direct weight access is prohibited — all reads go through this interface

class FrozenCoreInterface:
    """Read-only access layer for Tier 1. No write operations exist."""
    
    def generate(self, prompt: str, **kwargs) -> str: ...
    def embed(self, text: str) -> list[float]: ...
    def get_logprobs(self, prompt: str) -> dict[str, float]: ...
    
    # These must raise NotImplementedError — they do not exist
    def update_weights(self, *args): raise NotImplementedError("Tier 1 is sacred.")
    def fine_tune(self, *args): raise NotImplementedError("Tier 1 is sacred.")
```

---

## 4. Tier 2 — Consolidated Semantic Weights

### 4.1 EWC — Primary Update Mechanism

**Mathematical basis:**

```
Loss_total(θ) = Loss_new_task(θ) + Σ_i (λ/2) * F_i * (θ_i - θ*_i)²

Where:
  θ          = current parameters
  θ*_i       = optimal parameters after previous task (saved snapshot)
  F_i        = Fisher Information for parameter i
              ≈ E[(∂ log p(y|x,θ) / ∂θ_i)²]
  λ          = EWC regularization strength (tune empirically; start: 0.4)
```

**Fisher Information Interpretation:** F_i measures how much changing weight i changes the model's predictions on previously learned data. High F_i = important weight = heavily protected. Low F_i = unimportant weight = can change freely.

**Implementation:** Avalanche library `EWCStrategy` + custom extensions for LLM-scale Fisher computation.

**Known limitation:** EWC's quadratic approximation breaks down when task distributions are very different. At that point, regularization strength must increase significantly. Monitor loss dynamics.

### 4.2 Adaptive SVD — Secondary Update Mechanism

```
Standard weight update (FFN layers):
  W_new = W_old + ΔW

SVD decomposition of ΔW:
  ΔW = U · Σ · V^T

Low-rank approximation:
  ΔW_approx = U_k · Σ_k · V_k^T   (keep top-k singular values)

Merge:
  W_new = W_old + ΔW_approx
```

**When to use:** When LoRA adapter merging creates rank-mismatch artifacts, or when EWC alone is insufficient for a specific knowledge domain update.

**Risk:** Numerical instability at 8B scale. Always:
1. Check condition number of ΔW before decomposition
2. Validate weight norms before and after merge
3. Run regression suite before accepting update
4. Rollback strategy must exist before every SVD operation

### 4.3 LoRA Skill Adapters

Planned adapters:
| Adapter | Domain | Training Data |
|---|---|---|
| `veena-devops` | AWS, cloud infra, deployment | Technical docs, Piyush's infra logs |
| `veena-research` | ML/AI research, paper reading | ArXiv papers, research notes |
| `veena-personal` | Piyush-specific patterns | Tier 3 consolidated experiences |
| `veena-code` | Python, LangGraph, production code | Piyush's codebase, documentation |

---

## 5. Tier 3 — Episodic Buffer

### 5.1 ChromaDB Configuration

```python
BUFFER_CONFIG = {
    "collection_name": "veena_episodic",
    "hard_cap": 50_000,           # Absolute maximum — never exceeded
    "eviction_threshold": 45_000,  # Trigger MemMan review at 90% capacity
    "embedding_model": "all-MiniLM-L6-v2",  # Benchmark vs alternatives
    "distance_metric": "cosine",
    "persist_directory": "./veena_episodic_db"
}
```

### 5.2 Sample Schema

```python
@dataclass
class EpisodicSample:
    id: str                        # UUID
    timestamp: datetime
    content: str                   # The raw interaction/observation text
    embedding: list[float]         # Pre-computed embedding
    sample_type: SampleType        # HARD | DIFFERENTIAL | REDUNDANT
    memman_confidence: float       # MemMan's confidence in classification (0-1)
    source: str                    # "interaction" | "correction" | "observation"
    correction_data: dict | None   # If source=correction: {rejected, preferred}
    replay_count: int              # Times replayed during sleep cycles
    stability_score: float         # 0.0=new/unstable, 1.0=fully consolidated
    tier0_refs: list[str]          # IDs of Tier 0 nodes this sample references
```

### 5.3 MemMan — Full Specification

**MemMan is the most critical component in the architecture. It runs on every sample insert.**

```
INPUT: New sample (text + embedding + metadata)
OUTPUT: Classification (HARD | DIFFERENTIAL | REDUNDANT) + confidence score

CLASSIFICATION LOGIC:

1. HARD SAMPLE DETECTION (highest priority):
   - Was this a correction event? → HARD (always)
   - Did Veena produce a low-confidence output? → HARD
   - Did Veena's output contradict Tier 0 facts? → HARD
   - Did Veena fail a multi-step task? → HARD
   
2. DIFFERENTIAL SAMPLE DETECTION:
   - Novelty score: max cosine similarity to existing buffer < 0.7 → potential DIFFERENTIAL
   - Knowledge gap score: query Tier 1 on content → if Tier 1 uncertain → DIFFERENTIAL
   - Domain novelty: embedding cluster assignment → if new cluster → DIFFERENTIAL
   
3. REDUNDANCY DETECTION:
   - Max cosine similarity to existing buffer ≥ 0.85 → REDUNDANT (likely)
   - Tier 1 already handles confidently → REDUNDANT
   - Pattern already in Tier 0 with high confidence → REDUNDANT
   
4. CONFLICT RESOLUTION (when signals disagree):
   - HARD signal always wins
   - DIFFERENTIAL wins over REDUNDANT
   - When uncertain: default to DIFFERENTIAL (false positive cost << false negative cost)
```

**MemMan Evaluation Loop (mandatory in Phase 2):**
- Sample 500 items from buffer after each week of operation
- Human-rate 50 randomly selected samples: correct classification or not?
- Compute precision/recall per class
- Alert threshold: precision < 0.80 on HARD class = MemMan failure = stop and fix

---

## 6. Sleep Cycle Engine

### 6.1 State Machine

```
States: ACTIVE | SLEEP_SCHEDULED | SLEEPING | VALIDATING | WAKING

Transitions:
  ACTIVE → SLEEP_SCHEDULED: 
    trigger = (buffer_fill_pct >= 80%) OR (scheduled_time reached)
  
  SLEEP_SCHEDULED → SLEEPING:
    prerequisite = no active interactions
    action = lock buffer (no new writes)
  
  SLEEPING → VALIDATING:
    action = replay → EWC update → run regression suite
    
  VALIDATING → ACTIVE:  (success path)
    prerequisite = regression suite passed (no >2% degradation)
    action = clear buffer, unlock, log cycle metrics
    
  VALIDATING → SLEEPING:  (failure path)
    prerequisite = regression suite failed
    action = rollback Tier 2 to pre-sleep checkpoint, alert Piyush
```

### 6.2 Ebbinghaus Replay Scheduler

```
Stability Function: s(t) = stability_score ∈ [0.0, 1.0]

Replay interval: I(s) = I_min * e^(k * s)
  where:
    I_min = 1 (replay next sleep cycle if s ≈ 0)
    k = 3.0 (controls curve steepness — tune empirically)
    
Stability update after successful replay:
  s_new = s_old + Δs
  Δs = learning_rate * (1 - s_old)  # diminishing returns as s → 1
  
Promotion to permanent:
  if s >= 0.95: mark as CONSOLIDATED, remove from scheduler
  
Degradation on failed retrieval:
  s_new = s_old * 0.7  # penalty for failed recall
```

### 6.3 Sleep Cycle Metrics (CloudWatch)
- `veena.buffer.fill_pct` — current buffer fill percentage
- `veena.sleep.cycle_count` — total sleep cycles completed
- `veena.sleep.duration_seconds` — time per sleep cycle
- `veena.sleep.samples_consolidated` — samples promoted to permanent per cycle
- `veena.tier2.weight_delta_norm` — L2 norm of weight changes per cycle
- `veena.tier2.fisher_norm_mean` — mean Fisher norm (proxy for plasticity health)
- `veena.regression.accuracy_delta` — accuracy change after each update

---

## 7. Proactive Engine

### 7.1 LangGraph Architecture

```
ProactiveEngine (background LangGraph graph):

Nodes:
  [state_reader]     → reads Tier 0 (Piyush's current state)
  [activity_reader]  → reads Tier 3 recent activity
  [trigger_evaluator]→ evaluates all registered triggers
  [briefing_gen]     → generates proactive message if trigger fires
  [delivery]         → delivers via configured channel (terminal / voice / notification)

Edges:
  state_reader → activity_reader → trigger_evaluator
  trigger_evaluator → briefing_gen (if any trigger fires)
  trigger_evaluator → END (if no triggers fire)
  briefing_gen → delivery → END

Schedule: Runs every 30 minutes during Active Phase
```

### 7.2 Trigger Registry

```python
class TriggerType(Enum):
    TEMPORAL = "temporal"           # Time-based (morning brief, EOD summary)
    THRESHOLD = "threshold"         # Buffer %, AWS cost, goal deadline proximity
    ANOMALY = "anomaly"             # Deviation from Piyush's baseline patterns
    GOAL_DRIFT = "goal_drift"       # Trajectory vs target mismatch
    INACTIVITY = "inactivity"       # N days no activity on active project
    PATTERN_MATCH = "pattern_match" # Known behavioral pattern detected
```

---

## 8. Data Flow Diagrams

### 8.1 Active Phase — Single Interaction

```
Piyush input
     │
     ▼
[Query Router]
     │
     ├──→ [Tier 0 Reader] ──→ personal context
     │
     ├──→ [Tier 1 Generator] ──→ base response
     │
     └──→ [Tier 3 RAG] ──→ episodic context
                │
                ▼
         [Context Assembler] ──→ merged context
                │
                ▼
         [Tier 1 Generator with full context]
                │
                ▼
         [Response Quality Evaluator]
                │
                ├──→ [MemMan] ──→ classify and store in Tier 3
                │
                └──→ [Tier 0 Updater] ──→ update personal facts if present
                │
                ▼
         Response to Piyush
```

### 8.2 Correction Flow

```
Piyush: "That's wrong. The correct answer is X."
     │
     ▼
[Correction Detector] ──→ extract (rejected_response, preferred_response)
     │
     ├──→ [Tier 3 Insert] type=HARD, source=correction
     │         correction_data = {rejected, preferred}
     │
     ├──→ [Tier 0 Update] log correction event to correction history
     │
     └──→ [DPO Queue] append (rejected, preferred) pair for next sleep cycle
```

---

## 9. Interface Specifications

### 9.1 REST API (FastAPI — Phase 2+)

```
POST /interact          — main interaction endpoint
POST /correct           — submit correction
POST /feedback          — thumbs up/down
GET  /status            — system health, buffer fill, last sleep cycle
GET  /tier0/summary     — Piyush's current state summary
POST /sleep/trigger     — manually trigger sleep cycle
GET  /sleep/history     — sleep cycle log
GET  /metrics           — all CloudWatch metrics
```

### 9.2 CLI Interface (Phase 2+)

```bash
veena chat              — interactive session
veena correct "..."     — submit correction
veena status            — system health
veena sleep             — trigger sleep cycle manually
veena tier0 show        — dump Tier 0 summary
veena buffer stats      — buffer fill, top samples by type
```

---

## 10. Architecture Decision Records (ADRs)

ADRs live in `docs/decisions/`. Template:

```markdown
# ADR-NNN: [Title]
Date: YYYY-MM-DD
Status: [Proposed | Accepted | Superseded]

## Context
What situation requires a decision?

## Decision
What was decided?

## Rationale
Why was this the right choice? What alternatives were considered?

## Consequences
What does this decision mean for the rest of the architecture?

## Risks
What could go wrong? How is it mitigated?
```

**Pending ADRs (must be resolved before Phase 1 code):**

| ID | Decision | Deadline |
|---|---|---|
| ADR-001 | LLaMA 3.1 8B vs Mistral 7B | Before Phase 1 start |
| ADR-002 | ChromaDB vs FAISS for Tier 3 | Before Phase 2 start |
| ADR-003 | EWC lambda value (initial) | Before Phase 3 start |
| ADR-004 | Neo4j vs RDFLib for Tier 0 (use RDFLib proto → Neo4j prod?) | Before Phase 3.5 start |
| ADR-005 | DPO preference pair quality gate threshold | Before Phase 3 start |

**Decided ADRs:**

| ID | Decision | Outcome |
|---|---|---|
| ADR-D01 | DPO vs PPO for preference learning | DPO — simpler, better suited for solo dev |
| ADR-D02 | Local inference vs cloud-only | Local primary (Ollama), cloud for training |

---

## 11. Testing Strategy

### Unit Tests (all phases)
- Every class and function has a corresponding test
- MemMan classification: unit test each signal independently
- EWC penalty: verify penalty increases when weights deviate from θ*
- Ebbinghaus scheduler: verify interval calculation at stability 0.0, 0.5, 0.95, 1.0

### Integration Tests (Phase 2+)
- Full interaction cycle: input → MemMan → Tier 3 → response
- Sleep cycle: inject 100 samples → run sleep → verify consolidation → verify buffer clear
- Correction loop: inject correction → sleep → verify behavioral change persists

### Endurance Tests (Phase 3+)
- 30-day simulation: 30 sleep cycles, verify no monotonic degradation
- Buffer overflow simulation: fill to 100% → verify sleep triggers before overflow
- DPO corruption test: inject 10 deliberately bad preference pairs → measure behavioral drift

### Regression Suite (runs after every Sleep Cycle)
- HellaSwag subset (500 questions) — must not drop >2%
- Custom domain eval (100 questions) — must not drop >2%
- Tier 1 isolation test — verify Tier 1 weights unchanged via checksum

---

*This document is version-controlled. Update after every significant architectural decision.*
*Last updated: Project initialization*
*Next scheduled review: End of Phase 0*

# Project Veena — Research Papers Guide
# This file tells you what to read, when to read it, and what to extract from each paper.
# Update with your own notes as you read.

---

## Reading Priority System

🔴 **REQUIRED** — Read before the listed phase begins. No exceptions.
🟡 **IMPORTANT** — Read during the listed phase. Directly affects implementation.
🟢 **REFERENCE** — Skim abstract + key sections. Return when specifically relevant.

---

## PHASE 0 — Must Read Before Writing Phase 1 Code

---

### 🔴 [P0-1] Overcoming Catastrophic Forgetting in Neural Networks
**Authors:** Kirkpatrick, Pascanu, Rabinowitz et al. (DeepMind, 2017)
**Where:** arXiv:1612.00796 | https://arxiv.org/abs/1612.00796
**Pages:** ~12 pages
**Read by:** End of Phase 0 Week 3

**Why it matters for Veena:**
EWC is Veena's primary Tier 2 update mechanism. You will implement this from scratch in Phase 0 and use it in production in Phase 3. If you don't understand the Fisher Information Matrix derivation and the quadratic penalty, you cannot tune EWC correctly, and you cannot diagnose failures.

**What to extract:**
- Section 2: The mathematical formulation. Understand every symbol in the loss equation.
- Section 3: The Fisher Information approximation. Why is empirical Fisher used instead of exact?
- Figure 1: The "elastic band" intuition for weight protection.
- Section 4: Experiments on task sequences. What are the failure modes?

**Key question to answer after reading:**
"At what point does the quadratic approximation break down, and how does that manifest in Veena's sleep cycles?"

**Your notes:**
_(fill in as you read)_

---

### 🔴 [P0-2] A Comprehensive Study of Continual Learning Techniques
**Where:** arXiv:2404.16789 | https://arxiv.org/abs/2404.16789
**Read by:** End of Phase 0 Week 4

**Why it matters for Veena:**
This is the map of the entire CL landscape. Without it, you're navigating Phase 3 blind. You need to know where Veena's approach sits, what alternatives exist, and why they weren't chosen.

**Sections to read (others can be skimmed):**
- Section 1: Introduction — the problem definition
- Section 3: CL settings (Task-IL, Class-IL, Domain-IL) — which one is Veena?
- Section 4: Regularization approaches — EWC and variants
- Section 5: Replay approaches — why Veena uses experience replay + regularization combined
- Skip: hardware-specific sections, edge computing sections

**What to extract:**
- The four families of CL solutions and when each is appropriate
- Why regularization alone isn't sufficient for long-lived systems
- Why replay + regularization (Veena's approach) outperforms either alone
- What "forward transfer" and "backward transfer" mean — you'll need these terms in Phase 3

**Your notes:**
_(fill in as you read)_

---

### 🔴 [P0-3] QLoRA: Efficient Finetuning of Quantized LLMs
**Authors:** Dettmers, Pagnoni, Holtzman, Zettlemoyer (2023)
**Where:** arXiv:2305.14314 | https://arxiv.org/abs/2305.14314
**Read by:** End of Phase 0 Week 3

**Why it matters for Veena:**
Tier 1 is built with QLoRA. If you don't understand what QLoRA is doing at the weight level, you can't diagnose training failures, can't interpret loss curves, and can't make intelligent decisions about rank r and alpha.

**What to extract:**
- Section 2: NF4 quantization — what it is and why it preserves more information than INT8
- Section 3: Double quantization — what it adds
- Section 4: Paged optimizers — why this matters for memory
- Figure 1: The overall QLoRA architecture — understand every component
- Table 2-3: Benchmark results — what performance trade-off are you accepting?

**Key question to answer:**
"What exactly is modified during QLoRA training, and what stays frozen? How does this map to Tier 1 (frozen) vs Tier 2 (LoRA) in Veena?"

**Your notes:**
_(fill in as you read)_

---

### 🟡 [P0-4] Complementary Learning Systems and Deep Learning (PNAS 2022)
**Where:** PNAS 2022 — search "complementary learning systems deep learning PNAS 2022"
**Read by:** End of Phase 0 Week 5

**Why it matters for Veena:**
This is the biological justification for Veena's entire three-tier architecture. The hippocampus-neocortex interaction during sleep is the model for Tier 3 (episodic) → Tier 2 (consolidated) consolidation. Reading this will make the sleep cycle design feel inevitable rather than arbitrary.

**What to extract:**
- The two-system model: fast hippocampal binding vs slow neocortical consolidation
- Why sleep (offline replay) is necessary for stable long-term learning
- The role of interleaved replay in preventing interference
- What "systems consolidation" means and how it maps to Veena's sleep cycle

**Your notes:**
_(fill in as you read)_

---

## PHASE 1 — Read During Frozen Core Development

---

### 🟡 [P1-1] MSSR: Memory-Efficient Selective Self-Replay
**Where:** arXiv:2603.09892 | https://arxiv.org/abs/2603.09892
**Read by:** Phase 1 Week 2

**Why it matters for Veena:**
Relevant to the replay strategy in Veena's sleep cycle. MSSR proposes selective replay based on memory uncertainty — this could improve the Ebbinghaus scheduler in Phase 3.

**What to extract:**
- The selective replay criterion — how does it decide what to replay?
- Memory efficiency gains vs naive full replay
- Does it directly integrate with EWC, or is it a standalone approach?

**Your notes:**
_(fill in as you read)_

---

### 🟢 [P1-2] LLaMA: Open and Efficient Foundation Language Models (Meta, 2023)
**Where:** arXiv:2302.13971
**Skim by:** Phase 1 start

**Why:** You're building on this model. Know its architecture, training data, and limitations before you fine-tune it.

**What to extract:**
- Architecture details: attention mechanism, normalization, positional encoding
- Training data composition — what does it already know well vs poorly?
- Known failure modes and biases

---

## PHASE 3 — Read During Sleep Cycle / DPO Development

---

### 🔴 [P3-1] Direct Preference Optimization (DPO)
**Authors:** Rafailov, Sharma, Mitchell et al. (Stanford, 2023)
**Where:** arXiv:2305.18290 | https://arxiv.org/abs/2305.18290
**Read by:** Phase 3 start

**Why it matters for Veena:**
DPO is Veena's feedback learning mechanism. It converts Piyush's corrections into permanent behavioral updates. The original RLHF (PPO) approach requires a separate reward model and is unstable. DPO eliminates both problems. You need to understand why this works mathematically, not just that it works.

**What to extract:**
- Section 3: The DPO objective derivation — understand why this is equivalent to RLHF reward maximization
- Section 4: The practical algorithm — what exactly does a training step look like?
- Section 5: Experiments — what failure modes does DPO have? (Mode collapse, over-optimization)
- The preference data format: (prompt, chosen, rejected) — this is your correction format

**Key question for Veena:**
"What happens to DPO when the preference dataset is small (< 100 pairs)? What's the minimum viable dataset size?"

**Your notes:**
_(fill in as you read)_

---

### 🟡 [P3-2] Gradient Episodic Memory for Continual Learning (GEM)
**Where:** arXiv:1706.08840
**Read by:** Phase 3 Week 2

**Why:** GEM is an alternative to EWC that works by constraining gradient updates rather than penalizing weight changes. Understanding it will help you diagnose situations where EWC is insufficient and you need a stronger guarantee.

---

## PHASE 4 — Read During Neuro-Symbolic Development

---

### 🔴 [P4-1] HippoRAG 2: From RAG to Memory
**Where:** ICML 2025 proceedings — search "HippoRAG 2 ICML 2025"
**Read by:** Phase 4 start

**Why it matters for Veena:**
HippoRAG 2 is the direct replacement for raw ChromaDB in Tier 3. It introduces graph-based episodic memory where concepts are nodes and relationships are edges, with temporal decay of older nodes. This is Phase 4's core episodic memory upgrade.

**What to extract:**
- Graph construction: how are nodes and edges created from text?
- Decay mechanism: how exactly do older nodes decay in retrieval weight?
- Multi-hop retrieval: how does graph traversal improve over flat cosine similarity?
- Integration with LLMs: what's the query interface?
- Known limitations: where does it fail? Under what retrieval conditions?

**Practical concern:** This is research-grade code as of project start. Expect integration effort. Budget 2 extra weeks.

**Your notes:**
_(fill in as you read)_

---

### 🔴 [P4-2] Neuro-Symbolic Imitation Learning
**Where:** arXiv:2503.21406 | https://arxiv.org/abs/2503.21406
**Read by:** Phase 4 Week 2

**Why it matters for Veena:**
This paper reports 95% success on multi-step tasks for neuro-symbolic systems vs 34% for pure neural. That gap is why Veena has a symbolic layer at all. You need to understand how they achieve this to replicate the improvement.

**What to extract:**
- How is the symbolic layer structured? What format are rules/facts stored in?
- How does the neural model query the symbolic layer?
- The imitation learning setup: what kinds of demonstrations are used?
- Where does the combined system still fail?

**Your notes:**
_(fill in as you read)_

---

### 🟡 [P4-3] From Knowledge Graphs to Knowledge Graphs with Neural Networks
**Where:** Search for "neuro-symbolic AI survey 2023" — multiple valid options
**Read by:** Phase 4 Week 1

**Why:** Before integrating Neo4j with the neural stack, understand the general design patterns for neuro-symbolic systems. This is survey-level reading, not implementation-level.

---

## Additional References (Return When Relevant)

| Reference | Topic | When Relevant |
|---|---|---|
| Attention is All You Need (Vaswani 2017) | Transformer architecture | Phase 0 foundations |
| LoRA: Low-Rank Adaptation (Hu et al. 2021) | LoRA adapter mechanics | Phase 0 / Phase 1 |
| Retrieval-Augmented Generation (Lewis 2020) | RAG pipeline design | Phase 2 |
| Constitutional AI (Anthropic 2022) | Behavioral alignment | Phase 3.5+ |
| RT-2 (Google 2023) | Vision-language-action | Phase 5 |
| Whisper (OpenAI 2022) | Speech-to-text | Phase 5 |

---

## Paper Notes Template

Copy this for each paper you finish reading:

```markdown
## [PAPER ID] — Personal Notes

**Date read:** YYYY-MM-DD
**Phase:** N

**Core claim (1 sentence):**

**How it applies to Veena (specific, not vague):**

**What I'm going to implement based on this:**

**Open questions / things I'm unsure about:**

**Things the paper got wrong or where I disagree:**
```

---

*Update this file as you read. The notes column is the most valuable part — not the citations.*

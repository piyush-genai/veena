# Phase 0 — Foundations Execution Guide
# Weeks 1–6 | Current Phase
# This is your day-to-day guide. Not aspirational. Executable.

---

## Why Phase 0 Is Non-Negotiable

You cannot intelligently design a Sleep Cycle if you don't understand what gradient updates do to weights. You cannot tune EWC if you don't understand the Fisher Information Matrix. You cannot build MemMan if you don't understand what makes a sample informative vs redundant.

Phase 0 is not a warmup. It is the technical foundation that either makes Phases 2 and 3 comprehensible or incomprehensible. The exit gate exists to enforce this. It is not negotiable.

Estimated time investment: 4–6 focused hours per day. This is a research project, not a side project.

---

## Week 1 — The Transformer, Mechanistically

### Goal
Implement a transformer from scratch. Not understanding it conceptually — implementing it. Understand what every weight matrix does during forward and backward passes.

### Day-by-Day

**Day 1–2: Karpathy's makemore series**
- Watch: "The spelled-out intro to neural networks and backpropagation" (2h22m)
  https://youtu.be/VMj-3S1tku0
- Implement bigram character-level model in PyTorch
- Run it. Watch the loss go down. Understand what each step is doing.

**Day 3–4: Build the transformer**
- Watch: "Let's build GPT: from scratch, in code, spelled out" (1h56m)  
  https://youtu.be/kCc8FmEb1nY
- Follow along — write every line yourself, don't copy-paste
- Train on Shakespeare. Get coherent (if terrible) text out.
- Target perplexity: below 1.6 on validation set

**Day 5: The critical questions**
Write answers to these in `docs/phase0_notes.md`:
1. What is the shape of the weight matrix in a single attention head? Why that shape?
2. What happens to all those attention weights during a forward pass? Where do they live?
3. What does the backward pass modify? What stays unchanged?
4. When I call `optimizer.step()`, what exactly changes in memory?
5. If I train on new data tomorrow, what will be different about the model? At what level?

**Day 6–7: The forgetting demo**
- Run `phase0_foundations/catastrophic_forgetting_demo.py` without --ewc
- Record the exact numbers: peak Task A accuracy, final Task A accuracy, forgetting %
- Ask yourself: "Why exactly did this happen? Which weights changed? Why did that erase Task A?"
- Write a 3-paragraph explanation in `docs/phase0_notes.md`

---

## Week 2 — Catastrophic Forgetting Deep Dive + EWC

### Goal
Understand the problem and the primary solution at implementation depth.

**Day 1–2: Read the EWC paper**
- arXiv:1612.00796 — all 12 pages
- Read Section 2 twice. Draw the Fisher information formula on paper.
- Answer: what is the Fisher Information Matrix? What does it measure? Why is the diagonal approximation used?

**Day 3–5: Implement EWC from scratch**
The `catastrophic_forgetting_demo.py` has the EWC class with method stubs. Complete them:

```python
def _compute_fisher(self, dataloader: DataLoader) -> None:
    """
    For each parameter θ_i, compute:
    F_i ≈ E[(∂ log p(y|x,θ) / ∂θ_i)²]
    
    Practical steps:
    1. Set model to eval mode
    2. For each batch in dataloader:
       a. Forward pass → get log probabilities
       b. Compute cross-entropy loss
       c. Backward pass → get gradients
       d. Square the gradients and accumulate
    3. Normalize by number of samples
    """
    pass

def penalty(self) -> torch.Tensor:
    """
    Compute: (lambda/2) * Σ_i F_i * (θ_i - θ*_i)²
    
    This adds to the task B loss during training.
    When this term is large, it means θ_i has drifted far from θ*_i
    on a weight that was important for Task A.
    """
    pass
```

**Day 5–6: Experiment systematically**

Run these four experiments. Record ALL numbers in a table:

| λ value | Peak Task A | Final Task A | Forgetting % | Final Task B |
|---|---|---|---|---|
| 0 (no EWC) | | | | |
| 100 | | | | |
| 500 | | | | |
| 5000 | | | | |

Plot all four on the same graph. What pattern do you see?

**Day 7: Write the synthesis**

Answer these in `docs/phase0_notes.md`:
1. What is the stability-plasticity trade-off? Give a concrete example from your experiments.
2. At λ=5000, what's happening to Task B performance? Why?
3. Why does EWC fail eventually on very long task sequences (hint: Fisher matrices accumulate)?
4. How does Veena's Sleep Cycle design address the "accumulating Fisher" problem?

---

## Week 3 — QLoRA Fine-Tuning

### Goal
Fine-tune a small LLM with QLoRA. Understand exactly what changed in the model.

### Setup First

```bash
# If not already done:
pip install -r requirements/phase0.txt

# Verify GPU/MPS
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('MPS:', torch.backends.mps.is_available())"

# Test Ollama
ollama run llama3.1 "What is catastrophic forgetting in neural networks?"
```

### The Fine-Tuning Task

You'll fine-tune TinyLlama (1.1B) on a custom dataset. The model choice is deliberate — LLaMA 3.1 8B is for Phase 1. TinyLlama is for learning.

**Step 1: Write your dataset (Day 1)**

Write 50 Q&A pairs manually. Topic: anything you care about deeply (Veena architecture, DevOps, AWS, doesn't matter). Writing them yourself forces you to think about data quality. Good format:

```json
{"prompt": "What is the difference between EWC and experience replay?", 
 "completion": "EWC adds a regularization penalty to the loss function that prevents important weights from changing too much. Experience replay stores old examples and mixes them into new training batches. EWC operates at the weight level; replay operates at the data level. Veena uses both: EWC during sleep cycles for weight protection, and episodic replay for the sample stream."}
```

**Step 2: Scale with datasets library (Day 2)**

```python
from datasets import Dataset
import json

# Load your 50 manual pairs
with open("phase0_foundations/qlora_data.json") as f:
    data = json.load(f)

dataset = Dataset.from_list(data)
dataset = dataset.train_test_split(test_size=0.1)
```

**Step 3: Fine-tune (Day 2–3)**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer, SFTConfig
import torch

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Should print: trainable params: ~2M || all params: ~1.1B || trainable%: ~0.18%

training_args = SFTConfig(
    output_dir="./phase0_foundations/qlora_output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    bf16=True,
    save_strategy="epoch",
    logging_steps=10,
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    args=training_args,
)

trainer.train()
model.save_pretrained("./phase0_foundations/qlora_adapter")
```

**Step 4: Analyze and compare (Day 4)**

```python
# Load base model and fine-tuned model
# Run all 50 of your manual questions through both
# Rate each response: base model better / fine-tuned better / same
# What did fine-tuning change? What did it not change?
```

**Day 5–7: Answer the key questions**

Write in `docs/phase0_notes.md`:
1. What is `trainable%: ~0.18%`? What is the other 99.82% doing during fine-tuning?
2. If LoRA only modifies q_proj and v_proj, what does that mean for the model's behavior?
3. Veena's Tier 1 is the base model (frozen). Tier 2 uses LoRA adapters. After fine-tuning Tier 2 with a DevOps adapter, can you still use Tier 1's general knowledge? Why?
4. What would happen if you merged the LoRA adapter into the base weights? What would you lose?

---

## Week 4 — Continual Learning Survey + Environment

### Goal
Read the CL survey. Get all infrastructure running.

**Day 1–3: The CL Survey**
arXiv:2404.16789 — read Sections 1, 3, 4, 5 carefully. Others can be skimmed.

After reading, write the 1-page personal summary required by the Phase 0 exit gate:
- 4 families of CL solutions: what are they, when does each apply?
- Where does Veena's architecture sit? What family (or combination)?
- What are the known failure modes of regularization-only approaches (relevant to Phase 3)?

**Day 4–7: Full environment setup**

Follow the setup checklist in ROADMAP.md Section "Phase 0 — Environment Setup".
Do not move on until every item is green. A broken AWS setup will block Phase 1.

Critical: run an actual SageMaker training job, even if it's just the HuggingFace BERT example. You need to know the full job → checkpoint → S3 pipeline works before you run a multi-hour LLaMA training on it.

---

## Week 5 — Integration and ADRs

### Goal
Integrate all Phase 0 knowledge. Make the two pending architecture decisions.

**Day 1–2: Write ADR-001 (LLaMA 3.1 8B vs Mistral 7B)**

Template in ARCHITECTURE.md Section 10. Fill in:
- Context: what factors matter for Tier 1?
- Decision: which model?
- Rationale: why? What convinced you?
- Consequences: what does this decision mean for the rest of Phase 1?
- Risks: what could go wrong?

Key factors to research:
- Context window: LLaMA 3.1 8B has 128K; Mistral 7B has 32K. Does Veena need > 32K at inference time?
- License: LLaMA uses the Meta Community License. Does this affect how you can use/distribute Veena?
- GGUF quality: check Ollama model page — is 4-bit quantization of comparable quality for both?

**Day 3–4: Write ADR-002 (ChromaDB vs FAISS)**

Key factors:
- ChromaDB: built-in persistence, metadata filtering, simpler API, slower at scale
- FAISS: faster similarity search, no built-in persistence (you build it), more control
- At 50,000 embeddings: does the performance difference matter? Benchmark both.
- Which has better integration with LangGraph?

**Day 5–7: Mini integration test**

Build a tiny version of the Active Phase pipeline:
1. Query Tier 1 (Ollama) for a response
2. Store the interaction in ChromaDB (Tier 3)
3. On next query, retrieve relevant past interactions and include in context
4. Verify the retrieved context improves the response

This is not production code. It's a proof of concept that the components talk to each other.

---

## Week 6 — Exit Gate Review + Phase 1 Preparation

### Goal
Verify all exit gate items. Plan Phase 1 first sprint.

**Day 1–2: Exit gate self-audit**

Go through every item in the ROADMAP.md Phase 0 exit gate. For each:
- If checked: write 1 sentence confirming it (don't just checkbox it)
- If not checked: block the rest of the week until it is

**Day 3–4: Phase 1 planning**

Before Phase 1 starts, answer these in `docs/phase1_prep.md`:
1. What is the exact corpus composition? (Wikipedia dump date, Gutenberg book list, domain manual list)
2. What SageMaker instance type? (g5.2xlarge = ~$1.5/hr; g5.12xlarge = ~$5.5/hr — which do you need?)
3. What is the QLoRA rank r you're starting with? Why?
4. What does "domain-specific" mean for Veena? What domain? What manuals?
5. What is your evaluation strategy for Tier 1? Write the 100 evaluation questions now.

**Day 5–7: Buffer**

Use this time to:
- Finish anything not complete from Weeks 1–5
- Re-read your own notes — does it all make sense?
- Run one more full EWC experiment with notes fresh in mind
- Ask Claude any remaining questions before Phase 1 begins

---

## Common Failure Modes in Phase 0

**Failure: Running Avalanche EWC instead of implementing it yourself**
Why it kills you: Phase 3 you will need to debug EWC behavior at the Fisher matrix level. If you've only ever called `EWCStrategy()`, you won't know where to look.
Fix: Implement EWC from scratch first. Then use Avalanche.

**Failure: Skipping the catastrophic forgetting demo**
Why it kills you: You will design Phase 3 decisions based on conceptual intuition instead of observed behavior.
Fix: Run the demo. Record numbers. Plot curves. Save the output.

**Failure: Fine-tuning LLaMA 3.1 8B in Phase 0 instead of TinyLlama**
Why it kills you: 8B debugging is slow and expensive. TinyLlama gives identical conceptual learning.
Fix: Use TinyLlama for everything in Phase 0.

**Failure: Not writing anything down**
Why it kills you: Phase 4 Piyush will not remember what Phase 0 Piyush learned or decided.
Fix: `docs/phase0_notes.md` gets an entry every day. ADRs get written before decisions become code.

**Failure: Moving to Phase 1 before exit gate is green**
Why it kills you: Every hour of Phase 1 spent on something Phase 0 should have taught you costs 3 hours to unlearn.
Fix: The exit gate is not a formality. It exists because every item on it maps to a specific Phase 3 failure mode.

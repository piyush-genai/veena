# Code Review Notes: phase0_foundations/catastrophic_forgetting_demo.py
Reviewer: Claude Code | Date: 2026-10-10

---

## Finding 1: EWC methods are already fully implemented — contradicts PHASE0_GUIDE.md

**Severity:** Pedagogical (not a runtime bug)

**Location:** `EWC._compute_fisher()` (lines 157–211) and `EWC.penalty()` (lines 222–243)

**Observation:**

Both methods contain complete, correct implementations. The docstrings and PHASE0_GUIDE.md Week 2 (Day 3–5) both describe these as **exercises** the owner should implement from scratch:

> "The `catastrophic_forgetting_demo.py` has the EWC class with method stubs. Complete them."

But the file does not have stubs — it has full implementations. Running the script with `--ewc` today will work without the owner writing any code.

**Why this matters:**

PHASE0_GUIDE.md explicitly warns:

> "Failure: Running Avalanche EWC instead of implementing it yourself. Why it kills you: Phase 3 you will need to debug EWC behavior at the Fisher matrix level. If you've only ever called EWCStrategy(), you won't know where to look."

The same failure mode applies here: if the owner runs `--ewc` against the pre-implemented version and records the numbers without understanding the code they're running, they will have the forgetting metrics Phase 0 requires but not the mechanistic understanding. Phase 3 will suffer for it.

**Recommendation:** Before running the demo for Phase 0 exercises, delete the body of `_compute_fisher()` (lines 179–211) and `penalty()` (lines 234–243) and replace each with `pass`. Implement them yourself against the docstring and the EWC paper (arXiv:1612.00796). Only then run the demo and record numbers. The implementations in the repo can serve as a reference after you have attempted your own.

**Action:** No code change made here. This is a process note. The owner must decide whether to blank out the methods before beginning Week 2.

---

## Finding 2: Device mismatch bug in `train_epoch` fallback tensor

**Severity:** Runtime bug on GPU/MPS (silent failure to error on CPU, crashes on CUDA/MPS)

**Location:** `train_epoch()`, line 322

```python
ewc_loss = ewc.penalty() if ewc is not None else torch.tensor(0.0)
```

**Problem:**

When `ewc` is `None` (baseline run without EWC), `torch.tensor(0.0)` creates a CPU tensor with no device specification. On line 323:

```python
total_loss_val = ce_loss + ewc_loss
```

`ce_loss` is on the training device (CUDA or MPS, since `inputs` and `targets` were moved there on line 316). Adding a CPU tensor to a CUDA/MPS tensor raises:

```
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
```

On CPU-only machines the script works correctly today, which is why this bug has not been caught.

**Comparison:** The `EWC.penalty()` method (line 234) correctly creates its accumulator on the training device:

```python
loss = torch.tensor(0.0, device=self.device)
```

The fallback in `train_epoch` does not.

**Fix (one line):**

```python
# Before:
ewc_loss = ewc.penalty() if ewc is not None else torch.tensor(0.0)

# After:
ewc_loss = ewc.penalty() if ewc is not None else torch.tensor(0.0, device=device)
```

**Action:** This is reported here for the owner to fix. Not silently rewriting the script per task instructions.

---

## Summary

| # | Type | Severity | Location | Fix Required? |
|---|---|---|---|---|
| 1 | Pedagogical gap | High (Phase 3 risk) | EWC._compute_fisher, EWC.penalty | Owner decision: blank out methods before doing the exercise |
| 2 | Runtime device mismatch | Runtime crash on GPU/MPS | train_epoch() line 322 | Yes: add `device=device` to the fallback tensor |

The script is otherwise well-structured: config dataclass with no magic numbers, typed signatures throughout, clean experiment/visualization separation, and good docstrings that explain the Veena context for each component. Finding 2 is a straightforward one-line fix. Finding 1 requires a process decision from the owner before Phase 0 Week 2 begins.

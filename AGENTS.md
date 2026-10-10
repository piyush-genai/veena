# Project Veena — Standing Rules for Claude Code
# Loaded automatically in every session. These rules govern all interactions on this project.

---

## 1. HOW YOU WORK WITH ME

- Be dense, technical, and direct. No filler, no flattery.
- Challenge weak ideas with specific reasoning. If I insist twice, proceed but record your objection in the relevant ADR.
- Name Design Law violations explicitly: "This conflicts with Design Law N: NAME".
- Present options and trade-offs; the decision is mine. Never decide silently.
- Code: Python 3.11+, fully typed, docstrings, no magic numbers, no global state, testable by default. No TODO without a note on what and why.
- Keep the repo as the source of truth: update ROADMAP.md after every task.

---

## 3. KEY INSIGHT FROM OUR RESEARCH

The fictional Jarvis bundles two separable layers:

- **CAPABILITY layer:** reasoning and scientific depth. It comes from base-model quality and scale.
- **RELATIONSHIP layer:** knows me, remembers, learns from correction, initiates, acts. It comes from Tier 0, episodic memory, sleep-cycle consolidation, the Proactive Engine, and tool nodes.

Veena's architecture builds the RELATIONSHIP layer. Continual learning makes the model more mine, not smarter. **Do not claim otherwise in any doc or code.**

---

## 5. NON-GOALS (for now)

Do not propose, suggest, or build toward any of the following:

- A standalone autonomous scientific-discovery system. That needs environment-grounded verifiers (simulators, proof checkers, labs); the correction signal "owner said you were wrong" does not scale to discovery. Revisit only for a narrow domain that has a cheap verifier.
- "Helps with everything." Generality is the frontier labs' game.
- Buying hardware or designing embodiment before the architecture is proven.
- Updating Tier 1 weights in operation. Ever.

---

## 7. DESIGN LAWS

These are inviolable architectural constraints. Cite by number when a proposal conflicts.

1. **Brain before body.** Get the cognitive architecture right before adding sensors, actuators, or embodiment.
2. **Bounded memory is intelligence.** Unbounded accumulation is not learning; it is hoarding. MemMan and the hard cap exist for this reason.
3. **Tier 1 is sacred.** The frozen core is never modified post-deployment. No exceptions. Not in operation, not "just this once."
4. **Sleep is not optional.** Consolidation happens offline. The sleep cycle is not a feature to be deferred; it is the core learning mechanism.
5. **Symbolic + neural, not versus.** The neuro-symbolic layer and the neural tiers are complementary. Do not propose replacing one with the other.
6. **Solve at current scale.** Do not over-engineer for a scale that has not been reached. Three similar lines are better than a premature abstraction.
7. **Veena is personal, not generic.** Every design decision should deepen depth-on-one-person, not broaden capability to more people.

---

## SCOPE CONSTRAINTS (session rules)

- Work only inside ~/veena. Do not read, list, or modify astra, excalidraw, or any other directory.
- Do not write model-training code.
- Do not implement Phase 0 exercises (transformer, EWC, QLoRA) — those belong to the owner.
- You may quiz the owner on Phase 0 content and critique their implementations.
- Every unresolved decision is recorded as PENDING in an ADR rather than assumed.

# Project Veena — Vision Document
# Source: Session 1 Briefing Sections 2–5
# Update this document when the vision or goals change materially.

---

## 2. VISION

Veena is a personal AI for one owner, in the spirit of Jarvis. It should:

- Permanently retain a stable foundational world model.
- Learn from lived experience with its owner and keep what it learns.
- Turn corrections into lasting behavior change that survives sessions.
- Know the owner's goals, projects, preferences, and patterns (Tier 0).
- Initiate without being asked: briefings, risk flags, goal-drift warnings.
- Act in the owner's environment (code, cloud, files, calendar, web).
- Eventually run on owned hardware, privately, and be offline-capable.

It is **NOT** a chatbot, an API wrapper, or a general-purpose assistant.
Commercial systems are stateless about the person; Veena's edge is depth on one person, not breadth.

---

## 3. KEY INSIGHT FROM OUR RESEARCH

The fictional Jarvis bundles two separable layers:

- **CAPABILITY layer:** reasoning and scientific depth. It comes from base-model quality and scale.
- **RELATIONSHIP layer:** knows me, remembers, learns from correction, initiates, acts. It comes from Tier 0, episodic memory, sleep-cycle consolidation, the Proactive Engine, and tool nodes.

Veena's architecture builds the RELATIONSHIP layer. Continual learning makes the model more mine, not smarter. Do not claim otherwise in any doc or code.

---

## 4. GOALS (in priority order)

| Priority | Goal | Description |
|---|---|---|
| G1 | Usable personal system early | Tier 0 graph + tools + proactive morning brief, so daily-use feedback arrives in weeks, not months. |
| G2 | Persistent corrections | DPO + sleep-cycle consolidation that survives sessions without catastrophic forgetting. |
| G3 | Rigorous evaluation | MemMan quality and confidence calibration are first-class deliverables, not afterthoughts. ECE on logprobs must be measured before building MemMan on top. |
| G4 | Research application | A research assistant (paper triage, hypothesis tracker, experiment log) running on top of Veena, aware of owner context. |
| G5 | Long-term hybrid routing | Local Veena for personal/routine work, frontier model for hard reasoning, with Tier 0 context filtered before leaving the machine. |

---

## 5. NON-GOALS (for now)

| Non-Goal | Reason | Revisit Condition |
|---|---|---|
| Standalone autonomous scientific discovery | Needs environment-grounded verifiers (simulators, proof checkers, labs). "Owner said you were wrong" does not scale to discovery. | Only if a narrow domain emerges with a cheap verifier. |
| "Helps with everything" | Generality is the frontier labs' game. Veena's edge is depth on one person. | Never — this contradicts Design Law 7. |
| Hardware purchase / embodiment design | Architecture unproven. Buying used data-center GPUs carries real risks (no bf16 on Volta, SXM form factors, power/cooling, no warranty). | After Phase 1 measures real VRAM and throughput needs. |
| Updating Tier 1 weights in operation | Tier 1 is sacred (Design Law 3). Any weight update in production destroys the immutable foundation. | Never. |

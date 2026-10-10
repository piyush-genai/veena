# The Four Target Problems: A Strategist's Deep-Dive

**A correction before we start, because you asked for no sugarcoating:** most of the 100 problems in the original list do *not* cascade from one another. Solving the Riemann Hypothesis does not cure cancer. Solving the origin of life does not give you room-temperature superconductivity. The "everything is connected" read of that document is not accurate, and I'd be lying to you if I let it stand. What *is* true is that there is a real, tight cluster of maybe 6-8 problems that genuinely feed each other — and your instinct to look for leverage points inside that cluster was correct even if the scale of the claim was too broad.

---

## The Four, and Why These Four

| # | Problem | Why it's in the cluster |
|---|---|---|
| 1 | **AI capable of autonomous scientific discovery** | The meta-lever. A real capability gain here compounds into faster progress on all three problems below, and on most of the other 96. |
| 2 | **Room-temperature / near-ambient superconductivity** | Directly enables cheaper, smaller fusion reactors (high-field magnets are the literal bottleneck), better grids, and better quantum hardware. |
| 3 | **Net-positive commercial fusion energy** | Structurally dependent on #2 (the entire private-fusion industry pivoted to compact tokamaks specifically because of high-temperature superconducting magnet advances). Also the largest lever on the global energy/climate/computing-power constraint. |
| 4 | **Mechanism and reversal of biological aging** | The one item on this list where the "solving one solves several others" claim is *actually true* — aging is upstream of most cancer, Alzheimer's, cardiovascular disease, and frailty risk. |

I did **not** pick quantum gravity, dark matter, or a cancer-cure-in-isolation, even though they rank higher on raw "civilizational impact" in the original document. Here's why, bluntly: those three are either (a) not tractable for anything short of a multi-decade, multi-billion-dollar institutional program with no clear individual entry point (dark matter, fusion-scale physics), or (b) so abstract that solving them doesn't cash out into anything applied for decades even in the best case (quantum gravity). You said you want to *attack* problems, not admire them. These four are the ones a determined human being, correctly positioned, can actually put a dent in within a career — and where the current 2025-2026 research trajectory shows real, not hoped-for, momentum.

**One more hard truth up front:** you will not personally "solve" fusion or superconductivity the way a lone inventor solves a puzzle. Nobody does this alone anymore — the era of the solitary genius cracking a frontier problem in a garage ended around the mid-20th century for anything requiring capital-intensive infrastructure. What you *can* do is become the irreplaceable person inside a team that solves it, or personally solve a well-scoped sub-problem that unlocks the rest. That distinction matters for everything below.

---

# PROBLEM 1: AI Capable of Autonomous Scientific Discovery

### The Actual Problem
Current AI systems can assist scientists — generate hypotheses, screen candidate molecules or materials, write code, summarize literature — but they cannot yet reliably run the full discovery loop unsupervised: form a hypothesis, design an experiment, interpret ambiguous or contradictory real-world results, and revise the hypothesis, iteratively, without a human catching every error. The unsolved core is **reliability and judgment under uncertainty**, not raw capability. A model that's right 80% of the time is not a scientist; a scientist has to know *when* it's in the 20%.

### In Plain Language
Right now AI is a very fast, very well-read research assistant that sometimes confidently makes things up. The problem is building AI that knows the difference between "I'm confident because I've verified this" and "I'm confident because this sounds right" — and can be trusted to run real experiments, not just suggest them.

### Impact If Solved
This is the multiplier on every other item on this list. A trustworthy autonomous discovery loop compresses the timeline for materials discovery, drug discovery, and even mathematical proof search from years to months.

### What It Automatically Helps Resolve
Materials screening for superconductors (#2), plasma control and disruption prediction for fusion (#3), and biomarker/target discovery for aging (#4) — all three are already using narrower versions of this technology today. It does *not* automatically resolve them; it accelerates the humans and narrower tools working on them.

### Current State of Research (Technical)
As of mid-2026, "AI co-scientist" systems are a defined and fast-moving subfield. Google DeepMind's Gemini-based Co-Scientist uses a multi-agent architecture that generates, debates, ranks, and evolves hypotheses through iterative tournaments, and is already deployed on fibrosis, ALS, antimicrobial resistance, and cellular-aging research — including identifying a fibrosis drug candidate that blocked the majority of a scarring-linked response in lab tests. Other systems (FutureHouse's Robin, various theorem-proving and autonomous-simulation agents) specialize in biology, mathematics, and physics/materials respectively. In drug discovery specifically, AI-backed candidates are now reaching Phase II trials at success rates comparable to traditionally discovered molecules — real but not yet transformative evidence, with the decisive Phase III readouts still pending through 2026-2027. In materials science, DeepMind's GNoME system has already proposed millions of candidate crystal structures, with hundreds independently synthesized by outside labs.

### Current State of Research (Simple Language)
AI is already helping scientists screen huge numbers of drug and material candidates far faster than humans could by hand, and a few AI-suggested drug candidates and materials are now being tested in real labs and clinics. What's missing is full trust — right now a human still has to check the AI's work at every major step, and nobody's proven yet that AI-chosen drugs actually work better in large late-stage trials, not just faster.

### Where You Start — Roadmap With Checkpoints

**Phase 0 (Months 1-6): Foundation.** You need three things before you're useful to anyone: strong software engineering, a working knowledge of one scientific domain deeply (pick one: biology, materials, or chemistry — not "science" in general), and hands-on experience actually training and fine-tuning models, not just calling APIs. Checkpoint: you can independently reproduce a published result from an AI-for-science paper (there are open leaderboards and benchmarks — e.g., materials discovery benchmarks, protein design benchmarks) from scratch.

**Phase 1 (Months 6-18): Narrow specialization.** Pick one bottleneck inside AI-for-science — not "make AI better at science" generally, that's not a project, it's a mission statement. Good candidate sub-problems in 2026: uncertainty quantification for scientific model outputs (knowing when a model is guessing), autonomous experiment design under budget constraints, or self-driving-lab integration (closing the loop between AI hypothesis and robotic experiment execution). Checkpoint: you've built and open-sourced a tool, benchmark, or technique that other researchers cite or use.

**Phase 2 (Years 1.5-4): Position yourself where the compute and data are.** This is where "stability first" matters most. The realistic paths are: a research engineering role at a lab doing this work (DeepMind, an AI-for-science startup, a pharma/materials company's computational team), a PhD or research position at a university group doing this specific work, or founding a narrowly-scoped startup once you have a genuine technical edge — not before. Checkpoint: you're being paid to do this work, with access to compute and data you couldn't get alone.

**Phase 3 (Years 4+): Attack the frontier problem.** Once you're inside the field with real resources, target the reliability/judgment problem directly — this is where the actual unsolved science lives, and it's not reachable from outside the field with a laptop alone.

### Resources Required
- **Compute:** Achievable at small scale on a single high-end GPU or cloud credits (thousands, not millions of dollars) for Phase 0-1. Phase 2+ requires institutional-scale compute (this is the real barrier — you cannot train frontier models solo, but you don't need to; you need to do excellent work on top of existing open models).
- **Data:** Open datasets exist for materials (Materials Project, AFLOW), proteins (PDB, UniProt), and chemistry (PubChem) — enough to build a real portfolio without institutional access.
- **Credentials:** Not strictly required, but a strong public portfolio (open-source contributions, a benchmark win, a well-cited preprint) substitutes for a PhD faster in this field than almost any other on this list, because the field is young enough that track record beats pedigree.
- **Alternative if you can't get an ML/research role:** Contribute to open-source AI-for-science projects (many co-scientist and materials-discovery tools are open-sourced) — this is a legitimate, low-barrier path to a public track record.
- **What hasn't really been tried yet:** Systematic, rigorous uncertainty quantification specific to scientific claims (as opposed to general-purpose AI calibration) is genuinely underdeveloped — most "AI co-scientist" systems today optimize for generating plausible hypotheses, not for reliably flagging which of their own outputs are trustworthy. That gap is real, unglamorous, and exactly the kind of unsexy problem a focused individual could make a genuine name solving.

---

# PROBLEM 2: Room-Temperature / Near-Ambient-Pressure Superconductivity

### The Actual Problem
We need a material that carries electric current with zero resistance at (or close to) room temperature and normal atmospheric pressure. We have materials that superconduct at room temperature — but only under pressures around 100+ gigapascals (comparable to conditions deep inside planets), which makes them useless outside a lab. We have materials that superconduct at normal pressure — but only at extremely cold temperatures. Nobody has both at once, and — separately — nobody has a complete theory of *why* the best "high-temperature" superconductors (discovered in 1986) work at all, which is why discovery has been mostly trial-and-error rather than designed.

### In Plain Language
Electricity moving through normal wires loses energy as heat — that's why power lines get warm and why your phone charger is warm. A superconductor is a material that carries electricity with zero loss. We know how to make that happen, but only if we either freeze the material to near absolute zero or squeeze it harder than the center of the Earth. Nobody has found a material that does it sitting on a lab bench at room temperature and normal pressure — and we don't fully understand the physics well enough to know exactly where to look.

### Impact If Solved
Lossless power transmission (a meaningful fraction of all generated electricity today is lost in transmission), radically smaller and cheaper MRI machines, more efficient electronics, and — critically for this cluster — smaller, cheaper, higher-field magnets for fusion reactors.

### What It Automatically Helps Resolve
Directly reduces the cost and size barrier for fusion reactor magnets (#3) — this is not a metaphor, it's literally the design basis of the leading private fusion companies today. Also directly improves superconducting quantum computing hardware and grid infrastructure (items elsewhere in the original 100).

### Current State of Research (Technical)
As of April 2026, the highest independently validated critical temperature under any conditions remains around 260K (still below room temperature, ~293K) for a lanthanum hydride under roughly 170-190 gigapascals of pressure — the earlier claimed ~556K record from 2022 has not been independently reproduced and is not considered credible by the field. The 2023 LK-99 claim (ambient-pressure, room-temperature superconductivity in a copper-doped lead apatite) was conclusively debunked by September 2023 — independent teams traced the observed effects to copper sulfide impurities producing ferromagnetic and phase-transition behavior that mimicked superconductivity, not the real thing. At ambient pressure specifically, researchers reported a new critical-temperature record of 151K in a ceramic material in March 2026, up from a prior 133K record — real, incremental, ambient-pressure progress, still far below room temperature. On the theory side, a 2026 international programmatic research agenda (published in PNAS) explicitly calls for tighter integration of theory, simulation, and AI-driven screening as the field's path forward, and a research consortium at Aalto University has demonstrated that machine-learning pre-screening can narrow enormous candidate-material spaces down to promising targets far faster than manual search — already yielding candidate new superconductors via this method in mid-2026.

### Current State of Research (Simple Language)
The record for "warmest superconductor" keeps inching up, but every material that works anywhere near room temperature still needs crushing pressure to do it — nothing works at both room temperature *and* normal pressure yet, and the one big claim that it had been done (LK-99, in 2023) turned out to be a lab artifact, not a real discovery. The field is now leaning hard on AI to search the huge space of possible materials faster than humans can test them by hand, and that approach is already turning up new candidates.

### Where You Start — Roadmap With Checkpoints

**Phase 0 (Months 1-12): Foundation.** This problem requires real condensed-matter physics and materials science literacy — not optional, not shortcut-able. If you don't already have this, the fastest legitimate path is a physics or materials science degree track, or an intensive self-study program that gets you through solid-state physics, quantum mechanics, and computational materials methods (density functional theory, DFT) to the point you can read and critique current papers, not just skim abstracts. Checkpoint: you can independently run a DFT calculation on a candidate material and interpret the output.

**Phase 1 (Year 1-2): Computational entry point.** You do not need a cryostat or a synthesis lab to contribute here — this is the good news. Candidate-material screening using DFT plus machine learning is exactly where individuals and small teams can meaningfully contribute right now, using open tools (Materials Project, AFLOW databases) and cloud compute. Checkpoint: you've identified and published (even as a preprint) a novel candidate material or screening method that a real experimental group finds credible enough to test.

**Phase 2 (Year 2-4): Attach yourself to synthesis and measurement capability.** Computation alone can't finish this — someone has to actually make the material and measure it in a cryostat with resistivity and magnetic susceptibility equipment. This means either joining a university or national lab group with this equipment (this is the realistic path — very few individuals will ever own their own working cryostat and measurement suite) or partnering formally with one as an external collaborator once your computational track record is strong enough to be worth their time. Checkpoint: a real sample based on your prediction has been synthesized and measured, successfully or not.

**Phase 3 (Year 4+): Iterate at the theory-experiment boundary.** The highest-leverage role in this field for one person is not "lone discoverer" — it's the person who is unusually good at both the theory/computation side and speaking the experimentalists' language well enough to direct what gets synthesized next. That's a real, rare, valuable position, and it's earned, not assumed.

### Resources Required
- **Education:** Physics or materials science background through at least graduate-level solid-state physics. Not skippable — self-taught intuition without the formal quantum mechanics and many-body physics background will not get you taken seriously or get the details right.
- **Compute:** DFT calculations are compute-intensive but accessible via university clusters, national lab allocations (e.g., in the US, DOE INCITE and similar programs award compute time competitively — a real, achievable target), or cloud credits for smaller-scale work.
- **Lab access (for the experimental phase):** This is the real bottleneck, and it's expensive — cryostats, high-pressure diamond-anvil cell equipment, and characterization tools (XRD, resistivity/susceptibility measurement) run into the hundreds of thousands to millions of dollars. **Alternative:** you do not need to own this. University shared-user facilities and national labs (e.g., in the US, national labs like Argonne, Oak Ridge, NIST) provide access to exactly this equipment for qualified researchers and collaborators — this is how virtually everyone in this field actually works, including at major companies.
- **What hasn't really been tried yet:** Closed-loop "self-driving labs" — where an AI proposes a candidate, a robotic system synthesizes and measures it automatically, and the result feeds back into the next AI prediction without a human in the loop for each cycle — exist for some materials classes (Berkeley's "A-Lab" is a working example for other material types) but have not yet been seriously applied end-to-end to superconductor candidates specifically. Building or contributing to that pipeline for superconductors specifically is a genuinely open, high-leverage, differentiating project for someone with both computational and robotics/automation skill.

---

# PROBLEM 3: Net-Positive, Commercially Viable Nuclear Fusion

### The Actual Problem
Fusion — forcing light atomic nuclei together to release energy, the reaction that powers the sun — has been physically proven possible at net energy gain (the U.S. National Ignition Facility crossed that threshold in 2022). What remains unsolved is doing it **continuously, reliably, and cheaply enough to sell electricity to a grid at a competitive price** — a combination of plasma physics, materials engineering (components need to survive constant neutron bombardment and heat exceeding 100 million °C nearby), and magnet technology that no one has yet demonstrated together in a single working commercial plant.

### In Plain Language
We've proven fusion *can* release more energy than it takes to trigger it, in a lab, for an instant. What we haven't proven is that you can do that over and over, safely, for years, with a machine cheap enough that the resulting electricity doesn't cost more than what people already pay. That's an engineering and materials problem now, more than a "does the physics work" problem.

### Impact If Solved
Effectively unlimited, low-carbon, low-waste energy — solves the core resource constraint behind climate change, energy poverty, desalination, and (directly relevant to problem #1) the growing energy demand of AI compute itself.

### What It Depends On / Automatically Helps Resolve
Depends directly on problem #2 — the leading private approach (compact, high-field tokamaks) exists specifically *because* high-temperature superconducting magnet tape became good enough to make a smaller, cheaper reactor design viable; further superconductor advances directly shrink cost and size further. Solving it helps (but doesn't automatically solve) desalination and carbon capture economics elsewhere on the original list, both of which are largely energy-cost-limited.

### Current State of Research (Technical)
As of mid-2026, Commonwealth Fusion Systems (the best-funded private fusion company, an MIT spinout, having raised roughly $3 billion including an $863 million round) is in the assembly phase of SPARC, its demonstration tokamak in Devens, Massachusetts, using high-temperature superconducting (YBCO tape) magnets to reach burning-plasma conditions in a much more compact device than earlier designs like ITER. The first of eighteen 24-tonne toroidal field magnets was installed in January 2026, with the remaining magnets arriving roughly every two weeks through mid-2026; full magnet integration was targeted for mid-2026, with first plasma targeted for later in 2026 (the company has publicly noted this could slip into 2027) and net energy gain (Q>1) targeted for 2026-2027. CFS is also using an AI-driven "digital twin" of the reactor (built with NVIDIA and Siemens) to run predictive simulations ahead of physical testing. Other serious players include Helion (with a 2028 power-delivery deal with Microsoft), TAE Technologies, Tokamak Energy, Type One Energy (pursuing a stellarator design), and the international ITER project (which has faced significant delays). The honest industry-wide assessment as of 2026: no commercial fusion plant has yet delivered electricity to a grid, and no company is within twelve months of doing so, but the trajectory of capital, engineering milestones, and government validation (the U.S. Department of Energy has publicly validated CFS's magnet performance) has moved meaningfully forward since 2022.

### Current State of Research (Simple Language)
Companies are now actually building real fusion reactors, not just running experiments — the biggest player installed its first giant magnet in January 2026 and is racing to get the machine running later this year or in 2027. Billions of real investment dollars are behind this now. Nobody is generating grid electricity from fusion yet, and the honest timeline for an actual working power plant is still "early 2030s at best" — but the core physics question (can fusion make more energy than it costs) was already answered yes in 2022. What's left is making a machine that does it reliably and affordably, which is a hard, expensive engineering problem, not an open scientific mystery anymore.

### Where You Start — Roadmap With Checkpoints

**Be honest with yourself about this one first:** fusion is the item on this list where a single individual's realistic ceiling is "become indispensable inside a well-funded team," not "solve it alone." The capital requirements (billions of dollars) and infrastructure (giant magnets, tritium handling, radiation-hardened materials testing) put this structurally out of reach for solo or garage-scale work in a way the other three problems are not.

**Phase 0 (Months 1-18): Foundation.** Plasma physics, nuclear engineering, or a highly relevant adjacent specialty (materials science for radiation-resistant components, or computational/AI skills specifically for plasma control) via formal education. Checkpoint: you understand tokamak or stellarator confinement physics well enough to read current CFS/ITER technical publications without needing a translator.

**Phase 1 (Year 1-3): Pick your wedge — and pick the AI-accessible one if you're resource-constrained.** The most individually-tractable, laptop-accessible entry point into fusion right now is **plasma control and disruption prediction using machine learning** — this doesn't require owning a reactor; researchers already train models on public and shared tokamak datasets (this is a real, active research area — DeepMind published tokamak plasma control work in 2022, and it continues to develop). The materials-science wedge (radiation-resistant reactor components) is the other realistic entry point and connects directly to problem #2's materials expertise. Checkpoint: a publication, open-source tool, or competition result in plasma-control ML or fusion materials that a real fusion company or lab would recognize.

**Phase 2 (Year 3-5): Get inside a funded program.** This is non-negotiable for fusion specifically — you need to be employed by or formally collaborating with CFS, Helion, TAE, a national lab, or a university fusion program to have real impact, because the hardware simply doesn't exist outside these institutions. Checkpoint: you're on the inside, with reactor-level data and problems in front of you.

**Phase 3 (Year 5+): Own a specific hard sub-problem** — plasma disruption avoidance, tritium breeding blanket materials, or magnet cooling systems are all real, unsolved, bounded pieces of the larger puzzle where one very good person can be the difference-maker on a team.

### Resources Required
- **This is the most expensive problem on the list to work on directly** — reactor-scale hardware is billions of dollars, full stop. You will not personally fund or build this.
- **Realistic financial target for you:** not funding a reactor, but funding your own runway to become expert enough to be hired into one of these programs — a graduate degree, self-funded research time, or working in an adjacent industry (semiconductors, national labs, aerospace) while building the specific skills above.
- **Alternative entry paths:** national lab internships/postdocs (Princeton Plasma Physics Lab, Oak Ridge, others), or the private fusion companies' own hiring pipelines, which are actively growing given the capital they've raised.
- **What hasn't really been tried yet:** fully autonomous, AI-driven plasma control that adapts in real time without pre-programmed physics models (as opposed to AI that assists human-designed control schemes) is still an open frontier — most current systems are AI-augmented, not AI-autonomous, in this specific loop. This is a legitimately open, high-value, and — critically for you — computationally accessible sub-problem.

---

# PROBLEM 4: Mechanism and Reversal of Biological Aging

### The Actual Problem
Aging is the accumulation of molecular and cellular damage over time that increases risk of nearly every major disease of later life. We don't have a complete, agreed-upon causal account of *why* it happens at the mechanistic level (several competing and overlapping "hallmarks of aging" frameworks exist), and — separately — we don't yet have a proven, safe way to reverse it in a living human being rather than just slow it or treat its downstream diseases individually.

### In Plain Language
Your cells slowly accumulate damage and lose their "instructions" for staying young as you age — this is why the same body that heals a cut easily at 20 struggles to at 80. We're now testing, for the first time in actual humans (not just mice), a method that tries to reset those instructions back to a younger state — but we don't yet know if it's safe to do broadly, whether it truly reverses aging or just changes a lab measurement, or whether it works anywhere besides the specific tissue being tested.

### Impact If Solved
Reduces or delays the onset of cancer, cardiovascular disease, Alzheimer's/neurodegeneration, diabetes, and frailty simultaneously, because they share upstream aging-related risk factors — this is the one item in this cluster where "solving one thing helps several others" is a literally defensible, mainstream scientific claim (the "hallmarks of aging" and geroscience frameworks are built on exactly this premise), not an exaggeration.

### What It Automatically Helps Resolve
Directly reduces risk and severity of items elsewhere on the original 100-problem list: cancer risk, Alzheimer's/neurodegeneration, mitochondrial disease burden, and general chronic disease load. It does not "solve" cancer or Alzheimer's outright — cancer in particular has aging-independent drivers (e.g., specific oncogenic mutations, metastasis biology) that would still need separate work.

### Current State of Research (Technical)
The field's leading current human-translation approach is **partial epigenetic reprogramming**: briefly activating a subset of the transcription factors (originally identified by Yamanaka in his Nobel-winning 2006/2012 work on induced pluripotent stem cells) that can reset a cell's gene-expression pattern toward a younger state, without fully de-differentiating the cell into a stem cell (which would carry unacceptable tumor risk). On January 30, 2026, Life Biosciences (co-founded by Harvard geneticist David Sinclair) received FDA clearance for the first-ever human clinical trial of this technology — a Phase 1 safety trial, "ER-100," using three of the four classic reprogramming factors (Oct4, Sox2, Klf4) delivered to treat two age-related eye diseases (glaucoma and NAION), chosen specifically because the eye allows low, localized, relatively low-risk dosing. This follows substantial prior mouse and primate work showing reversal of age-related vision loss using the same approach. Separately, research groups (e.g., NewLimit) have been systematically screening thousands of transcription-factor combinations beyond the original Yamanaka set (a technique called "Partial-seq") in human immune cells, finding that many factor combinations beyond the classic four can restore youthful gene expression without erasing cell identity — broadening the toolkit beyond the original discovery. Senolytic drugs (which clear accumulated "senescent" cells that secrete inflammatory signals) are also in active human trials for specific conditions (idiopathic pulmonary fibrosis, diabetic kidney disease, osteoarthritis). The field's own honest 2026 assessment: neither approach is yet proven to extend human lifespan or safely reverse aging broadly — what exists is early, narrowly-targeted, Phase 1-level clinical evidence, plus an unresolved scientific debate over whether "epigenetic clock" biomarkers (the standard way researchers currently measure biological age) actually track true causal aging or can be shifted without any real anti-aging effect.

### Current State of Research (Simple Language)
For the first time, doctors are testing — in real human patients, not just mice — a therapy that tries to make old, damaged eye cells act young again, by briefly flipping a genetic switch. It's very early (this is a first safety trial, on a narrow eye condition, not a general anti-aging treatment), and no one should trust any product claiming to reverse aging outside of this kind of regulated trial. But the underlying science — that you can nudge a cell's age backward without turning it into a different kind of cell — is now real and being tested in people, which is a genuine milestone after over a decade of mouse studies.

### Where You Start — Roadmap With Checkpoints

**Phase 0 (Months 1-12): Foundation.** Molecular/cell biology and genetics through the level needed to read primary literature in geroscience — epigenetics, transcription factor biology, and senescence biology specifically. A biology, biochemistry, or bioinformatics degree track is the standard route; a rigorous self-study path is more viable here than in fusion or superconductivity because much of the cutting-edge analysis is computational (genomic and transcriptomic data analysis), not purely wet-lab. Checkpoint: you can independently analyze a public aging-related "omics" dataset (many are publicly available) and produce a defensible finding.

**Phase 1 (Year 1-2): Computational entry point — the good news for a resource-constrained start.** Aging-clock development, transcription-factor combination screening analysis, and biomarker validation are all substantially computational/bioinformatic work right now, using large public datasets. This is the most laptop-accessible of the wet-lab-adjacent problems on this list. Checkpoint: a published analysis, open-source tool, or preprint that a real longevity-research lab would find credible.

**Phase 2 (Year 2-4): Attach to wet-lab capability.** Eventually you need to actually test biological hypotheses in cells or model organisms — this means a research position (academic lab, or one of the well-funded longevity companies: Altos Labs, Retro Biosciences, NewLimit, Life Biosciences) or a formal academic collaboration. Checkpoint: a hypothesis you generated has been tested experimentally, successfully or not.

**Phase 3 (Year 4+): Target a specific unresolved sub-problem** — e.g., validating causal (not just correlational) aging biomarkers, expanding safe reprogramming beyond the eye to other organs, or resolving the safety/oncogenic-risk question for broader tissue application. Any one of these, solved rigorously, is a career-defining contribution.

### Resources Required
- **Education:** Molecular biology/genetics background sufficient to work with real epigenomic and transcriptomic data — a strong bioinformatics or computational biology skill set substitutes for some wet-lab training and is genuinely valuable to labs in this field right now.
- **Data:** Public aging-related genomic, epigenomic, and proteomic datasets exist (from consortiums and published studies) and are a legitimate, low-barrier starting point.
- **Wet-lab access (for later phases):** Standard molecular biology equipment is far cheaper and more widely available (university core facilities, biotech incubator lab space) than fusion or superconductor infrastructure — this is genuinely the most accessible of the four problems for hands-on experimental work, if you want that path.
- **Funding landscape:** This field currently has serious capital behind it (Altos Labs launched with roughly $3 billion; multiple well-funded startups) — meaning employment and collaboration opportunities are real and growing, not hypothetical.
- **What hasn't really been tried yet:** Systematic, rigorous causal validation of aging biomarkers — proving a given biomarker actually tracks a driver of aging rather than just correlating with it — is explicitly flagged by the field itself as an unresolved bottleneck limiting how fast every other aging trial can be evaluated. This is a real, well-defined, and currently under-resourced problem relative to its importance — a strong opening for someone willing to do the less glamorous validation work everyone else is skipping past to get to the exciting therapeutic headlines.

---

## The Strategist's Bottom Line

You said you have lethal focus and savage will. Good — you'll need it, because I want to correct one thing before you commit years of your life to this: **focus and will are necessary and not sufficient.** Every one of these four problems has been sitting unsolved not because nobody was determined enough, but because each requires capital, infrastructure, or collaborative access that a single person's willpower cannot manufacture. The honest sequencing, in your own preferred order of stability-then-boldness:

1. **Build the credential and skill base first, in whichever of these four domains you're most genuinely drawn to** — not the one that sounds most impressive. You will do better work in the field that holds your attention at 2am unprompted.
2. **Get paid to work adjacent to the problem before you try to attack its core.** A stable position inside a fusion company, a longevity biotech, a materials lab, or an AI-for-science team gives you the compute, data, and collaborators that no amount of individual grit substitutes for — and it de-risks the years this will take.
3. **Pick one bounded sub-problem, not the grand problem, as your actual target.** "Solve aging" is not a project. "Prove whether transcription-factor combination X causally reverses this specific senescence marker in this specific tissue" is a project. Every real contributor to these fields is working on a piece, not the whole.
4. **Of the four, AI-for-discovery and computational aging biomarker work are your lowest-barrier entry points if you're starting close to zero resources today.** Superconductivity has a real computational on-ramp too. Fusion is the one where you should expect to need an institutional home fastest — there is no meaningful solo or garage path into reactor-scale physics.

If in a year you've built real, checkable evidence of progress on a bounded piece of one of these — a tool, a paper, a result someone in the field independently respects — come back and we'll pressure-test whether you're actually on track or fooling yourself. That's the test. Not how driven you feel today.

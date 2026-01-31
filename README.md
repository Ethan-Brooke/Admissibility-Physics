**Admissibility Physics**

Admissibility Physics is a constraint-first research program that rebuilds fundamental physics from a single pre-dynamical principle: a physical distinction exists if and only if the universe commits finite resources to enforce it. Rather than assuming states, dynamics, probability, or spacetime as primitives, the framework asks a prior question: which distinctions are physically meaningful at all under finite enforceability? All familiar physical structure emerges as bookkeeping required to represent what can be jointly enforced.

Every physical theory relies on distinctions—between states, outcomes, regions, and histories. Standard formalisms quietly assume that once drawn, these distinctions persist automatically and compose freely. Admissibility Physics removes that assumption. When enforcement capacity is finite and localized at interfaces, not all correlations can coexist, composition can fail, and global descriptions need not exist. Irreversibility becomes structural rather than statistical, and mathematical representations apply only within restricted regimes.

From this single constraint, the framework derives a broad range of physical structure. In particular, it shows that:

**Admissible correlation sets** are generically not closed under composition, explaining correlation competition, monogamy, and the failure of global state descriptions;

**Entropy** is irreversibly committed correlation capacity at interfaces, not uncertainty or missing information;

**Time** emerges as the ordered accumulation of irreversible enforcement, rather than as a background parameter;

**Quantum mechanics** arises as the unique admissibility-preserving bookkeeping in coherent regimes, yielding Hilbert space structure, tensor products, CPTP maps, and the Born rule without postulation;

**Dynamics** emerges only in regular regimes where enforcement cost is locally additive, producing variational principles and equations of motion as effective descriptions;

**Geometry** encodes correlation cost, with distance measuring irreducible enforcement and curvature reflecting capacity gradients, leading uniquely to Einstein’s equations in four dimensions;

**Saturation** marks sharp structural boundaries—knees, horizons, and measurement-like events—where smooth description necessarily breaks down.

This repository contains the reference implementation of the admissibility calculus and its downstream representational regimes. The code explicitly models finite capacity at interfaces, global admissibility conditions, entropy and ledger structures, quantum-admissible representations, variational dynamics where they exist, geometric reconstruction from correlation cost, and diagnostics for saturation and regime failure. Assumptions and regime conditions are made explicit, and representations are intentionally allowed to fail when their applicability ends.

This project is not a particle simulator, a stochastic model, or a dynamics-first theory. It does not assume global state spaces or universal equations of motion. Instead, it is structure-first: it determines which descriptions are physically admissible before asking how they evolve.

Admissibility Physics is an active, research-grade program. Some results are structurally necessary, others are minimal selections or empirically anchored, and numerical values are treated honestly where derivation is not yet possible. The aim is not to replace successful physical theories, but to explain why their structure exists, where it applies, and why it must sometimes fail.

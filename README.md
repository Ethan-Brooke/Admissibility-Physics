Admissibility Physics

Admissibility Physics is a constraint-first research program that rebuilds fundamental physics from a single pre-dynamical principle:

A physical distinction exists if and only if the universe commits finite resources to enforce it.

Rather than postulating states, dynamics, probability, or spacetime as primitive, the framework asks a prior question: Which distinctions are physically meaningful at all, given finite enforcement capacity?
All subsequent structure—quantum mechanics, entropy, time, geometry, and gravity—emerges as bookkeeping required to represent what can be jointly enforced.

Core Idea

Every physical theory relies on distinctions: between states, outcomes, regions, histories. Standard formalisms silently assume these distinctions persist automatically and compose freely.

Admissibility Physics makes this assumption explicit—and removes it.

If enforcing distinctions requires finite resources localized at interfaces, then:

not all correlations can coexist,

composition can fail,

global descriptions need not exist,

irreversibility is structural rather than statistical,

and familiar mathematical representations apply only in restricted regimes.

The framework formalizes this using admissibility: a global joint-enforceability condition under finite correlation capacity.

What the Framework Derives

Starting from finite enforceability alone, the program derives:

Non-closure under composition
Jointly admissible correlations need not compose, explaining monogamy, global state failure, and competition for structure.

Entropy as committed correlation capacity
Entropy is not uncertainty or probability—it is irreversible enforcement already paid at interfaces.

Time as ordered commitment
Temporal direction emerges from monotonic accumulation of irreversible commitments, not from dynamics.

Quantum mechanics as admissible representation
Hilbert space, linearity, tensor products, CPTP maps, and the Born rule arise as the unique bookkeeping structures that preserve admissibility in coherent regimes.

Dynamics as extremal admissible reallocation
Variational principles and equations of motion emerge only when enforcement cost is locally additive; they fail generically near saturation.

Geometry as correlation cost
Distance measures irreducible enforcement cost; curvature reflects capacity gradients; Einstein’s equations arise as the unique admissibility-preserving closure in four dimensions.

Sharp regime boundaries
Saturation produces knees, horizons, measurement-like events, and breakdowns of smooth description—structural limits rather than dynamical pathologies.

What This Codebase Implements

This repository contains the reference implementation of the admissibility calculus and its downstream representational regimes. It includes:

capacity accounting at interfaces,

admissibility checks and cut-set bounds,

entropy and irreversible ledger structures,

quantum-admissible representations,

variational dynamics in regular regimes,

geometric reconstruction from correlation cost,

and diagnostics for saturation and regime failure.

The code is intentionally explicit about assumptions, regime conditions, and failure modes. Where a representation ceases to be meaningful, the code stops—by design.

What This Is Not

Not a simulation of particles or fields

Not a probabilistic or stochastic model

Not a numerical solver for fundamental constants

Not dynamics-first or state-space-first physics

Admissibility Physics is structure-first: it determines what physics is allowed to describe before asking how descriptions evolve.

Status and Scope

This project is active, research-grade, and exploratory. Some results are structural necessities; others are minimal selections or empirically anchored. Numerical values are treated honestly where derivation is not yet possible.

The goal is not to replace existing successful theories, but to explain why their structure exists, where it applies, and why it must sometimes fail.

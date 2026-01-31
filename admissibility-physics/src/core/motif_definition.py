"""
ADMISSIBLE MOTIF: FORMAL DEFINITION
====================================

This document provides the canonical definition of "motif" in Admissibility Physics.
It is substrate-independent and applies to both mean-field and hypergraph backends.

Author: Admissibility Physics Project
Date: January 2026
Version: 1.0

================================================================================
DEFINITION (Admissible Motif)
================================================================================

A **motif** M is a finite subset of distinctions (or, in the hypergraph backend,
a finite connected subgraph) satisfying three axioms:

(M1) JOINT COMMITMENT
    All elements of M become committed within a bounded temporal window Ï„_c.
    
    Formally: âˆƒ tâ‚€ such that âˆ€ d âˆˆ M: commit_time(d) âˆˆ [tâ‚€, tâ‚€ + Ï„_c]
    
    Default: Ï„_c = 3 steps

(M2) PERSISTENCE
    M persists under admissible microdynamics with probability â‰¥ p_min.
    
    Formally: P(M âŠ† S(t) for all t â‰¥ t_commit | M committed) â‰¥ p_min
    
    Default: p_min = 0.5

(M3) BOUNDED LEDGER COST
    M incurs bounded ledger cost per step after commitment.
    
    Formally: E[Î”R per step | M exists] â‰¤ L_max
    
    Default: L_max = 1.0 (or finite, context-dependent)

================================================================================
DERIVED QUANTITIES
================================================================================

Given a motif M, we define:

**Size**: |M| = number of distinctions (or nodes/edges in hypergraph)

**Commit Time**: t_c(M) = min{commit_time(d) : d âˆˆ M}

**Commit Spread**: Ïƒ_c(M) = std{commit_time(d) : d âˆˆ M}
    - Small spread â†’ "tight" motif (committed together)
    - Large spread â†’ "loose" motif (staged commitment)

**Persistence**: P(M) = fraction of post-commitment steps where M âŠ† S(t)

**Ledger Efficiency**: L(M) = Î”R / steps_survived
    - Low L(M) â†’ "light" motif
    - High L(M) â†’ "heavy" motif
    - This is the MASS PROXY

**Interface Signature**: Q_i(M) = E_i(S) - E_i(S \\ M)
    - The enforcement load contributed by M at interface i
    - This is the CHARGE PROXY
    - Vector Q(M) = (Q_1(M), Q_2(M), ..., Q_n(M)) for n interfaces

**SWAP Survival**: S(M) = fraction of SWAP proposals survived while M exists
    - High S(M) â†’ "mobile" motif
    - Low S(M) â†’ "immobile" motif (but not necessarily heavy)

================================================================================
MOTIF CLASSIFICATION
================================================================================

Motifs are classified by:

1. SIZE CLASS: {singleton, pair, triple, ...}

2. STABILITY CLASS:
   - Stable: P(M) â‰¥ 0.9
   - Metastable: 0.5 â‰¤ P(M) < 0.9
   - Unstable: P(M) < 0.5

3. MASS CLASS (by ledger efficiency):
   - Light: L(M) < 0.1
   - Medium: 0.1 â‰¤ L(M) < 1.0
   - Heavy: L(M) â‰¥ 1.0

4. CHARGE CLASS (by interface signature):
   - Neutral: Q(M) â‰ˆ 0 at all interfaces
   - Charged: Q(M) â‰  0 at some interface
   - Multi-charged: Q(M) â‰  0 at multiple interfaces

================================================================================
INTERACTION OUTCOMES
================================================================================

When two motifs M, N approach (in hypergraph) or coexist (in mean-field):

- ANNIHILATE: Both M and N disappear, ledger spikes
- FUSE: M âˆª N becomes a new committed motif
- SCATTER: M and N persist but exchange distinctions
- COEXIST: M and N both persist independently
- DECOHERE: At least one motif loses coherence (uncommits or fragments)

================================================================================
SUBSTRATE INDEPENDENCE
================================================================================

This definition applies to:

1. MEAN-FIELD BACKEND
   - Distinction = integer ID
   - M = FrozenSet[int]
   - No geometry, no position

2. HYPERGRAPH BACKEND
   - Distinction = edge or subgraph
   - M = connected sub-hypergraph
   - Position defined by node coordinates (if assigned)

The transition from mean-field to hypergraph is:
   - Each distinction â†’ small hypergraph motif
   - Commitment â†’ subgraph freeze
   - SWAP â†’ edge rerouting
   - Interface load â†’ cut load

================================================================================
PHYSICAL INTERPRETATION
================================================================================

In the Admissibility Physics framework:

| Motif Property | Physical Analog |
|----------------|-----------------|
| Existence      | Particle        |
| Size           | Particle type   |
| Persistence    | Stability       |
| Ledger cost    | Mass            |
| Interface sig  | Charge          |
| SWAP survival  | Mobility        |
| Interactions   | Scattering      |

These are DERIVED from A1-A6, not assumed.

================================================================================
CONSTANTS (Tunable)
================================================================================

COMMIT_WINDOW = 3        # Ï„_c: max steps for "joint" commitment
PERSISTENCE_MIN = 0.5    # p_min: minimum persistence to qualify
LEDGER_MAX = 1.0         # L_max: maximum ledger cost per step
SIGMA_THRESHOLD = 0.5    # Ïƒ value above which commitment triggers (in engine)

================================================================================
"""

# Formal constants
COMMIT_WINDOW = 3
PERSISTENCE_MIN = 0.5
LEDGER_MAX = 1.0
SIGMA_THRESHOLD = 0.5

# For programmatic access
MOTIF_DEFINITION = {
    "M1_joint_commitment": {
        "description": "All elements commit within bounded temporal window",
        "parameter": "Ï„_c",
        "default": COMMIT_WINDOW
    },
    "M2_persistence": {
        "description": "Motif persists with probability â‰¥ p_min",
        "parameter": "p_min", 
        "default": PERSISTENCE_MIN
    },
    "M3_bounded_cost": {
        "description": "Ledger cost per step â‰¤ L_max",
        "parameter": "L_max",
        "default": LEDGER_MAX
    }
}

def is_valid_motif(
    commit_times: dict,
    persistence: float,
    ledger_per_step: float,
    tau_c: int = COMMIT_WINDOW,
    p_min: float = PERSISTENCE_MIN,
    L_max: float = LEDGER_MAX
) -> tuple:
    """
    Check if a candidate satisfies the motif definition.
    
    Returns (is_valid, violations) where violations is a list of failed axioms.
    """
    violations = []
    
    # M1: Joint commitment
    if commit_times:
        times = list(commit_times.values())
        spread = max(times) - min(times)
        if spread > tau_c:
            violations.append(f"M1: commit spread {spread} > Ï„_c={tau_c}")
    
    # M2: Persistence
    if persistence < p_min:
        violations.append(f"M2: persistence {persistence:.2f} < p_min={p_min}")
    
    # M3: Bounded ledger cost
    if ledger_per_step > L_max:
        violations.append(f"M3: ledger/step {ledger_per_step:.2f} > L_max={L_max}")
    
    return (len(violations) == 0, violations)


if __name__ == "__main__":
    print(__doc__)

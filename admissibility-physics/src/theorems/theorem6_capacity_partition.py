"""
THEOREM 6: ELECTROWEAK MIXING FROM UNIFICATION + CAPACITY PARTITION

The weak mixing angle sinÂ²Î¸_W is NOT a free parameter.
At the GUT scale, it is FIXED by group theory:

    sinÂ²Î¸_W(M_GUT) = 3/8

This theorem derives this from:
1. SU(5) hypercharge embedding (Theorem 5.5)
2. Generator normalization (Tr(TÂ²) conventions)
3. "Mode democracy" at unification (equal coupling per generator)

Admissibility interpretation:
    Î¸_W measures capacity allocation between isospin and hypercharge 
    enforcement channels.
"""

from fractions import Fraction
from dataclasses import dataclass
from typing import List, Tuple
import math

# =============================================================================
# SETUP: THE ELECTROWEAK MIXING PROBLEM
# =============================================================================

SETUP = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THEOREM 6: SETUP â€” THE ELECTROWEAK MIXING PROBLEM
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

THE STANDARD MODEL HAS TWO ELECTROWEAK COUPLINGS:

    gâ‚‚  for SU(2)_L  (weak isospin)
    gâ‚  for U(1)_Y   (hypercharge)

The WEAK MIXING ANGLE is defined by:

    sinÂ²Î¸_W = gâ‚Â² / (gâ‚Â² + gâ‚‚Â²)

OBSERVED VALUE (at M_Z):

    sinÂ²Î¸_W â‰ˆ 0.231

THE DEEP QUESTION:

    Why do the couplings have this particular ratio?
    Is it arbitrary, or structurally determined?


FROM THEOREM 5.5:

    If G_SM embeds in SU(5), then hypercharge Y is a generator
    with FIXED normalization relative to SU(2).
    
    This means the RATIO gâ‚/gâ‚‚ at the unification scale is NOT free.


THE CLAIM:

    At the GUT scale M_U where SU(5) is unbroken:
    
        sinÂ²Î¸_W(M_U) = 3/8 = 0.375
    
    This is a GROUP-THEORETIC necessity, not a parameter choice.
"""


# =============================================================================
# DEFINITIONS
# =============================================================================

DEFINITIONS = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
DEFINITIONS
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

D6.1 (Coupling as Enforcement Throughput):
    
    In Admissibility Physics:
    
    â€¢ Each gauge generator = a distinguishability-enforcement mode
    â€¢ The coupling g measures coordination throughput per generator
    â€¢ gâ»Â² ~ capacity cost per unit distinction flux
    
    The gauge kinetic term:
        (1/gÂ²) âˆ« Tr(FÂ²)
    
    represents enforcement capacity allocated to that gauge sector.


D6.2 (Electroweak Partition):

    Electroweak symmetry partitions enforcement into two channels:
    
    â€¢ SU(2)_L: weak isospin distinction modes (3 generators)
    â€¢ U(1)_Y:  hypercharge distinction mode (1 generator)
    
    The mixing angle measures the partition:
    
        sinÂ²Î¸_W = gâ‚Â² / (gâ‚Â² + gâ‚‚Â²)
                = (U(1) throughput) / (total EW throughput)


D6.3 (Generator Normalization):

    For a simple Lie group G with generators Táµƒ:
    
        Tr(Táµƒ Táµ‡) = T(R) Î´áµƒáµ‡
    
    where T(R) is the Dynkin index of representation R.
    
    For the fundamental representation:
    â€¢ SU(N): T(fund) = 1/2
    
    CONVENTION: We normalize all generators so Tr(TÂ²) = 1/2 
    in the fundamental representation.
"""


# =============================================================================
# LEMMA 6A: HYPERCHARGE NORMALIZATION IN SU(5)
# =============================================================================

LEMMA_6A = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
LEMMA 6A: HYPERCHARGE NORMALIZATION IN SU(5)
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

FROM THEOREM 5.5:

    In SU(5), the hypercharge generator is:
    
        Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2)


CLAIM: The properly normalized hypercharge generator is:

        Y_normalized = âˆš(3/5) Ã— Y_SM
    
    where Y_SM is the Standard Model hypercharge.


PROOF:

Step 1: Compute Tr(YÂ²) in the fundamental 5
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2)
    
    Tr(YÂ²) = 3 Ã— (1/3)Â² + 2 Ã— (1/2)Â²
           = 3 Ã— (1/9) + 2 Ã— (1/4)
           = 1/3 + 1/2
           = 5/6


Step 2: Compare with SU(2) generator normalization
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    For SU(2) generators T^a in the fundamental 2:
    
        Tr(T^a T^b) = (1/2) Î´^{ab}
    
    So for any single generator:
        Tr(TÂ²) = 1/2


Step 3: Find the normalization factor
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    We want Tr(Y_normÂ²) = 1/2 (same as SU(2) generators)
    
    If Y_norm = k Ã— Y, then:
        Tr(Y_normÂ²) = kÂ² Ã— Tr(YÂ²) = kÂ² Ã— (5/6)
    
    Setting this equal to 1/2:
        kÂ² Ã— (5/6) = 1/2
        kÂ² = 3/5
        k = âˆš(3/5)


Step 4: The normalized hypercharge
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    Y_GUT = âˆš(3/5) Ã— Y_SM
    
    Or equivalently, the GUT-normalized coupling is:
    
        gâ‚ = âˆš(5/3) Ã— g_Y
    
    where g_Y is the SM hypercharge coupling.


VERIFICATION:
    
    Tr(Y_GUTÂ²) = (3/5) Ã— (5/6) = 1/2  âœ“
    
    This matches the SU(2) normalization convention.  â–¡
"""


def compute_hypercharge_normalization():
    """Compute the hypercharge normalization factor."""
    
    print("\n" + "="*70)
    print("COMPUTING HYPERCHARGE NORMALIZATION")
    print("="*70)
    
    # Hypercharge eigenvalues in the fundamental 5
    Y_5 = [Fraction(-1,3), Fraction(-1,3), Fraction(-1,3), 
           Fraction(1,2), Fraction(1,2)]
    
    print("\nHypercharge generator in fundamental 5:")
    print(f"  Y = diag{tuple(Y_5)}")
    
    # Compute Tr(YÂ²)
    Tr_Y2 = sum(y**2 for y in Y_5)
    print(f"\n  Tr(YÂ²) = Î£áµ¢ Yáµ¢Â² = {Tr_Y2} = {float(Tr_Y2):.6f}")
    
    # For SU(2), Tr(TÂ²) = 1/2 in fundamental
    Tr_T2_SU2 = Fraction(1, 2)
    print(f"\n  SU(2) normalization: Tr(TÂ²) = {Tr_T2_SU2}")
    
    # Normalization factor
    k_squared = Tr_T2_SU2 / Tr_Y2
    print(f"\n  To match: kÂ² = {Tr_T2_SU2} / {Tr_Y2} = {k_squared}")
    print(f"            kÂ² = {float(k_squared):.6f}")
    print(f"            k  = âˆš({k_squared}) = âˆš(3/5)")
    
    # The famous 5/3 factor
    factor = Fraction(5, 3)
    print(f"\n  Therefore: gâ‚Â² = (5/3) Ã— g_YÂ²")
    print(f"             gâ‚  = âˆš(5/3) Ã— g_Y")
    
    return k_squared, factor


# =============================================================================
# LEMMA 6B: UNIFIED COUPLING AT M_GUT
# =============================================================================

LEMMA_6B = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
LEMMA 6B: UNIFIED COUPLING AT THE GUT SCALE
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

ASSUMPTION (Unification):

    At the GUT scale M_U, the SU(5) symmetry is unbroken.
    
    There is a SINGLE coupling g_U for the entire SU(5).
    
    All 24 generators of SU(5) have the same coupling.


CONSEQUENCE:

    The SU(3), SU(2), and U(1) subgroup couplings are:
    
        gâ‚ƒ(M_U) = g_U     (SU(3) âŠ‚ SU(5))
        gâ‚‚(M_U) = g_U     (SU(2) âŠ‚ SU(5))
        gâ‚(M_U) = g_U     (U(1)_Y âŠ‚ SU(5), with GUT normalization)


CRITICAL POINT:

    This "mode democracy" â€” equal coupling per generator â€” 
    is automatic in a simple group.
    
    It becomes the admissibility interpretation:
    
        At unification, each enforcement mode (generator) 
        carries equal capacity weight.


FROM LEMMA 6A:

    gâ‚ = âˆš(5/3) Ã— g_Y
    
    So at unification:
        g_Y(M_U) = âˆš(3/5) Ã— g_U
        gâ‚‚(M_U) = g_U
        gâ‚ƒ(M_U) = g_U
"""


# =============================================================================
# THEOREM 6: THE WEAK MIXING ANGLE AT UNIFICATION
# =============================================================================

THEOREM_6 = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THEOREM 6: sinÂ²Î¸_W(M_U) = 3/8
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

THEOREM STATEMENT:

    If the Standard Model gauge group embeds in SU(5) with unification
    at scale M_U, then the weak mixing angle at M_U is:
    
        sinÂ²Î¸_W(M_U) = 3/8 = 0.375


PROOF:

Step 1: Definition of sinÂ²Î¸_W
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    sinÂ²Î¸_W = g'Â² / (g'Â² + gÂ²)
    
    where:
    â€¢ g' = U(1)_Y coupling (SM normalization)
    â€¢ g  = SU(2)_L coupling


Step 2: Apply GUT relations at M_U
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    From Lemma 6B:
        gâ‚‚(M_U) = g_U
        g_Y(M_U) = âˆš(3/5) Ã— g_U

    So:
        g'Â² = g_YÂ² = (3/5) Ã— g_UÂ²
        gÂ²  = gâ‚‚Â² = g_UÂ²


Step 3: Compute sinÂ²Î¸_W
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    sinÂ²Î¸_W(M_U) = g'Â² / (g'Â² + gÂ²)
                 = [(3/5) g_UÂ²] / [(3/5) g_UÂ² + g_UÂ²]
                 = (3/5) / (3/5 + 1)
                 = (3/5) / (8/5)
                 = 3/8


RESULT:

    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚                                             â”‚
    â”‚   sinÂ²Î¸_W(M_GUT) = 3/8 = 0.375             â”‚
    â”‚                                             â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

This is a GROUP-THEORETIC prediction, not a parameter fit.  â–¡
"""


def compute_weinberg_angle():
    """Compute the weak mixing angle at the GUT scale."""
    
    print("\n" + "="*70)
    print("COMPUTING sinÂ²Î¸_W AT GUT SCALE")
    print("="*70)
    
    # From Lemma 6A: g_YÂ² = (3/5) g_UÂ²
    g_Y_squared_ratio = Fraction(3, 5)  # g_YÂ² / g_UÂ²
    g_2_squared_ratio = Fraction(1, 1)  # g_2Â² / g_UÂ² = 1
    
    print("\nAt unification (M_U):")
    print(f"  g_YÂ² / g_UÂ² = {g_Y_squared_ratio}")
    print(f"  g_2Â² / g_UÂ² = {g_2_squared_ratio}")
    
    # sinÂ²Î¸_W = g_YÂ² / (g_YÂ² + g_2Â²)
    numerator = g_Y_squared_ratio
    denominator = g_Y_squared_ratio + g_2_squared_ratio
    sin2_theta_W = numerator / denominator
    
    print(f"\n  sinÂ²Î¸_W = g_YÂ² / (g_YÂ² + g_2Â²)")
    print(f"          = {numerator} / ({g_Y_squared_ratio} + {g_2_squared_ratio})")
    print(f"          = {numerator} / {denominator}")
    print(f"          = {sin2_theta_W}")
    print(f"          = {float(sin2_theta_W):.6f}")
    
    print(f"\n  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”")
    print(f"  â”‚  sinÂ²Î¸_W(M_GUT) = 3/8 = 0.375      â”‚")
    print(f"  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜")
    
    return sin2_theta_W


# =============================================================================
# ADMISSIBILITY INTERPRETATION
# =============================================================================

ADMISSIBILITY_INTERPRETATION = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
ADMISSIBILITY INTERPRETATION
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

IN STANDARD PHYSICS:

    sinÂ²Î¸_W is "just" a coupling ratio.
    The value 3/8 at M_GUT is "just" group theory.


IN ADMISSIBILITY PHYSICS:

    sinÂ²Î¸_W is a CAPACITY ALLOCATION RATIO.
    
    The electroweak sector has two enforcement channels:
    
    1. SU(2)_L (weak isospin): 3 generators
       â†’ Enforces distinctions like (u,d), (Î½,e)
       
    2. U(1)_Y (hypercharge): 1 generator
       â†’ Enforces electric-charge-related distinctions
    
    The mixing angle measures:
    
        sinÂ²Î¸_W = (hypercharge enforcement capacity)
                  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
                  (total electroweak enforcement capacity)


WHY 3/8?

    At unification, "mode democracy" holds:
    
    â€¢ Each SU(5) generator carries equal enforcement weight
    â€¢ The 24 generators split: 8 (SU(3)) + 3 (SU(2)) + 1 (U(1)_Y) + 12 (broken)
    
    For the electroweak 3+1 = 4 generators:
    
    â€¢ U(1)_Y has effective weight 3/5 (from normalization)
    â€¢ SU(2) has weight 1 per generator Ã— 3 generators
    
    Total EW capacity: (3/5) + 3 = 3/5 + 15/5 = 18/5
    
    Wait, that's not quite right. Let me recalculate...
    
    Actually, the mixing angle is:
    
        sinÂ²Î¸_W = g_YÂ² / (g_YÂ² + g_2Â²)
        
    This measures the HYPERCHARGE FRACTION of the combined EW coupling.
    
    At unification with g_YÂ² = (3/5)g_UÂ² and g_2Â² = g_UÂ²:
    
        Hypercharge capacity: 3/5
        Isospin capacity: 1 (= 5/5)
        Total: 8/5
        
        Ratio: (3/5) / (8/5) = 3/8


THE PHYSICAL MEANING:

    At the GUT scale:
    
    â€¢ 3/8 of electroweak enforcement goes to hypercharge modes
    â€¢ 5/8 of electroweak enforcement goes to isospin modes
    
    This is a STRUCTURAL partition, not a dynamical accident.


WHAT CHANGES AT LOW ENERGY:

    RG running changes the effective capacity allocation:
    
    â€¢ SU(2) coupling runs differently than U(1)
    â€¢ At M_Z: sinÂ²Î¸_W â‰ˆ 0.231 (not 0.375)
    
    The 3/8 â†’ 0.231 evolution is the "capacity renormalization" 
    as one moves from GUT-scale enforcement to low-energy enforcement.
"""


# =============================================================================
# WHAT THIS ACHIEVES
# =============================================================================

ACHIEVEMENT = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
WHAT THEOREM 6 ACHIEVES
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

DERIVED (from GUT embedding + normalization):

    âœ“ The GUT-normalized hypercharge: gâ‚ = âˆš(5/3) g_Y
    âœ“ The unification-scale mixing angle: sinÂ²Î¸_W(M_U) = 3/8
    âœ“ This is a GROUP-THEORETIC result, not numerology


ADMISSIBILITY CONTRIBUTION:

    âœ“ Interpretation: sinÂ²Î¸_W = capacity partition ratio
    âœ“ "Mode democracy" at unification = equal enforcement per generator
    âœ“ The 3/8 is a structural allocation, not a coincidence


NOT YET DERIVED:

    âœ— sinÂ²Î¸_W(M_Z) â‰ˆ 0.231 (requires RG running)
    âœ— The GUT scale M_U itself (â‰ˆ 10Â¹â¶ GeV)
    âœ— Why SU(5) specifically (vs SO(10), Eâ‚†, etc.)
    âœ— Threshold corrections at M_U


THE LOGIC CHAIN:

    Theorem 5.5: Y is a generator of SU(5)
                 â†’ Y has FIXED normalization
                 
    Theorem 6:   At unification, gâ‚ = gâ‚‚ = g_U (mode democracy)
                 â†’ sinÂ²Î¸_W(M_U) = 3/8
                 
    This is the FIRST NUMERICAL PREDICTION of the framework
    that doesn't come from numerology.
"""


# =============================================================================
# COMPARISON WITH EXPERIMENT
# =============================================================================

COMPARISON = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
COMPARISON WITH EXPERIMENT
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

PREDICTION:
    sinÂ²Î¸_W(M_GUT) = 3/8 = 0.375

OBSERVED (at M_Z â‰ˆ 91 GeV):
    sinÂ²Î¸_W(M_Z) â‰ˆ 0.231

THE GAP:
    0.375 â†’ 0.231 requires RG running from M_GUT to M_Z


CONSISTENCY CHECK:

    The SM RG equations give:
    
        sinÂ²Î¸_W(Î¼) â‰ˆ 3/8 Ã— [1 - (Î±_GUT/2Ï€) Ã— b Ã— log(M_GUT/Î¼)]
    
    where b depends on the matter content.
    
    Running from M_GUT ~ 10Â¹â¶ GeV down to M_Z ~ 10Â² GeV:
    
        14 orders of magnitude of running
        â†’ sinÂ²Î¸_W drops from 0.375 to ~0.21-0.23
    
    The OBSERVED value 0.231 is CONSISTENT with GUT unification
    (within experimental + theoretical uncertainties).


HISTORICAL NOTE:

    This was one of the great successes of SU(5) GUTs:
    
    â€¢ Predicted sinÂ²Î¸_W â‰ˆ 0.21 (1974, before precise measurements)
    â€¢ Observed sinÂ²Î¸_W â‰ˆ 0.23 (LEP, 1990s)
    
    The discrepancy is small and can be accounted for by:
    â€¢ SUSY threshold corrections
    â€¢ GUT threshold corrections
    â€¢ Higher-dimension operators
"""


# =============================================================================
# SUMMARY
# =============================================================================

SUMMARY = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THEOREM 6: SUMMARY
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                                                                     â”‚
â”‚  THEOREM 6: Electroweak Mixing from Unification                    â”‚
â”‚                                                                     â”‚
â”‚  GIVEN:                                                            â”‚
â”‚    â€¢ G_SM âŠ‚ SU(5) (from Theorem 5.5)                              â”‚
â”‚    â€¢ Unified coupling at M_GUT (mode democracy)                    â”‚
â”‚                                                                     â”‚
â”‚  DERIVED:                                                          â”‚
â”‚    â€¢ gâ‚ = âˆš(5/3) Ã— g_Y  (hypercharge normalization)               â”‚
â”‚    â€¢ sinÂ²Î¸_W(M_GUT) = 3/8 = 0.375                                 â”‚
â”‚                                                                     â”‚
â”‚  ADMISSIBILITY INTERPRETATION:                                     â”‚
â”‚    â€¢ sinÂ²Î¸_W = capacity partition between EW channels             â”‚
â”‚    â€¢ 3/8 to hypercharge, 5/8 to isospin                           â”‚
â”‚    â€¢ "Mode democracy" = equal enforcement per generator            â”‚
â”‚                                                                     â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                     â”‚
â”‚  THIS IS THE FIRST STRUCTURAL NUMBER IN THE FRAMEWORK              â”‚
â”‚                                                                     â”‚
â”‚  It comes from:                                                    â”‚
â”‚    1. SU(5) embedding (Theorem 5.5)                               â”‚
â”‚    2. Generator normalization (group theory)                       â”‚
â”‚    3. Unification (single coupling at M_GUT)                       â”‚
â”‚                                                                     â”‚
â”‚  NOT from numerology or parameter fitting.                         â”‚
â”‚                                                                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
"""


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("THEOREM 6: ELECTROWEAK MIXING FROM CAPACITY PARTITION")
    print("="*70)
    
    print(SETUP)
    print(DEFINITIONS)
    print(LEMMA_6A)
    
    compute_hypercharge_normalization()
    
    print(LEMMA_6B)
    print(THEOREM_6)
    
    compute_weinberg_angle()
    
    print(ADMISSIBILITY_INTERPRETATION)
    print(ACHIEVEMENT)
    print(COMPARISON)
    print(SUMMARY)


if __name__ == "__main__":
    main()

"""
THEOREM 4 (CORRECTED): MINIMAL ANOMALY-FREE CHIRAL GAUGE NET

Three critical corrections from referee feedback:

PROBLEM 1: Hypercharge assignments are INPUT, not derived
    Previous version assumed Y_Q = 1/6, Y_L = -1/2
    This is SM input, not admissibility output

PROBLEM 2: Lemma 4A logic is flawed
    U(1) theories exist (QED!) - cannot eliminate them
    Need: "confinement needed for robust records" not "U(1) inadmissible"

PROBLEM 3: Uniqueness not proven
    Elimination table incomplete (Sp(n), exceptional groups, etc.)
    Cost functional too crude (dim alone)

This version gives HONEST accounting of what is actually derived.
"""

# =============================================================================
# CORRECTED THEOREM STATEMENT
# =============================================================================

CORRECTED_STATEMENT = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THEOREM 4 (CORRECTED): What Is Actually Derived
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

ESTABLISHED (from Theorems 2-3):
    G = âˆáµ¢ SU(náµ¢) Ã— U(1)^m  (general form)


THEOREM 4A (Conditional):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    IF we assume:
    (i)   Chiral electroweak structure SU(2)_L Ã— U(1)_Y
    (ii)  Standard electric charge quantization (Q = Tâ‚ƒ + Y)
    (iii) Anomaly cancellation (quantum consistency)
    (iv)  Minimal additional structure
    
    THEN:
    The color sector must have multiplicity N_c = 3.
    
    The minimal confining realization is SU(3).


THEOREM 4B (Robust Records):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    For robust classical record formation at finite capacity:
    
    At least one CONFINING sector is required.
    
    Confinement provides:
    - Stable, localized bound-state encodings
    - Redundant record storage in hadron structure  
    - Screening of long-range enforcement spillover


THEOREM 4C (Partial Uniqueness):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Among gauge groups of the form SU(N_c) Ã— SU(2) Ã— U(1) with:
    - Standard charge quantization
    - One generation of chiral fermions
    - Anomaly freedom
    
    The value N_c = 3 is UNIQUE.
    
    Larger groups (SU(4), SU(5), ...) require:
    - Different charge assignments, OR
    - Additional matter content, OR
    - Higher enforcement cost


WHAT IS NOT DERIVED:
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    âœ— Why SU(2) Ã— U(1) specifically (vs other chiral structures)
    âœ— Electric charge quantization (why Q_e = -1, Q_u = +2/3, etc.)
    âœ— Why chiral (vs vectorlike)
    âœ— Full uniqueness among ALL possible gauge groups
"""


# =============================================================================
# LEMMA 4A (CORRECTED): Confinement for Robust Records
# =============================================================================

LEMMA_4A_CORRECTED = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
LEMMA 4A (CORRECTED): Confinement Required for Robust Records
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

âš ï¸ PREVIOUS (INCORRECT) CLAIM:
    "U(1)^m alone violates saturation stability"
    
    This was wrong because:
    - QED exists and is perfectly consistent
    - "Enforcement load scaling" was not rigorously defined
    - Long-range forces don't make a theory "inadmissible"


CORRECTED CLAIM:
    At least one CONFINING sector is required for robust classical 
    record formation under finite capacity constraints.


ARGUMENT (weaker but defensible):

1. CLASSICAL RECORDS require stable, distinguishable configurations.
   Under A4, records must persist once formed.

2. ABELIAN THEORIES (U(1)) have:
   - Long-range (1/r) fields
   - Charges that can be arbitrarily separated
   - No intrinsic scale for localization
   - Fragile record encoding (perturbations propagate to infinity)

3. CONFINING THEORIES provide:
   - Bound states (hadrons) as stable composite objects
   - Intrinsic scale (Î›_QCD) for localization
   - Redundant encoding in bound-state structure
   - Robust records: perturbing a hadron doesn't affect distant records

4. For ROBUST record formation at FINITE capacity:
   - Need localized, stable configurations
   - Confinement naturally provides this
   - Pure U(1) does not (though U(1) can coexist WITH confining sector)

âš ï¸ NOTE: This does NOT say U(1) is inadmissible.
         It says U(1) ALONE is insufficient for robust records.
         The SM has BOTH: U(1)_EM for long-range AND SU(3) for confinement.


CONCLUSION:
    At least one confining sector (SU(n) with appropriate matter) 
    is required for robust classical record formation.
    
    This is a PHYSICAL argument, not a mathematical theorem.  â–¡
"""


# =============================================================================
# LEMMA 4C (CORRECTED): N_c = 3 is Conditional
# =============================================================================

LEMMA_4C_CORRECTED = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
LEMMA 4C (CORRECTED): N_c = 3 Given Standard Charges
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

âš ï¸ PREVIOUS (OVERCLAIMED):
    "Anomaly admissibility forces N_c = 3"
    
    This smuggled in the Standard Model hypercharges as input.


CORRECTED STATEMENT:

THEOREM: Given standard electric charge quantization, anomaly 
         cancellation in a minimal chiral electroweak theory 
         requires the color multiplicity N_c = 3.


SETUP (STATED AS ASSUMPTIONS):

    (A1) Gauge group: G = SU(N_c) Ã— SU(2)_L Ã— U(1)_Y
    
    (A2) Electric charge formula: Q = Tâ‚ƒ + Y
         (This is the standard electroweak embedding)
    
    (A3) Observed charges:
         - Electron: Q_e = -1
         - Up quark: Q_u = +2/3
         - Down quark: Q_d = -1/3
         
    (A4) Minimal chiral matter: one generation of
         - Quark doublet Q_L
         - Lepton doublet L
         - Right-handed singlets u_R, d_R, e_R


DERIVATION:

Step 1: Hypercharges from charge formula (A2) + observations (A3)
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    For lepton doublet L = (Î½, e)_L:
        Q_Î½ = 0 = +1/2 + Y_L  â†’  Y_L could be -1/2
        Q_e = -1 = -1/2 + Y_L  â†’  Y_L = -1/2  âœ“ (consistent)
    
    For quark doublet Q = (u, d)_L:
        Q_u = +2/3 = +1/2 + Y_Q  â†’  Y_Q = +1/6
        Q_d = -1/3 = -1/2 + Y_Q  â†’  Y_Q = +1/6  âœ“ (consistent)

    âš ï¸ These hypercharges are DERIVED from observed electric charges.
       The observed charges are INPUT.


Step 2: [SU(2)]Â²[U(1)] anomaly cancellation
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    A = Î£_{doublets} (multiplicity Ã— hypercharge) = 0
    
    A = N_c Ã— Y_Q + 1 Ã— Y_L = 0
    A = N_c Ã— (1/6) + (-1/2) = 0
    
    âŸ¹ N_c = 3


Step 3: Verification
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    With N_c = 3, all SM anomalies cancel. [Standard textbook result]


HONEST ASSESSMENT:
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

WHAT IS DERIVED:
    âœ“ N_c = 3 follows from anomaly cancellation
    
WHAT IS ASSUMED (not derived from admissibility):
    âœ— SU(2)_L Ã— U(1)_Y electroweak structure
    âœ— Q = Tâ‚ƒ + Y charge formula
    âœ— Electron charge = -1
    âœ— Quark charges = +2/3, -1/3
    âœ— Chiral (not vectorlike) matter
    âœ— One generation structure

THE REAL THEOREM IS:
    "SM charge quantization + anomaly freedom âŸ¹ N_c = 3"
    
    This is CONDITIONAL, not absolute.  â–¡
"""


# =============================================================================
# LEMMA 4D (CORRECTED): Incomplete Uniqueness
# =============================================================================

LEMMA_4D_CORRECTED = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
LEMMA 4D (CORRECTED): Partial Elimination, Not Full Uniqueness
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

âš ï¸ PREVIOUS (OVERCLAIMED):
    "SU(3) Ã— SU(2) Ã— U(1) is the UNIQUE minimal solution"
    
    This was incomplete. Not all alternatives were checked.


WHAT WAS NOT ADEQUATELY ADDRESSED:

    (1) Symplectic groups: Sp(2) â‰… SU(2), but Sp(4), Sp(6)?
    
    (2) Exceptional groups: Gâ‚‚, Fâ‚„, Eâ‚†, Eâ‚‡, Eâ‚ˆ
        Some appear in GUT constructions (Eâ‚† especially)
    
    (3) Vectorlike constructions: Anomaly-free without chirality
        These exist and can confine
    
    (4) Technicolor variants: SU(N_TC) replacing Higgs
    
    (5) Different charge quantizations:
        Non-standard hypercharge assignments exist that are anomaly-free


CORRECTED STATEMENT:

THEOREM (Partial):
    Among gauge groups of the specific form
        G = SU(N_c) Ã— SU(2) Ã— U(1)
    with:
    - Standard electric charge quantization
    - Minimal chiral fermion content (one generation)
    - All gauge anomalies cancelled
    
    The value N_c = 3 is uniquely determined.


WHAT THIS DOES NOT PROVE:

    âœ— That SU(N_c) Ã— SU(2) Ã— U(1) is the only viable structure
    âœ— That chiral is required (vectorlike theories exist)
    âœ— That standard charges are required
    âœ— That exceptional groups are excluded
    âœ— Full uniqueness among all gauge theories


MORE COMPLETE ELIMINATION WOULD REQUIRE:

    (1) Cost functional including:
        - Generator count dim(G)
        - Matter representation burden |R|
        - Number of anomaly conditions
        - Confinement scale behavior
        - Coupling unification properties
    
    (2) Systematic check of:
        - All compact simple Lie groups
        - All products up to some dimension
        - All chiral representations
        - All anomaly-free combinations
    
    This is a significant research program, not done here.


HONEST CONCLUSION:

    Within the restricted class:
        SU(N_c) Ã— SU(2) Ã— U(1) with SM charges
    
    The choice N_c = 3 is forced by anomaly cancellation.
    
    Full uniqueness among ALL gauge theories is NOT established.  â–¡
"""


# =============================================================================
# WHAT IS ACTUALLY DERIVED (HONEST ACCOUNTING)
# =============================================================================

HONEST_ACCOUNTING = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
HONEST ACCOUNTING: WHAT THEOREM 4 ACTUALLY ACHIEVES
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

FULLY DERIVED FROM A1-A4 (Theorems 2-3):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    âœ“ Gauge theory exists
    âœ“ Gauge group is compact Lie group
    âœ“ Form: G = âˆáµ¢ SU(náµ¢) Ã— U(1)^m (from C*-algebra automorphisms)
    âœ“ Non-abelian factors exist (from A2: non-closure)
    âœ“ Principal bundle + connection structure (from A4: locality)


DERIVED WITH PHYSICAL ASSUMPTIONS (Theorem 4A):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    âš  Need confining sector for robust records
      ASSUMPTION: "Robust classical records" require localized stable states
      PHYSICS: Confinement provides this; pure U(1) does not suffice alone


DERIVED CONDITIONALLY (Theorem 4C):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Given:
    - SU(N_c) Ã— SU(2) Ã— U(1) structure  [ASSUMED]
    - Standard charge quantization       [ASSUMED]
    - Chiral matter content             [ASSUMED]
    - Anomaly cancellation              [DERIVED from consistency]
    
    Then: N_c = 3  [DERIVED from arithmetic]


NOT DERIVED (remain as inputs or open questions):
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    âœ— Why SU(2) Ã— U(1) electroweak (vs SU(3) Ã— U(1), etc.)
    âœ— Why Q = Tâ‚ƒ + Y (charge formula)
    âœ— Why Q_e = -1, Q_u = +2/3, Q_d = -1/3 (observed charges)
    âœ— Why chiral matter (vs vectorlike)
    âœ— Why this generation structure
    âœ— Why not exceptional groups
    âœ— Full uniqueness proof


â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THE CORRECT CLAIM
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

THEOREM 4 (Corrected):

    (a) Admissibility (A1-A4) derives GAUGE THEORY with compact 
        gauge group G = âˆ SU(náµ¢) Ã— U(1)^m.
        
    (b) Robust classical records favor at least one CONFINING sector.
    
    (c) Given the Standard Model structure SU(N_c) Ã— SU(2) Ã— U(1)
        with standard charge quantization, anomaly cancellation 
        UNIQUELY determines N_c = 3.
        
    (d) Full uniqueness of SM among all gauge theories is NOT proven.


WHAT THIS MEANS:

    The framework CONSTRAINS but does not UNIQUELY DETERMINE the SM.
    
    If you input "electroweak structure + observed charges", 
    you get "3 colors" as output.
    
    But the electroweak structure itself is not derived from A1-A4.
"""


# =============================================================================
# OPEN QUESTIONS FOR FUTURE WORK
# =============================================================================

OPEN_QUESTIONS = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
OPEN QUESTIONS: What Would Complete the Derivation
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

To derive the FULL SM gauge group from admissibility alone, 
we would need to address:


Q1: WHY SU(2) Ã— U(1) ELECTROWEAK?
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Why not SU(3) Ã— U(1)? Or SU(2) Ã— SU(2) Ã— U(1)?
    
    Possible approaches:
    - Minimality of chiral structure
    - Anomaly freedom with minimal matter
    - Connection to spacetime symmetry (spin-statistics)
    
    STATUS: Open


Q2: WHY THESE CHARGES?
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Why Q_e = -1 (not -2 or -1/2)?
    Why Q_u = +2/3, Q_d = -1/3 (not other fractions)?
    
    Possible approaches:
    - GUT embedding (SU(5) or SO(10) quantizes charges)
    - Anomaly cancellation with multiple generations
    - Magnetic monopole quantization (Dirac)
    
    STATUS: Requires additional structure (GUT or gravity)


Q3: WHY CHIRAL?
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Why not vectorlike matter (L and R identical under gauge group)?
    
    Possible approaches:
    - Connection to A4 (irreversibility requires asymmetry)
    - Parity violation as fundamental
    - Relation to arrow of time
    
    STATUS: Plausible connection to A4, not proven


Q4: FULL UNIQUENESS?
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Is SM the unique solution, or one of several?
    
    Would need:
    - Complete scan of all compact Lie groups
    - All chiral representations
    - All anomaly-free combinations
    - Rigorous cost functional
    
    STATUS: Major research program


Q5: NUMBER OF GENERATIONS?
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    Why 3 generations? (Not addressed at all in current work)
    
    Possible approaches:
    - Topology of extra dimensions
    - Index theorems
    - Anomaly cancellation with gravity
    
    STATUS: Completely open
"""


# =============================================================================
# SUMMARY
# =============================================================================

SUMMARY = """
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THEOREM 4 (CORRECTED): SUMMARY
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                                                                     â”‚
â”‚  WHAT IS RIGOROUSLY DERIVED:                                       â”‚
â”‚                                                                     â”‚
â”‚  From A1-A4:                                                       â”‚
â”‚      G = âˆ SU(náµ¢) Ã— U(1)^m  (general form of gauge group)         â”‚
â”‚                                                                     â”‚
â”‚  From physical argument:                                           â”‚
â”‚      Need at least one confining sector for robust records         â”‚
â”‚                                                                     â”‚
â”‚  From SM structure + anomaly cancellation:                         â”‚
â”‚      N_c = 3  (conditional on assuming SM electroweak)             â”‚
â”‚                                                                     â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                     â”‚
â”‚  WHAT IS ASSUMED (not derived):                                    â”‚
â”‚                                                                     â”‚
â”‚      â€¢ SU(2) Ã— U(1) electroweak structure                         â”‚
â”‚      â€¢ Standard electric charge quantization                       â”‚
â”‚      â€¢ Chiral matter content                                       â”‚
â”‚      â€¢ One-generation structure                                    â”‚
â”‚                                                                     â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                     â”‚
â”‚  HONEST CONCLUSION:                                                â”‚
â”‚                                                                     â”‚
â”‚  "Given the Standard Model framework, N_c = 3 is forced."          â”‚
â”‚                                                                     â”‚
â”‚  NOT:                                                              â”‚
â”‚  "Admissibility uniquely determines the Standard Model."           â”‚
â”‚                                                                     â”‚
â”‚  The latter would require deriving:                                â”‚
â”‚      â€¢ Electroweak structure from A1-A4                           â”‚
â”‚      â€¢ Charge quantization from A1-A4                             â”‚
â”‚      â€¢ Chirality from A1-A4                                       â”‚
â”‚      â€¢ Full uniqueness proof                                       â”‚
â”‚                                                                     â”‚
â”‚  These remain open problems.                                       â”‚
â”‚                                                                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
"""


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("THEOREM 4 (CORRECTED): HONEST ACCOUNTING")
    print("What is actually derived vs assumed")
    print("=" * 70)
    
    print(CORRECTED_STATEMENT)
    print(LEMMA_4A_CORRECTED)
    print(LEMMA_4C_CORRECTED)
    print(LEMMA_4D_CORRECTED)
    print(HONEST_ACCOUNTING)
    print(OPEN_QUESTIONS)
    print(SUMMARY)


if __name__ == "__main__":
    main()

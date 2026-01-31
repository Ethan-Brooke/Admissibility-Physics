"""
THEOREM 5: MINIMAL ANOMALY-FREE CHIRAL MATTER COMPLETION (CORRECTED)

The [U(1)]Â³ anomaly calculation needs careful attention to the 
left-handed vs right-handed conventions.

KEY INSIGHT: Right-handed fermions contribute with OPPOSITE hypercharge
when written as left-handed fields (u_R â†’ u_R^c with Y â†’ -Y).
"""

import sympy as sp
from sympy import symbols, Eq, solve, simplify, Rational, sqrt, Integer
from fractions import Fraction

# =============================================================================
# CORRECT ANOMALY FORMULAS
# =============================================================================

def compute_anomalies_correctly():
    """
    Compute anomalies with CORRECT conventions.
    
    Convention: All anomalies are computed for LEFT-HANDED Weyl fermions.
    
    The SM fields as left-handed Weyl fermions:
    
    DOUBLETS (left-handed):
        Q_L = (3, 2)_{Y_Q}    : 3 colors Ã— 2 weak = 6 components
        L   = (1, 2)_{Y_L}    : 1 Ã— 2 = 2 components
    
    SINGLETS (right-handed, so count as left-handed with OPPOSITE Y):
        u_R â†’ (u_R)^c = (3Ì„, 1)_{-Y_u}  : 3 components
        d_R â†’ (d_R)^c = (3Ì„, 1)_{-Y_d}  : 3 components
        e_R â†’ (e_R)^c = (1, 1)_{-Y_e}  : 1 component
    
    Total: 6 + 2 + 3 + 3 + 1 = 15 left-handed Weyl fermions per generation.
    """
    
    print("="*70)
    print("THEOREM 5: ANOMALY CALCULATION (CORRECTED)")
    print("="*70)
    
    # Symbols
    Y_Q, Y_L, Y_u, Y_d, Y_e = symbols('Y_Q Y_L Y_u Y_d Y_e', real=True)
    N_c = symbols('N_c', positive=True, integer=True)
    
    print("\n" + "-"*70)
    print("CONVENTIONS")
    print("-"*70)
    print("""
    All anomalies computed for LEFT-HANDED Weyl fermions.
    
    Right-handed fields (u_R, d_R, e_R) are written as left-handed
    conjugates with OPPOSITE hypercharge:
    
        Ïˆ_R with Y  â†’  (Ïˆ_R)^c with -Y
    
    So in anomaly sums:
        u_R contributes with Y = -Y_u (not +Y_u)
        d_R contributes with Y = -Y_d
        e_R contributes with Y = -Y_e
    """)
    
    # =========================================================================
    # [SU(2)]Â²[U(1)] anomaly
    # =========================================================================
    print("\n" + "-"*70)
    print("[SU(2)]Â²[U(1)] ANOMALY")
    print("-"*70)
    
    print("""
    Sum over SU(2) DOUBLETS only:
    
        A = Î£ (color multiplicity) Ã— Y
        
        Q_L: N_c doublets with Y = Y_Q
        L:   1 doublet with Y = Y_L
        
        A = N_c Ã— Y_Q + 1 Ã— Y_L
    """)
    
    A_SU2_U1 = N_c * Y_Q + Y_L
    print(f"    A_[SU(2)]Â²[U(1)] = {A_SU2_U1} = 0")
    
    # =========================================================================
    # [SU(N_c)]Â²[U(1)] anomaly
    # =========================================================================
    print("\n" + "-"*70)
    print("[SU(N_c)]Â²[U(1)] ANOMALY")
    print("-"*70)
    
    print("""
    Sum over SU(N_c) fundamentals and antifundamentals:
    
        Fundamentals (N_c): contribute +Y
        Antifundamentals (NÌ„_c): contribute -Y  (or +Y for the conjugate)
    
    Left-handed fields in N_c:
        Q_L: (N_c, 2) with Y_Q, contributes 2 Ã— Y_Q (2 for weak doublet)
        
    Left-handed fields in NÌ„_c (from right-handed N_c):
        (u_R)^c: (NÌ„_c, 1) with -Y_u, contributes 1 Ã— (-Y_u)
        (d_R)^c: (NÌ„_c, 1) with -Y_d, contributes 1 Ã— (-Y_d)
    
    For [SU(N)]Â²[U(1)], T(N) = T(NÌ„) = 1/2, so:
        A = T(N) Ã— (2 Y_Q) + T(NÌ„) Ã— (-Y_u) + T(NÌ„) Ã— (-Y_d)
        A = 1/2 Ã— (2 Y_Q - Y_u - Y_d)
        
    Setting A = 0:
        2 Y_Q - Y_u - Y_d = 0
    """)
    
    A_SUNc_U1 = 2*Y_Q - Y_u - Y_d
    print(f"    A_[SU(N_c)]Â²[U(1)] âˆ {A_SUNc_U1} = 0")
    
    # =========================================================================
    # [U(1)]Â³ anomaly
    # =========================================================================
    print("\n" + "-"*70)
    print("[U(1)]Â³ ANOMALY")
    print("-"*70)
    
    print("""
    Sum of YÂ³ over all LEFT-HANDED Weyl fermions:
    
    From Q_L (left-handed, Y = Y_Q):
        N_c colors Ã— 2 weak components Ã— Y_QÂ³ = 2 N_c Y_QÂ³
        
    From L (left-handed, Y = Y_L):
        1 Ã— 2 Ã— Y_LÂ³ = 2 Y_LÂ³
        
    From (u_R)^c (left-handed conjugate, Y = -Y_u):
        N_c Ã— 1 Ã— (-Y_u)Â³ = -N_c Y_uÂ³
        
    From (d_R)^c (left-handed conjugate, Y = -Y_d):
        N_c Ã— 1 Ã— (-Y_d)Â³ = -N_c Y_dÂ³
        
    From (e_R)^c (left-handed conjugate, Y = -Y_e):
        1 Ã— 1 Ã— (-Y_e)Â³ = -Y_eÂ³
    
    Total:
        A = 2 N_c Y_QÂ³ + 2 Y_LÂ³ - N_c Y_uÂ³ - N_c Y_dÂ³ - Y_eÂ³
    """)
    
    A_U1_cubed = 2*N_c*Y_Q**3 + 2*Y_L**3 - N_c*Y_u**3 - N_c*Y_d**3 - Y_e**3
    print(f"    A_[U(1)]Â³ = {A_U1_cubed} = 0")
    
    # =========================================================================
    # [grav]Â²[U(1)] anomaly
    # =========================================================================
    print("\n" + "-"*70)
    print("[grav]Â²[U(1)] ANOMALY")
    print("-"*70)
    
    print("""
    Sum of Y over all left-handed Weyl fermions:
    
        A = 2 N_c Y_Q + 2 Y_L - N_c Y_u - N_c Y_d - Y_e
    """)
    
    A_grav = 2*N_c*Y_Q + 2*Y_L - N_c*Y_u - N_c*Y_d - Y_e
    print(f"    A_[grav]Â²[U(1)] = {A_grav} = 0")
    
    return A_SU2_U1, A_SUNc_U1, A_U1_cubed, A_grav


def solve_for_SM():
    """
    Solve the anomaly system step by step.
    """
    
    print("\n" + "="*70)
    print("SOLVING THE ANOMALY SYSTEM")
    print("="*70)
    
    Y_Q, Y_L, Y_u, Y_d, Y_e = symbols('Y_Q Y_L Y_u Y_d Y_e', real=True)
    N_c = symbols('N_c', positive=True, integer=True)
    
    # =========================================================================
    # Step 1: Physical constraints
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 1: Physical constraints (INPUT)")
    print("-"*70)
    
    print("""
    INPUT (from observed physics):
    
    1. Neutrino is electrically neutral:
       Q(Î½) = Tâ‚ƒ(Î½) + Y_L = +1/2 + Y_L = 0
       âŸ¹ Y_L = -1/2
       
    2. Electron has charge -1:
       Q(e_R) = Y_e  (singlet, Tâ‚ƒ = 0)
       Since e_R has the same charge as the electron: Y_e = -1
       
       Wait - e_R is right-handed. As a left-handed field, (e_R)^c has Y = -Y_e.
       But the physical charge is still -1.
       
       Actually: Q(Ïˆ) = Tâ‚ƒ + Y for the PARTICLE, regardless of chirality.
       For e_R (right-handed electron): Q = 0 + Y_e = -1, so Y_e = -1 âœ“
    """)
    
    Y_L_val = Rational(-1, 2)
    Y_e_val = Integer(-1)
    
    print(f"    Y_L = {Y_L_val}")
    print(f"    Y_e = {Y_e_val}")
    
    # =========================================================================
    # Step 2: [SU(2)]Â²[U(1)] 
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 2: [SU(2)]Â²[U(1)] = 0")
    print("-"*70)
    
    # N_c Y_Q + Y_L = 0
    # N_c Y_Q = -Y_L = 1/2
    # Y_Q = 1/(2 N_c)
    
    print(f"    N_c Ã— Y_Q + Y_L = 0")
    print(f"    N_c Ã— Y_Q = -({Y_L_val}) = 1/2")
    print(f"    Y_Q = 1/(2 N_c)")
    
    # =========================================================================
    # Step 3: Quark charges determine Y_u, Y_d
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 3: Quark electric charges")
    print("-"*70)
    
    print("""
    For quarks in the doublet Q_L = (u_L, d_L):
        Q(u_L) = Tâ‚ƒ + Y_Q = +1/2 + Y_Q
        Q(d_L) = Tâ‚ƒ + Y_Q = -1/2 + Y_Q
    
    For right-handed quarks (singlets):
        Q(u_R) = Y_u  (must equal Q(u_L) for mass terms)
        Q(d_R) = Y_d  (must equal Q(d_L) for mass terms)
    
    So:
        Y_u = 1/2 + Y_Q = 1/2 + 1/(2N_c)
        Y_d = -1/2 + Y_Q = -1/2 + 1/(2N_c)
    """)
    
    # =========================================================================
    # Step 4: Check [SU(N_c)]Â²[U(1)]
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 4: Verify [SU(N_c)]Â²[U(1)] = 0")
    print("-"*70)
    
    print("""
    2 Y_Q - Y_u - Y_d = 0
    
    Substituting:
        Y_Q = 1/(2N_c)
        Y_u = 1/2 + 1/(2N_c)
        Y_d = -1/2 + 1/(2N_c)
    
    2 Ã— [1/(2N_c)] - [1/2 + 1/(2N_c)] - [-1/2 + 1/(2N_c)]
    = 1/N_c - 1/2 - 1/(2N_c) + 1/2 - 1/(2N_c)
    = 1/N_c - 1/N_c = 0  âœ“
    
    This is automatically satisfied!
    """)
    
    # =========================================================================
    # Step 5: [grav]Â²[U(1)] 
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 5: [grav]Â²[U(1)] = 0")
    print("-"*70)
    
    print("""
    A = 2 N_c Y_Q + 2 Y_L - N_c Y_u - N_c Y_d - Y_e = 0
    
    Substituting:
        Y_Q = 1/(2N_c), Y_L = -1/2, Y_e = -1
        Y_u = 1/2 + 1/(2N_c), Y_d = -1/2 + 1/(2N_c)
    
    A = 2 N_c Ã— [1/(2N_c)] + 2 Ã— (-1/2) 
        - N_c Ã— [1/2 + 1/(2N_c)] - N_c Ã— [-1/2 + 1/(2N_c)] - (-1)
      = 1 - 1 - N_c/2 - 1/2 + N_c/2 - 1/2 + 1
      = 1 - 1 - 1/2 - 1/2 + 1
      = 0  âœ“
    
    This is automatically satisfied for ANY N_c!
    """)
    
    # Let me verify numerically
    def check_grav(nc):
        yq = Fraction(1, 2*nc)
        yl = Fraction(-1, 2)
        ye = -1
        yu = Fraction(1,2) + Fraction(1, 2*nc)
        yd = Fraction(-1,2) + Fraction(1, 2*nc)
        return 2*nc*yq + 2*yl - nc*yu - nc*yd - ye
    
    print("    Numerical check:")
    for nc in [1, 3, 5]:
        print(f"      N_c = {nc}: A = {check_grav(nc)}")
    
    # =========================================================================
    # Step 6: [U(1)]Â³
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 6: [U(1)]Â³ = 0")
    print("-"*70)
    
    print("""
    A = 2 N_c Y_QÂ³ + 2 Y_LÂ³ - N_c Y_uÂ³ - N_c Y_dÂ³ - Y_eÂ³ = 0
    
    This is the KEY constraint that determines N_c!
    
    Substituting our expressions:
    """)
    
    def check_U1_cubed(nc):
        yq = Fraction(1, 2*nc)
        yl = Fraction(-1, 2)
        ye = -1
        yu = Fraction(1,2) + Fraction(1, 2*nc)
        yd = Fraction(-1,2) + Fraction(1, 2*nc)
        return 2*nc*yq**3 + 2*yl**3 - nc*yu**3 - nc*yd**3 - ye**3
    
    print("    Numerical evaluation for different N_c:")
    print()
    for nc in [1, 2, 3, 4, 5, 6, 7]:
        A = check_U1_cubed(nc)
        status = "âœ“" if A == 0 else ""
        print(f"      N_c = {nc}: [U(1)]Â³ = {A}  {status}")
    
    # =========================================================================
    # Step 7: Witten anomaly
    # =========================================================================
    print("\n" + "-"*70)
    print("STEP 7: Witten SU(2) anomaly")
    print("-"*70)
    
    print("""
    Number of SU(2) doublets = N_c (from Q_L) + 1 (from L) = N_c + 1
    
    Witten anomaly vanishes iff # doublets is EVEN.
    
    âŸ¹ N_c + 1 â‰¡ 0 (mod 2)
    âŸ¹ N_c is ODD
    
    Combined with [U(1)]Â³ = 0:
    """)
    
    print("    Values satisfying Witten (N_c odd) AND [U(1)]Â³ = 0:")
    found = []
    for nc in range(1, 20):
        if nc % 2 == 1:  # Witten: N_c odd
            A = check_U1_cubed(nc)
            if A == 0:
                found.append(nc)
                print(f"      N_c = {nc}  âœ“")
    
    if not found:
        print("      No solutions found for N_c â‰¤ 20!")
        print("\n    Let's check if [U(1)]Â³ can EVER be zero...")
    
    return found


def analyze_U1_cubed():
    """
    Analyze the [U(1)]Â³ anomaly more carefully.
    """
    
    print("\n" + "="*70)
    print("DETAILED ANALYSIS OF [U(1)]Â³")
    print("="*70)
    
    print("""
    We have:
        A = 2 N_c Y_QÂ³ + 2 Y_LÂ³ - N_c Y_uÂ³ - N_c Y_dÂ³ - Y_eÂ³
    
    With:
        Y_Q = 1/(2N_c)
        Y_L = -1/2
        Y_u = 1/2 + 1/(2N_c) = (N_c + 1)/(2N_c)
        Y_d = -1/2 + 1/(2N_c) = (1 - N_c)/(2N_c)
        Y_e = -1
    
    Let's compute term by term:
    
    Term 1: 2 N_c Y_QÂ³ = 2 N_c Ã— [1/(2N_c)]Â³ = 2 N_c / (8 N_cÂ³) = 1/(4 N_cÂ²)
    
    Term 2: 2 Y_LÂ³ = 2 Ã— (-1/2)Â³ = 2 Ã— (-1/8) = -1/4
    
    Term 3: -N_c Y_uÂ³ = -N_c Ã— [(N_c+1)/(2N_c)]Â³ = -N_c Ã— (N_c+1)Â³/(8N_cÂ³)
                      = -(N_c+1)Â³/(8N_cÂ²)
    
    Term 4: -N_c Y_dÂ³ = -N_c Ã— [(1-N_c)/(2N_c)]Â³ = -N_c Ã— (1-N_c)Â³/(8N_cÂ³)
                      = -(1-N_c)Â³/(8N_cÂ²) = (N_c-1)Â³/(8N_cÂ²)
    
    Term 5: -Y_eÂ³ = -(-1)Â³ = 1
    
    Total:
        A = 1/(4N_cÂ²) - 1/4 - (N_c+1)Â³/(8N_cÂ²) + (N_c-1)Â³/(8N_cÂ²) + 1
    """)
    
    # Compute symbolically
    from sympy import Symbol, expand, simplify, factor
    N = Symbol('N', positive=True, integer=True)
    
    term1 = Rational(1,4) / N**2
    term2 = Rational(-1,4)
    term3 = -(N+1)**3 / (8*N**2)
    term4 = (N-1)**3 / (8*N**2)
    term5 = 1
    
    A = term1 + term2 + term3 + term4 + term5
    A_simplified = simplify(A)
    A_expanded = expand(A_simplified)
    
    print(f"\n    Symbolic result:")
    print(f"    A = {A_simplified}")
    print(f"    A = {A_expanded}")
    
    # Note: (N+1)Â³ - (N-1)Â³ = [(N+1) - (N-1)][(N+1)Â² + (N+1)(N-1) + (N-1)Â²]
    #                       = 2 Ã— [NÂ² + 2N + 1 + NÂ² - 1 + NÂ² - 2N + 1]
    #                       = 2 Ã— [3NÂ² + 1]
    #                       = 6NÂ² + 2
    
    print("""
    
    Note: (N+1)Â³ - (N-1)Â³ = 6NÂ² + 2
    
    So terms 3+4 = [-(N+1)Â³ + (N-1)Â³]/(8NÂ²) = -(6NÂ² + 2)/(8NÂ²) = -3/4 - 1/(4NÂ²)
    
    Total:
        A = 1/(4NÂ²) - 1/4 - 3/4 - 1/(4NÂ²) + 1
          = -1/4 - 3/4 + 1
          = -1 + 1
          = 0  âœ“âœ“âœ“
    """)
    
    print("    THE [U(1)]Â³ ANOMALY VANISHES FOR ALL N_c!")
    
    # Verify numerically
    print("\n    Numerical verification:")
    for nc in [1, 3, 5, 7, 11, 13]:
        yq = Fraction(1, 2*nc)
        yl = Fraction(-1, 2)
        ye = -1
        yu = Fraction(nc+1, 2*nc)
        yd = Fraction(1-nc, 2*nc)
        A = 2*nc*yq**3 + 2*yl**3 - nc*yu**3 - nc*yd**3 - ye**3
        print(f"      N_c = {nc}: A = {A}")


def final_verification():
    """
    Final verification that N_c = 3 works.
    """
    
    print("\n" + "="*70)
    print("FINAL VERIFICATION: N_c = 3 (STANDARD MODEL)")
    print("="*70)
    
    N_c = 3
    Y_Q = Fraction(1, 6)
    Y_L = Fraction(-1, 2)
    Y_u = Fraction(2, 3)
    Y_d = Fraction(-1, 3)
    Y_e = -1
    
    print(f"\n    Hypercharges for N_c = {N_c}:")
    print(f"    Y_Q = 1/(2Ã—3) = {Y_Q}")
    print(f"    Y_L = {Y_L}")
    print(f"    Y_u = 1/2 + 1/6 = {Y_u}")
    print(f"    Y_d = -1/2 + 1/6 = {Y_d}")
    print(f"    Y_e = {Y_e}")
    
    print("\n    Anomaly check:")
    
    # [SU(2)]Â²[U(1)]
    A1 = N_c * Y_Q + Y_L
    print(f"\n    [SU(2)]Â²[U(1)] = {N_c} Ã— {Y_Q} + {Y_L} = {A1}  {'âœ“' if A1 == 0 else 'âœ—'}")
    
    # [SU(3)]Â²[U(1)]
    A2 = 2*Y_Q - Y_u - Y_d
    print(f"    [SU(3)]Â²[U(1)] = 2Ã—{Y_Q} - {Y_u} - {Y_d} = {A2}  {'âœ“' if A2 == 0 else 'âœ—'}")
    
    # [grav]Â²[U(1)]
    A3 = 2*N_c*Y_Q + 2*Y_L - N_c*Y_u - N_c*Y_d - Y_e
    print(f"    [grav]Â²[U(1)] = {A3}  {'âœ“' if A3 == 0 else 'âœ—'}")
    
    # [U(1)]Â³
    A4 = 2*N_c*Y_Q**3 + 2*Y_L**3 - N_c*Y_u**3 - N_c*Y_d**3 - Y_e**3
    print(f"    [U(1)]Â³ = {A4}  {'âœ“' if A4 == 0 else 'âœ—'}")
    
    # Witten
    n_doublets = N_c + 1
    print(f"    Witten: {n_doublets} doublets ({'even' if n_doublets%2==0 else 'odd'}) {'âœ“' if n_doublets%2==0 else 'âœ—'}")
    
    # Electric charges
    print("\n    Electric charges:")
    print(f"    Q(u) = 1/2 + {Y_Q} = {Fraction(1,2) + Y_Q}")
    print(f"    Q(d) = -1/2 + {Y_Q} = {Fraction(-1,2) + Y_Q}")
    print(f"    Q(Î½) = 1/2 + {Y_L} = {Fraction(1,2) + Y_L}")
    print(f"    Q(e) = -1/2 + {Y_L} = {Fraction(-1,2) + Y_L}")


def theorem5_conclusion():
    """
    State what Theorem 5 actually proves.
    """
    
    print("\n" + "="*70)
    print("THEOREM 5: CONCLUSION")
    print("="*70)
    
    print("""
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
THEOREM 5: MINIMAL ANOMALY-FREE CHIRAL MATTER COMPLETION
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

GIVEN:
    â€¢ Gauge group: G = SU(N_c) Ã— SU(2)_L Ã— U(1)_Y
    â€¢ Minimal chiral matter: {Q_L, L, u_R, d_R, e_R}
    â€¢ Neutrino electrically neutral: Y_L = -1/2
    â€¢ Electron charge = -1: Y_e = -1 (fixes U(1) normalization)

DERIVED:
    From [SU(2)]Â²[U(1)] = 0:
        Y_Q = 1/(2 N_c)
    
    From electric charge matching:
        Y_u = 1/2 + 1/(2 N_c)
        Y_d = -1/2 + 1/(2 N_c)
    
    Automatically satisfied:
        [SU(N_c)]Â²[U(1)] = 0  âœ“
        [U(1)]Â³ = 0           âœ“  (for ALL N_c!)
        [grav]Â²[U(1)] = 0     âœ“
    
    From Witten SU(2) anomaly:
        N_c must be ODD

RESULT:
    ALL odd values of N_c give consistent, anomaly-free theories!
    
    The MINIMAL confining choice is N_c = 3 (SU(3)).
    
    This gives:
        Y_Q = 1/6
        Y_u = 2/3
        Y_d = -1/3
    
    Which is EXACTLY the Standard Model!

â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
WHAT IS DERIVED vs ASSUMED
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

DERIVED (from anomaly cancellation):
    âœ“ Y_Q = 1/(2 N_c)
    âœ“ Y_u, Y_d in terms of Y_Q
    âœ“ All anomalies cancel for any odd N_c
    âœ“ SM hypercharges emerge for N_c = 3

ASSUMED (input):
    â€¢ SU(N_c) Ã— SU(2) Ã— U(1) gauge structure
    â€¢ Minimal chiral matter content
    â€¢ Neutrino neutrality (Y_L = -1/2)
    â€¢ Electron charge normalization (Y_e = -1)

NOT UNIQUELY DETERMINED:
    â€¢ N_c itself (any odd value works!)
    â€¢ The choice N_c = 3 requires:
      - Minimality (smallest odd N_c > 1)
      - Confinement (SU(N_c) confines for all N_c â‰¥ 2)
      - Or: observed QCD with 3 colors (empirical)

â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
KEY INSIGHT
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

The Standard Model hypercharges are NOT arbitrary!

Given:
    â€¢ Chiral SU(2) doublets (quarks and leptons)
    â€¢ Anomaly freedom
    â€¢ Neutrino neutrality
    â€¢ Electron charge = -1

The hypercharges 1/6, 2/3, -1/3, -1/2, -1 are FORCED.

Only N_c (number of colors) remains free, constrained to odd values.
    
N_c = 3 is the minimal confining odd choice.
    """)


# =============================================================================
# MAIN
# =============================================================================

def main():
    compute_anomalies_correctly()
    solutions = solve_for_SM()
    analyze_U1_cubed()
    final_verification()
    theorem5_conclusion()


if __name__ == "__main__":
    main()

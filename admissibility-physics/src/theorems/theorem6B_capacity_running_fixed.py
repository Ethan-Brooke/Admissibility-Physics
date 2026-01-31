"""
THEOREM 6B: CAPACITY RENORMALIZATION FLOW (RG RUNNING) â€” FROM 3/8 TO ~0.231

This module continues Theorem 6 (sin^2 Î¸_W(M_U)=3/8 from SU(5) embedding)
by adding scale-dependent "capacity renormalization":

    1/Î±_i(Î¼) = 1/Î±_U + (b_i/2Ï€) ln(M_U/Î¼)          (1-loop)

where Î±_i = g_i^2/(4Ï€) are the gauge fine-structure constants.

Core point:
- Theorem 6A fixes the *boundary condition* at unification (3/8).
- Theorem 6B explains why the low-energy value is smaller: Î±_1 grows with energy
  more slowly than Î±_2 (SM b_i differ), changing the partition ratio.

Admissibility interpretation (optional layer):
- b_i are "enforcement-burden coefficients" for each distinction channel.
- Running corresponds to scale-dependent redistribution of enforceable throughput.

This file is deliberately honest:
- It uses standard 1-loop SM beta coefficients.
- It does NOT claim Admissibility derives the b_i yet (that's a future theorem).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Dict, Tuple


# ---------------------------------------------------------------------
# Standard 1-loop beta coefficients (SM, n_H=1, three generations)
# Conventions: d g / d ln Î¼ = (b / 16Ï€^2) g^3
# With this convention, 1/Î±(Î¼) = 1/Î±(Î¼0) - (b/2Ï€) ln(Î¼/Î¼0).
# We use the equivalent "unification boundary" form:
#    1/Î±_i(Î¼) = 1/Î±_U + (b_i/2Ï€) ln(M_U/Î¼)
# so that asymptotically-free b_i < 0 makes Î±_i smaller at high scale.
#
# IMPORTANT: b1 is for GUT-normalized U(1) (i.e., g1), not gY.
# SM values: b1 = 41/10, b2 = -19/6, b3 = -7
# ---------------------------------------------------------------------

SM_BETA_1LOOP = {
    "b1": 41.0 / 10.0,   # U(1) in SU(5) normalization (g1)
    "b2": -19.0 / 6.0,   # SU(2)
    "b3": -7.0,          # SU(3)
}


@dataclass(frozen=True)
class RGSetup:
    """Boundary + coefficients for 1-loop running."""
    MU: float = 2.0e16          # unification scale (GeV) â€” adjustable
    alphaU: float = 1.0 / 40.0  # unified coupling at MU â€” adjustable (1/40 avoids Landau pole)
    b1: float = SM_BETA_1LOOP["b1"]
    b2: float = SM_BETA_1LOOP["b2"]
    b3: float = SM_BETA_1LOOP["b3"]


def alpha_at_scale(alphaU: float, b: float, MU: float, mu: float) -> float:
    """
    1-loop running from unified boundary (MU, alphaU) down to mu:
        1/Î±(mu) = 1/Î±U + (b/2Ï€) ln(MU/mu)
    """
    if mu <= 0 or MU <= 0:
        raise ValueError("Scales must be positive.")
    if mu > MU:
        # This function is for running down; running up just flips the log.
        pass
    inv = (1.0 / alphaU) + (b / (2.0 * math.pi)) * math.log(MU / mu)
    if inv <= 0:
        raise ValueError("Non-physical coupling encountered (1/Î± <= 0).")
    return 1.0 / inv


def sin2_theta_w_from_alphas(alpha1: float, alpha2: float) -> float:
    """
    Compute sin^2 Î¸_W from Î±1 (GUT-normalized U(1), i.e., g1) and Î±2 (SU(2)).
    Relationship between g1 and SM hypercharge gY:
        g1^2 = (5/3) gY^2  =>  Î±1 = (5/3) Î±Y  =>  Î±Y = (3/5) Î±1

    Then:
        sin^2 Î¸_W = gY^2 / (gY^2 + g2^2) = Î±Y / (Î±Y + Î±2)
                  = (3/5)Î±1 / ((3/5)Î±1 + Î±2)
    """
    alphaY = (3.0 / 5.0) * alpha1
    return alphaY / (alphaY + alpha2)


def run_theorem6b(mu: float = 91.1876, setup: RGSetup = RGSetup()) -> Dict[str, float]:
    """
    Run 1-loop RG from MU to mu and return couplings + sin^2 Î¸W.
    Default mu ~ MZ.
    """
    a1 = alpha_at_scale(setup.alphaU, setup.b1, setup.MU, mu)
    a2 = alpha_at_scale(setup.alphaU, setup.b2, setup.MU, mu)
    a3 = alpha_at_scale(setup.alphaU, setup.b3, setup.MU, mu)
    s2 = sin2_theta_w_from_alphas(a1, a2)

    return {
        "mu": mu,
        "MU": setup.MU,
        "alphaU": setup.alphaU,
        "alpha1": a1,
        "alpha2": a2,
        "alpha3": a3,
        "sin2_theta_w": s2,
    }


def scan_mu_range(mu_min: float = 1e2, mu_max: float = 1e16, n: int = 20, setup: RGSetup = RGSetup()):
    """
    Log-spaced scan of sin^2 Î¸_W(Î¼) between mu_min and mu_max.
    Prints a compact table.
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    log_min, log_max = math.log(mu_min), math.log(mu_max)
    print(f"{'mu[GeV]':>12}  {'sin^2 Î¸W':>10}  {'Î±1':>10}  {'Î±2':>10}  {'Î±3':>10}")
    for i in range(n):
        t = i / (n - 1)
        mu = math.exp(log_min + t * (log_max - log_min))
        res = run_theorem6b(mu=mu, setup=setup)
        print(f"{res['mu']:12.3e}  {res['sin2_theta_w']:10.4f}  {res['alpha1']:10.4f}  {res['alpha2']:10.4f}  {res['alpha3']:10.4f}")


def sanity_check_unification(setup: RGSetup = RGSetup()) -> Tuple[float, float]:
    """
    At mu = MU, Î±1=Î±2=Î±3=Î±U and sin^2 Î¸W = 3/8.
    """
    mu = setup.MU
    a1 = alpha_at_scale(setup.alphaU, setup.b1, setup.MU, mu)
    a2 = alpha_at_scale(setup.alphaU, setup.b2, setup.MU, mu)
    s2 = sin2_theta_w_from_alphas(a1, a2)
    return s2, 3.0 / 8.0


def main():
    print("THEOREM 6B â€” 1-loop running from MU to MZ")
    setup = RGSetup(MU=2e16, alphaU=1/40)

    s2_at_MU, target = sanity_check_unification(setup)
    print(f"Sanity @ MU: sin^2Î¸W = {s2_at_MU:.6f} (target {target:.6f})")

    # Default MZ-ish point
    res = run_theorem6b(setup=setup)
    print("\nDefault evaluation near MZ:")
    for k in ["MU", "alphaU", "mu", "alpha1", "alpha2", "alpha3", "sin2_theta_w"]:
        print(f"  {k:>12}: {res[k]:.6g}")

    print("\nScan (selected scales):")
    scan_mu_range(mu_min=1e2, mu_max=1e16, n=10, setup=setup)


if __name__ == "__main__":
    main()

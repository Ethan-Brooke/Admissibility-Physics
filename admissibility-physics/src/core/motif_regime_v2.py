#!/usr/bin/env python3
"""
MOTIF REGIME ANALYSIS v2.1
==========================

REFACTORED with:
1. Per-interface load vectors n_i (not global size)
2. Composability via combined load vectors
3. Refined failure mode detection (eta-share metric)
4. EPS_SLACK for strict interior Regime R (v2.1)
5. eta_overage_share for routing diagnostics (v2.1)

This is future-proof for:
- Routing (different interfaces carry different load)
- Geometry (distance = minimal cost over routes)
- Real composability (load vectors add, not sizes)
- Accumulated cost (stable boundaries)

Author: Admissibility Physics Project
Version: 2.1
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, FrozenSet
from collections import defaultdict
import json

# =============================================================================
# GLOBAL CONSTANTS
# =============================================================================

# Admissibility margin for strict interior of Regime R
# This prevents knife-edge boundaries and ensures:
# - Non-zero tangent space
# - Stable routing minima  
# - Well-defined accumulated cost
EPS_SLACK = 1e-6

# =============================================================================
# INTERFACE DEFINITION
# =============================================================================

@dataclass(frozen=True)
class Interface:
    """
    An enforcement interface.
    
    Now explicitly takes load n_i (not assumed equal to motif size).
    """
    name: str
    capacity: float       # C_i
    epsilon: float = 1.0  # Linear cost coefficient
    eta: float = 0.5      # Quadratic cost coefficient (non-closure)
    
    def cost(self, n: int) -> float:
        """E_i(n) = ÎµÂ·n + Î·Â·C(n,2)"""
        if n <= 0:
            return 0.0
        return self.epsilon * n + self.eta * n * (n - 1) / 2
    
    def linear_cost(self, n: int) -> float:
        """Linear component only: ÎµÂ·n"""
        return self.epsilon * n if n > 0 else 0.0
    
    def quadratic_cost(self, n: int) -> float:
        """Quadratic component only: Î·Â·C(n,2)"""
        if n <= 1:
            return 0.0
        return self.eta * n * (n - 1) / 2
    
    def max_n(self) -> int:
        """Maximum n before E(n) > C"""
        if self.eta < 1e-12:
            return int(self.capacity / self.epsilon) if self.epsilon > 0 else 999
        a = self.eta / 2
        b = self.epsilon - self.eta / 2
        c = -self.capacity
        disc = b*b - 4*a*c
        return max(0, int((-b + math.sqrt(disc)) / (2 * a))) if disc >= 0 else 0
    
    def headroom(self, n: int) -> float:
        """H_i = C_i - E_i(n)"""
        return self.capacity - self.cost(n)
    
    def saturation_fraction(self, n: int) -> float:
        """Ïƒ_i = E_i(n) / C_i"""
        return self.cost(n) / self.capacity if self.capacity > 0 else 1.0


# =============================================================================
# LOAD VECTOR
# =============================================================================

@dataclass
class LoadVector:
    """
    Per-interface load for a motif.
    
    This is the key abstraction: motifs don't just have a "size",
    they have a load at each interface.
    
    In mean-field: all loads equal (n_i = |M| for all i)
    In routing: loads can differ (n_i depends on how motif routes through i)
    """
    loads: Dict[str, int]
    
    @classmethod
    def uniform(cls, interfaces: List[Interface], size: int) -> 'LoadVector':
        """Create uniform load vector (mean-field case)."""
        return cls(loads={itf.name: size for itf in interfaces})
    
    @classmethod
    def from_dict(cls, d: Dict[str, int]) -> 'LoadVector':
        return cls(loads=dict(d))
    
    def __add__(self, other: 'LoadVector') -> 'LoadVector':
        """Add load vectors (composition)."""
        combined = dict(self.loads)
        for name, load in other.loads.items():
            combined[name] = combined.get(name, 0) + load
        return LoadVector(loads=combined)
    
    def __getitem__(self, interface_name: str) -> int:
        return self.loads.get(interface_name, 0)
    
    def total(self) -> int:
        """Total load across all interfaces (for reference)."""
        return sum(self.loads.values())
    
    def max_load(self) -> int:
        """Maximum load on any interface."""
        return max(self.loads.values()) if self.loads else 0
    
    def __repr__(self):
        return f"Load({self.loads})"


# =============================================================================
# FAILURE MODE ANALYSIS (Refined)
# =============================================================================

@dataclass
class FailureDiagnostics:
    """
    Detailed diagnostics for why a motif configuration fails/succeeds.
    
    Now uses load vectors and eta-share metrics.
    
    v2.1: Added EPS_SLACK and eta_overage_share.
    """
    interface_name: str
    load: int
    
    # Costs
    total_cost: float = 0.0
    linear_cost: float = 0.0
    quadratic_cost: float = 0.0
    
    # Capacity analysis
    capacity: float = 0.0
    headroom: float = 0.0
    saturation: float = 0.0
    
    # Overage analysis (when headroom < 0)
    overage: float = 0.0
    eta_share: float = 0.0          # Fraction of TOTAL cost from Î· term
    eta_overage_share: float = 0.0  # Fraction of OVERAGE from Î· term (v2.1)
    
    # Classification
    # v2.1: Use EPS_SLACK for strict interior
    is_saturated: bool = False      # headroom <= EPS_SLACK
    is_violated: bool = False       # headroom < 0 (actually over capacity)
    is_boundary: bool = False       # 0 <= headroom <= EPS_SLACK (knife-edge)
    
    def compute(self, itf: Interface):
        """Compute all diagnostics for this interface."""
        n = self.load
        
        self.total_cost = itf.cost(n)
        self.linear_cost = itf.linear_cost(n)
        self.quadratic_cost = itf.quadratic_cost(n)
        
        self.capacity = itf.capacity
        self.headroom = itf.headroom(n)
        self.saturation = itf.saturation_fraction(n)
        
        # v2.1: Three-way classification with EPS_SLACK
        self.is_violated = self.headroom < 0
        self.is_boundary = (0 <= self.headroom <= EPS_SLACK)
        self.is_saturated = self.headroom <= EPS_SLACK  # Either violated or boundary
        
        # Eta share of TOTAL cost (for regime characterization)
        self.eta_share = self.quadratic_cost / self.total_cost if self.total_cost > 0 else 0
        
        # v2.1: Eta share of OVERAGE (for routing/Î› diagnostics)
        if self.is_violated:
            self.overage = -self.headroom
            # What fraction of the overage is due to quadratic term?
            # This tells us: would increasing C help, or is it Î·-locked?
            # 
            # Compute: how much would we save by removing quadratic term?
            linear_only_cost = self.linear_cost
            linear_only_headroom = self.capacity - linear_only_cost
            
            if linear_only_headroom >= 0:
                # Linear alone would fit â†’ overage is entirely from Î·
                self.eta_overage_share = 1.0
            else:
                # Even linear doesn't fit â†’ split the blame
                linear_overage = -linear_only_headroom
                self.eta_overage_share = max(0, (self.overage - linear_overage) / self.overage) if self.overage > 0 else 0
        else:
            self.overage = 0
            self.eta_overage_share = 0


@dataclass
class FailureAnalysis:
    """
    Complete failure analysis for a load vector.
    
    Classifies failure mode based on:
    - Which interfaces saturate
    - Whether saturation is linear or eta-dominated
    - Margin to composability
    """
    load_vector: LoadVector
    interfaces: List[Interface]
    
    # Per-interface diagnostics
    diagnostics: Dict[str, FailureDiagnostics] = field(default_factory=dict)
    
    # Overall classification
    failure_mode: str = ""
    bottleneck_interface: str = ""
    
    # Composability metrics
    min_headroom: float = 0.0
    composability_index: float = 0.0  # Îº = min(H_i) / min(C_i)
    
    # For computing max partner
    max_partner_load: Optional[LoadVector] = None
    
    def analyze(self):
        """Perform complete failure analysis."""
        # Compute per-interface diagnostics
        for itf in self.interfaces:
            load = self.load_vector[itf.name]
            diag = FailureDiagnostics(interface_name=itf.name, load=load)
            diag.compute(itf)
            self.diagnostics[itf.name] = diag
        
        # Find bottleneck (minimum headroom)
        self.bottleneck_interface = min(
            self.diagnostics, 
            key=lambda name: self.diagnostics[name].headroom
        )
        self.min_headroom = self.diagnostics[self.bottleneck_interface].headroom
        
        # Composability index (strict interior)
        # Îº > 0 means strictly inside Regime R
        # Îº â‰ˆ 0 means boundary (knife-edge)
        # Îº < 0 means violated
        min_capacity = min(itf.capacity for itf in self.interfaces)
        self.composability_index = (self.min_headroom - EPS_SLACK) / min_capacity if min_capacity > 0 else 0
        
        # Classify failure mode
        self._classify()
        
        # Find max partner if composable
        if self.failure_mode == "COMPOSABLE":
            self.max_partner_load = self._find_max_partner()
    
    def _classify(self):
        """Classify the failure mode."""
        saturated = [name for name, d in self.diagnostics.items() if d.is_saturated]
        
        if not saturated:
            self.failure_mode = "COMPOSABLE"
            return
        
        if len(saturated) == 1:
            # Single interface saturation - check if eta-dominated
            diag = self.diagnostics[saturated[0]]
            if diag.eta_share > 0.5:
                self.failure_mode = "SINGLE_INTERFACE_ETA_DOMINATED"
            else:
                self.failure_mode = "SINGLE_INTERFACE_LINEAR_BOTTLENECK"
        else:
            # Multiple interfaces saturated
            # Check if eta dominates across saturated interfaces
            avg_eta_share = sum(
                self.diagnostics[name].eta_share 
                for name in saturated
            ) / len(saturated)
            
            if avg_eta_share > 0.6:
                self.failure_mode = "MULTI_INTERFACE_ETA_DOMINATED"
            elif avg_eta_share < 0.3:
                self.failure_mode = "MULTI_INTERFACE_LINEAR_COMPETITION"
            else:
                self.failure_mode = "MULTI_INTERFACE_MIXED"
    
    def _find_max_partner(self) -> Optional[LoadVector]:
        """
        Find the maximum partner load vector that can coexist.
        
        For uniform loads, this is finding max m such that
        E_i(n_i + m) <= C_i for all i.
        """
        # Binary search for max uniform partner
        lo, hi = 0, 100
        
        while lo < hi:
            mid = (lo + hi + 1) // 2
            
            # Create partner load vector (uniform for now)
            partner = LoadVector.uniform(self.interfaces, mid)
            combined = self.load_vector + partner
            
            # Check if combined is admissible
            admissible = all(
                itf.cost(combined[itf.name]) <= itf.capacity
                for itf in self.interfaces
            )
            
            if admissible:
                lo = mid
            else:
                hi = mid - 1
        
        if lo > 0:
            return LoadVector.uniform(self.interfaces, lo)
        return None
    
    def summary(self) -> str:
        """Human-readable summary."""
        lines = [f"Load {self.load_vector}: {self.failure_mode}"]
        lines.append(f"  Bottleneck: {self.bottleneck_interface}")
        lines.append(f"  Min headroom: {self.min_headroom:.2f}")
        lines.append(f"  Composability index Îº: {self.composability_index:.3f}")
        
        if self.failure_mode == "COMPOSABLE" and self.max_partner_load:
            lines.append(f"  Max partner: {self.max_partner_load}")
        
        # Per-interface breakdown
        lines.append("  Per-interface:")
        for name, diag in self.diagnostics.items():
            status = "âœ—" if diag.is_saturated else "âœ“"
            lines.append(f"    {status} {name}: E={diag.total_cost:.1f} "
                        f"(lin={diag.linear_cost:.1f}, quad={diag.quadratic_cost:.1f}), "
                        f"H={diag.headroom:.1f}, Î·-share={diag.eta_share:.1%}")
        
        return "\n".join(lines)


# =============================================================================
# REGIME BOUNDARY ANALYSIS
# =============================================================================

@dataclass
class RegimeBoundary:
    """
    Analysis of the composability boundary.
    
    Now works with load vectors.
    """
    interfaces: List[Interface]
    
    # Results
    composable_loads: List[LoadVector] = field(default_factory=list)
    saturating_loads: List[LoadVector] = field(default_factory=list)
    
    # Per-load analysis
    analyses: Dict[int, FailureAnalysis] = field(default_factory=dict)
    
    # Boundary metrics
    max_composable_uniform_size: int = 0
    regime_R_sizes: List[int] = field(default_factory=list)
    
    def analyze_uniform(self, max_size: int = 20):
        """
        Analyze uniform load vectors (mean-field case).
        
        This is the starting point; non-uniform will come with routing.
        """
        for size in range(1, max_size + 1):
            load = LoadVector.uniform(self.interfaces, size)
            analysis = FailureAnalysis(load_vector=load, interfaces=self.interfaces)
            analysis.analyze()
            
            self.analyses[size] = analysis
            
            if analysis.failure_mode == "COMPOSABLE":
                self.composable_loads.append(load)
                self.regime_R_sizes.append(size)
            else:
                self.saturating_loads.append(load)
        
        if self.regime_R_sizes:
            self.max_composable_uniform_size = max(self.regime_R_sizes)
    
    def print_report(self):
        """Print the regime boundary report."""
        print("\n" + "=" * 90)
        print("REGIME BOUNDARY ANALYSIS (Load Vector Formulation, v2.1)")
        print("=" * 90)
        
        print(f"\nEPS_SLACK = {EPS_SLACK} (strict interior margin)")
        
        print("\nInterfaces:")
        for itf in self.interfaces:
            print(f"  {itf.name}: C={itf.capacity}, Îµ={itf.epsilon}, Î·={itf.eta}, N_max={itf.max_n()}")
        
        print(f"\n{'Size':>4} {'Mode':<35} {'Bottleneck':<10} {'H_min':>8} {'Îº':>8} {'Î·-share':>8} {'Î·-over':>8}")
        print("-" * 90)
        
        for size in sorted(self.analyses.keys()):
            a = self.analyses[size]
            bn_diag = a.diagnostics[a.bottleneck_interface]
            eta_over = f"{bn_diag.eta_overage_share:.0%}" if bn_diag.is_violated else "â€”"
            print(f"{size:>4} {a.failure_mode:<35} {a.bottleneck_interface:<10} "
                  f"{a.min_headroom:>8.2f} {a.composability_index:>8.3f} {bn_diag.eta_share:>7.1%} {eta_over:>8}")
        
        print("\n" + "-" * 90)
        print(f"Regime R (strict interior): sizes {self.regime_R_sizes}")
        print(f"Max composable uniform size: {self.max_composable_uniform_size}")
        print(f"\nÎ·-share = quadratic/total (regime character)")
        print(f"Î·-over = quadratic contribution to overage (routing diagnosis)")
        
        if self.regime_R_sizes:
            print(f"\n*** DYNAMICS EXISTS for sizes 1 to {self.max_composable_uniform_size} ***")
        else:
            print(f"\n*** NO DYNAMICS: all sizes saturate ***")


# =============================================================================
# FAILURE MODE TAXONOMY
# =============================================================================

def failure_mode_taxonomy(interfaces: List[Interface], max_size: int = 15):
    """
    Generate complete failure mode taxonomy.
    """
    print("\n" + "=" * 80)
    print("FAILURE MODE TAXONOMY")
    print("=" * 80)
    
    mode_counts: Dict[str, List[int]] = defaultdict(list)
    
    for size in range(1, max_size + 1):
        load = LoadVector.uniform(interfaces, size)
        analysis = FailureAnalysis(load_vector=load, interfaces=interfaces)
        analysis.analyze()
        mode_counts[analysis.failure_mode].append(size)
    
    print("\nFailure modes observed:\n")
    
    for mode, sizes in sorted(mode_counts.items()):
        print(f"  {mode}:")
        print(f"    Sizes: {sizes}")
        
        if mode == "COMPOSABLE":
            print("    â†’ Room for perturbations; dynamics possible")
            print("    â†’ This is REGIME R")
        elif "ETA_DOMINATED" in mode:
            print("    â†’ Quadratic (non-closure) term dominates")
            print("    â†’ This is QUANTUM SATURATION")
            print("    â†’ Cannot be relieved by just increasing capacity")
        elif "LINEAR" in mode:
            print("    â†’ Linear term dominates")
            print("    â†’ This is CLASSICAL CONGESTION")
            print("    â†’ Could be relieved by increasing C_i")
        elif "MIXED" in mode:
            print("    â†’ Both linear and quadratic contribute")
            print("    â†’ Hybrid saturation")
        print()
    
    return mode_counts


# =============================================================================
# COMPOSABILITY VIA LOAD VECTORS
# =============================================================================

def composability_analysis(interfaces: List[Interface]):
    """
    Demonstrate composability with load vectors.
    """
    print("\n" + "=" * 80)
    print("COMPOSABILITY ANALYSIS (Load Vector Formulation)")
    print("=" * 80)
    
    # Example: two motifs with different loads
    print("\nExample: Composing two motifs")
    print("-" * 40)
    
    # Motif A: loads interface alpha more
    load_A = LoadVector(loads={"alpha": 3, "beta": 2, "gamma": 1})
    # Motif B: loads interface gamma more
    load_B = LoadVector(loads={"alpha": 1, "beta": 2, "gamma": 3})
    
    print(f"  Motif A: {load_A}")
    print(f"  Motif B: {load_B}")
    
    combined = load_A + load_B
    print(f"  Combined (A+B): {combined}")
    
    # Analyze each
    analysis_A = FailureAnalysis(load_vector=load_A, interfaces=interfaces)
    analysis_A.analyze()
    
    analysis_B = FailureAnalysis(load_vector=load_B, interfaces=interfaces)
    analysis_B.analyze()
    
    analysis_combined = FailureAnalysis(load_vector=combined, interfaces=interfaces)
    analysis_combined.analyze()
    
    print(f"\n  Motif A: {analysis_A.failure_mode} (Îº={analysis_A.composability_index:.3f})")
    print(f"  Motif B: {analysis_B.failure_mode} (Îº={analysis_B.composability_index:.3f})")
    print(f"  Combined: {analysis_combined.failure_mode} (Îº={analysis_combined.composability_index:.3f})")
    
    if analysis_combined.failure_mode == "COMPOSABLE":
        print("\n  âœ“ A and B can coexist!")
    else:
        print(f"\n  âœ— A and B cannot coexist: {analysis_combined.failure_mode}")
    
    # Show why load vectors matter
    print("\n" + "-" * 40)
    print("Why load vectors matter:")
    print("-" * 40)
    
    # Uniform load of size 4
    uniform_4 = LoadVector.uniform(interfaces, 4)
    analysis_u4 = FailureAnalysis(load_vector=uniform_4, interfaces=interfaces)
    analysis_u4.analyze()
    
    # Non-uniform load with same total
    nonuniform_4 = LoadVector(loads={"alpha": 5, "beta": 4, "gamma": 3})
    analysis_nu4 = FailureAnalysis(load_vector=nonuniform_4, interfaces=interfaces)
    analysis_nu4.analyze()
    
    print(f"\n  Uniform(4):    {uniform_4}")
    print(f"    â†’ {analysis_u4.failure_mode}, Îº={analysis_u4.composability_index:.3f}")
    
    print(f"\n  Non-uniform:   {nonuniform_4}")
    print(f"    â†’ {analysis_nu4.failure_mode}, Îº={analysis_nu4.composability_index:.3f}")
    
    print("\n  Same total load, different routing â†’ different composability!")
    print("  This is why load vectors are essential for routing/geometry.")


# =============================================================================
# PAPER 6 CONNECTION
# =============================================================================

def paper6_connection(interfaces: List[Interface]):
    """
    Connect to Paper 6: Dynamics requires Regime R.
    """
    print("\n" + "=" * 80)
    print("PAPER 6: DYNAMICS REQUIRES REGIME R")
    print("=" * 80)
    
    boundary = RegimeBoundary(interfaces=interfaces)
    boundary.analyze_uniform(max_size=15)
    
    print(f"""
THEOREM (Dynamics requires Regime R):

  Variational dynamics exists âŸº âˆƒ composable load vectors.

PROOF SKETCH:
  1. Equations of motion require Î´S/Î´Ï†
  2. This requires tangent space (nearby admissible states)
  3. "Nearby" = current load + small perturbation still admissible
  4. This is exactly: load_vector + ÎµÂ·Î´load is admissible
  5. Which requires: positive headroom at all interfaces
  6. Which is: composability (M4)

COMPUTATIONAL VERIFICATION:
""")
    
    if boundary.regime_R_sizes:
        print(f"  âœ“ Regime R exists: sizes {boundary.regime_R_sizes}")
        print(f"  âœ“ Max composable: {boundary.max_composable_uniform_size}")
        print(f"  âœ“ Dynamics is possible in this region")
        
        # Show the transition
        if boundary.max_composable_uniform_size < 15:
            trans = boundary.max_composable_uniform_size
            a_in = boundary.analyses[trans]
            a_out = boundary.analyses[trans + 1]
            
            print(f"\n  TRANSITION at size {trans} â†’ {trans+1}:")
            print(f"    Size {trans}: Îº = {a_in.composability_index:.3f} > 0 (composable)")
            print(f"    Size {trans+1}: Îº = {a_out.composability_index:.3f} â‰¤ 0 (saturated)")
            print(f"    Bottleneck: {a_out.bottleneck_interface}")
            print(f"    Failure mode: {a_out.failure_mode}")
    else:
        print(f"  âœ— No Regime R: all sizes saturate")
        print(f"  âœ— No dynamics possible")
    
    print(f"""
PHYSICAL INTERPRETATION:
  - Regime R = where field theory is defined
  - Outside Regime R = no infinitesimal variations = no EoM
  - Boundary = where "physics turns on/off"
  - Î·-dominated saturation = quantum limit
  - Linear saturation = classical congestion
""")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘              MOTIF REGIME ANALYSIS v2 (Load Vectors)                 â•‘")
    print("â•‘                                                                      â•‘")
    print("â•‘  Refactored for: routing, geometry, real composability              â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    # Standard interfaces
    interfaces = [
        Interface("alpha", capacity=12.0, epsilon=1.0, eta=0.4),
        Interface("beta", capacity=15.0, epsilon=1.2, eta=0.5),
        Interface("gamma", capacity=10.0, epsilon=0.8, eta=0.6),
    ]
    
    # 1. Regime boundary
    boundary = RegimeBoundary(interfaces=interfaces)
    boundary.analyze_uniform(max_size=12)
    boundary.print_report()
    
    # 2. Failure taxonomy
    failure_mode_taxonomy(interfaces, max_size=12)
    
    # 3. Composability with load vectors
    composability_analysis(interfaces)
    
    # 4. Paper 6 connection
    paper6_connection(interfaces)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY: Load Vector Formulation v2.1")
    print("=" * 80)
    print(f"""
KEY CHANGES FROM v1:

1. LOAD VECTORS instead of global size
   - n_i per interface, not just |M|
   - Composition: load_A + load_B (vector addition)
   - Prepared for routing (different paths â†’ different loads)

2. REFINED FAILURE MODES
   - ETA_DOMINATED vs LINEAR_BOTTLENECK
   - Î·-share metric: how much is quantum vs classical?
   - Mixed modes for hybrid saturation

3. COMPOSABILITY via combined load vectors
   - M4 now checks: can load_A + load_B fit?
   - Not just: can size_A + size_B fit?
   - This is correct under routing

v2.1 ADDITIONS:

4. EPS_SLACK = {EPS_SLACK} (strict interior)
   - Regime R = headroom > EPS_SLACK (not just >= 0)
   - Prevents knife-edge boundaries
   - Stable for variational calculus

5. Î·-overage-share metric
   - What fraction of overage is from Î· term?
   - Tells us: would more capacity help?
   - Î·-over = 100% â†’ capacity won't help (quantum limit)
   - Î·-over = 0% â†’ capacity would help (classical congestion)

READY FOR NEXT PUSH:
   - Routing = choose load vectors to minimize cost
   - Geometry = distance from routing costs
   - Accumulated cost = variation of loads over time
""")


if __name__ == "__main__":
    main()

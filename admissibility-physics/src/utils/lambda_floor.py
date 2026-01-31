#!/usr/bin/env python3
"""
LAMBDA FLOOR ENGINE
===================

Î› = irreducible residual enforcement cost that cannot be locally routed away.

Core insight:
- The universe routes correlations to minimize enforcement burden
- But some cost CANNOT be eliminated by rerouting
- This residual is Î›: the "cosmological constant" of enforcement

Î› is NOT what you add. Î› is what REMAINS after optimal rerouting.

This completes the unification:
  Enforceability â†’ Admissibility â†’ Composability â†’ Geometry â†’ Time â†’ Î›

Author: Admissibility Physics Project
Version: 1.0
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
from heapq import heappush, heappop
import itertools

# =============================================================================
# CONSTANTS
# =============================================================================

EPS_SLACK = 1e-6      # Admissibility margin
EPS_COST = 1e-9       # Cost comparison tolerance

# =============================================================================
# INTERFACE
# =============================================================================

@dataclass(frozen=True)
class Interface:
    """An enforcement interface with capacity and cost model."""
    name: str
    capacity: float
    epsilon: float = 1.0
    eta: float = 0.5
    
    def cost(self, n: int) -> float:
        """E(n) = ÎµÂ·n + Î·Â·C(n,2)"""
        if n <= 0:
            return 0.0
        return self.epsilon * n + self.eta * n * (n - 1) / 2
    
    def headroom(self, n: int) -> float:
        """H = C - E(n)"""
        return self.capacity - self.cost(n)
    
    def max_n(self) -> int:
        """Maximum n before E(n) > C"""
        if self.eta < 1e-12:
            return int(self.capacity / self.epsilon) if self.epsilon > 0 else 999
        a = self.eta / 2
        b = self.epsilon - self.eta / 2
        c = -self.capacity
        disc = b*b - 4*a*c
        return max(0, int((-b + math.sqrt(disc)) / (2 * a))) if disc >= 0 else 0


# =============================================================================
# LOAD VECTOR
# =============================================================================

@dataclass
class LoadVector:
    """Per-interface load configuration."""
    loads: Dict[str, int]
    
    @classmethod
    def empty(cls) -> 'LoadVector':
        return cls(loads={})
    
    def __getitem__(self, name: str) -> int:
        return self.loads.get(name, 0)
    
    def __add__(self, other: 'LoadVector') -> 'LoadVector':
        combined = dict(self.loads)
        for name, load in other.loads.items():
            combined[name] = combined.get(name, 0) + load
        return LoadVector(loads=combined)
    
    def __sub__(self, other: 'LoadVector') -> 'LoadVector':
        result = dict(self.loads)
        for name, load in other.loads.items():
            result[name] = result.get(name, 0) - load
        return LoadVector(loads=result)
    
    def copy(self) -> 'LoadVector':
        return LoadVector(loads=dict(self.loads))
    
    def __repr__(self):
        return f"Load({self.loads})"


# =============================================================================
# NETWORK (simplified from routing engine)
# =============================================================================

@dataclass(frozen=True)
class Edge:
    """An edge connecting two nodes via an interface."""
    u: str
    v: str
    interface: Interface
    
    def other(self, node: str) -> str:
        return self.v if node == self.u else self.u


@dataclass
class Network:
    """A routing network."""
    nodes: List[str]
    edges: List[Edge]
    
    _adjacency: Dict[str, List[Edge]] = field(default_factory=dict, repr=False)
    _interfaces: Dict[str, Interface] = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        self._adjacency = defaultdict(list)
        self._interfaces = {}
        for edge in self.edges:
            self._adjacency[edge.u].append(edge)
            self._adjacency[edge.v].append(edge)
            self._interfaces[edge.interface.name] = edge.interface
    
    def neighbors(self, node: str) -> List[Tuple[str, Edge]]:
        return [(e.other(node), e) for e in self._adjacency[node]]
    
    def interfaces(self) -> List[Interface]:
        return list(self._interfaces.values())


# =============================================================================
# PATH FINDING
# =============================================================================

@dataclass
class Path:
    """A path through the network."""
    nodes: List[str]
    edges: List[Edge]
    
    def load_contribution(self) -> Dict[str, int]:
        """Load added by this path."""
        loads = defaultdict(int)
        for e in self.edges:
            loads[e.interface.name] += 1
        return dict(loads)


def find_all_paths(
    network: Network,
    source: str,
    target: str,
    max_length: int = 6,
    max_paths: int = 20
) -> List[Path]:
    """Find paths from source to target."""
    if source == target:
        return [Path(nodes=[source], edges=[])]
    
    paths = []
    
    def dfs(current: str, visited: Set[str], path_nodes: List[str], path_edges: List[Edge]):
        if len(paths) >= max_paths or len(path_edges) > max_length:
            return
        
        if current == target:
            paths.append(Path(nodes=list(path_nodes), edges=list(path_edges)))
            return
        
        for neighbor, edge in network.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path_nodes.append(neighbor)
                path_edges.append(edge)
                dfs(neighbor, visited, path_nodes, path_edges)
                path_edges.pop()
                path_nodes.pop()
                visited.remove(neighbor)
    
    dfs(source, {source}, [source], [])
    paths.sort(key=lambda p: len(p.edges))
    return paths


# =============================================================================
# OBLIGATIONS (COMMITTED CORRELATIONS)
# =============================================================================

@dataclass
class Obligation:
    """
    A committed correlation that must be maintained.
    
    This is a "record" in the Admissibility sense:
    once committed, it cannot be erased, only rerouted.
    """
    id: int
    source: str
    target: str
    demand: int = 1
    
    def __repr__(self):
        return f"Ob({self.id}: {self.source}â†”{self.target}, d={self.demand})"


@dataclass
class RoutedObligation:
    """An obligation with its current routing."""
    obligation: Obligation
    path: Path
    
    def load_contribution(self) -> Dict[str, int]:
        return self.path.load_contribution()


# =============================================================================
# COST FUNCTIONS
# =============================================================================

def total_cost(load: LoadVector, interfaces: List[Interface]) -> float:
    """Total enforcement cost for a load configuration."""
    itf_map = {i.name: i for i in interfaces}
    return sum(itf_map[name].cost(n) for name, n in load.loads.items() if name in itf_map)


def residual_fraction(load: LoadVector, interfaces: List[Interface]) -> Tuple[float, str]:
    """
    Compute min_i(E_i/C_i) and the bottleneck interface.
    
    This measures how "full" the most constrained interface is.
    """
    worst = 0.0
    bn = ""
    
    for itf in interfaces:
        n = load[itf.name]
        frac = itf.cost(n) / itf.capacity if itf.capacity > 0 else 1.0
        if frac > worst:
            worst = frac
            bn = itf.name
    
    return worst, bn


def is_admissible(load: LoadVector, interfaces: List[Interface]) -> bool:
    """Check if load configuration is admissible."""
    for itf in interfaces:
        if itf.headroom(load[itf.name]) <= EPS_SLACK:
            return False
    return True


def transition_cost(L_prev: LoadVector, L_next: LoadVector, interfaces: List[Interface]) -> float:
    """Cost of transitioning between load states."""
    cost = 0.0
    for itf in interfaces:
        E_prev = itf.cost(L_prev[itf.name])
        E_next = itf.cost(L_next[itf.name])
        cost += abs(E_next - E_prev)
    return cost


# =============================================================================
# ROUTING WITH OBLIGATIONS
# =============================================================================

def route_obligation(
    network: Network,
    obligation: Obligation,
    existing_load: LoadVector,
    max_paths: int = 10
) -> Optional[RoutedObligation]:
    """
    Find the best admissible routing for a single obligation.
    
    Returns None if no admissible routing exists.
    """
    paths = find_all_paths(
        network, obligation.source, obligation.target, 
        max_length=6, max_paths=max_paths
    )
    
    interfaces = network.interfaces()
    best_path = None
    best_cost = float('inf')
    
    for path in paths:
        # Compute new load if we use this path
        path_contrib = path.load_contribution()
        new_loads = dict(existing_load.loads)
        for name, contrib in path_contrib.items():
            new_loads[name] = new_loads.get(name, 0) + contrib * obligation.demand
        
        new_load = LoadVector(loads=new_loads)
        
        # Check admissibility
        if not is_admissible(new_load, interfaces):
            continue
        
        # Compute cost
        cost = total_cost(new_load, interfaces)
        
        if cost < best_cost:
            best_cost = cost
            best_path = path
    
    if best_path is None:
        return None
    
    return RoutedObligation(obligation=obligation, path=best_path)


def route_all_obligations(
    network: Network,
    obligations: List[Obligation],
    initial_load: Optional[LoadVector] = None
) -> Optional[Tuple[List[RoutedObligation], LoadVector]]:
    """
    Route all obligations greedily (in order).
    
    Returns (routed_obligations, final_load) or None if impossible.
    """
    load = initial_load.copy() if initial_load else LoadVector.empty()
    routed = []
    
    for ob in obligations:
        result = route_obligation(network, ob, load)
        if result is None:
            return None
        
        routed.append(result)
        
        # Update load
        for name, contrib in result.path.load_contribution().items():
            load.loads[name] = load.loads.get(name, 0) + contrib * ob.demand
    
    return routed, load


# =============================================================================
# RELAXATION (REROUTING TO MINIMIZE COST)
# =============================================================================

def compute_load_from_routed(
    routed: List[RoutedObligation]
) -> LoadVector:
    """Compute total load from a set of routed obligations."""
    loads = defaultdict(int)
    for r in routed:
        for name, contrib in r.path.load_contribution().items():
            loads[name] += contrib * r.obligation.demand
    return LoadVector(loads=dict(loads))


def relax_routing(
    network: Network,
    routed: List[RoutedObligation],
    iterations: int = 3
) -> Tuple[List[RoutedObligation], LoadVector]:
    """
    Relax routing by trying alternative paths for each obligation.
    
    Uses coordinate descent: fix all but one, reroute that one optimally.
    """
    interfaces = network.interfaces()
    current = list(routed)
    current_load = compute_load_from_routed(current)
    current_cost = total_cost(current_load, interfaces)
    
    for _ in range(iterations):
        improved = False
        
        for i in range(len(current)):
            # Remove obligation i's contribution
            ob = current[i].obligation
            old_contrib = current[i].path.load_contribution()
            
            remaining_loads = dict(current_load.loads)
            for name, contrib in old_contrib.items():
                remaining_loads[name] = remaining_loads.get(name, 0) - contrib * ob.demand
            remaining_load = LoadVector(loads=remaining_loads)
            
            # Try to reroute obligation i
            new_routed = route_obligation(network, ob, remaining_load)
            
            if new_routed is None:
                continue  # Keep old routing
            
            # Compute new total load and cost
            new_contrib = new_routed.path.load_contribution()
            new_loads = dict(remaining_load.loads)
            for name, contrib in new_contrib.items():
                new_loads[name] = new_loads.get(name, 0) + contrib * ob.demand
            new_load = LoadVector(loads=new_loads)
            new_cost = total_cost(new_load, interfaces)
            
            if new_cost + EPS_COST < current_cost:
                current[i] = new_routed
                current_load = new_load
                current_cost = new_cost
                improved = True
        
        if not improved:
            break
    
    return current, current_load


# =============================================================================
# LAMBDA STATE
# =============================================================================

@dataclass
class LambdaState:
    """
    State of the Î› floor at a point in time.
    
    Tracks:
    - Current load (before relaxation)
    - Residual load (after optimal rerouting)
    - Various Î› measures
    """
    time_step: int
    
    # Before relaxation
    raw_load: LoadVector
    raw_cost: float
    
    # After relaxation (residual = Î›)
    residual_load: LoadVector
    lambda_E: float           # Total residual cost
    lambda_sigma: float       # Saturation fraction of bottleneck
    bottleneck: str           # Most saturated interface
    
    # Action accumulated so far
    action: float
    
    # How much was saved by relaxation
    relaxation_savings: float
    
    def __repr__(self):
        return (f"Î›(t={self.time_step}): Î›_E={self.lambda_E:.2f}, "
                f"Î›_Ïƒ={self.lambda_sigma:.1%}, bn={self.bottleneck}")


# =============================================================================
# LAMBDA FLOOR ESTIMATION
# =============================================================================

def estimate_lambda_floor(
    network: Network,
    obligation_stream: List[Obligation],
    relax_every: int = 3,
    verbose: bool = True
) -> List[LambdaState]:
    """
    Estimate the Î› floor over time as obligations accumulate.
    
    Process:
    1. Add obligations one at a time (records accumulating)
    2. Route each new obligation
    3. Periodically relax all routings to find residual
    4. Î› = cost that cannot be eliminated by rerouting
    
    This is the "cosmological constant" emerging from enforcement.
    """
    interfaces = network.interfaces()
    
    history = []
    active_routed: List[RoutedObligation] = []
    action = 0.0
    prev_load = LoadVector.empty()
    
    if verbose:
        print("\n" + "=" * 70)
        print("LAMBDA FLOOR ESTIMATION")
        print("=" * 70)
        print(f"\nProcessing {len(obligation_stream)} obligations...")
        print(f"Relaxation every {relax_every} steps")
    
    for t, ob in enumerate(obligation_stream):
        # Current load before adding new obligation
        current_load = compute_load_from_routed(active_routed)
        
        # Route the new obligation
        routed = route_obligation(network, ob, current_load)
        
        if routed is None:
            if verbose:
                print(f"\n  t={t}: SATURATION - cannot route {ob}")
            break
        
        active_routed.append(routed)
        
        # New load after routing
        new_load = compute_load_from_routed(active_routed)
        
        # Accumulate action
        action += transition_cost(prev_load, new_load, interfaces)
        prev_load = new_load
        
        # Periodic relaxation to compute residual
        if (t + 1) % relax_every == 0 or t == len(obligation_stream) - 1:
            raw_cost = total_cost(new_load, interfaces)
            
            # Relax: reroute everything to minimize cost
            relaxed_routed, residual_load = relax_routing(network, active_routed)
            active_routed = relaxed_routed  # Use relaxed routing going forward
            
            # Compute Î› metrics
            lambda_E = total_cost(residual_load, interfaces)
            lambda_sigma, bottleneck = residual_fraction(residual_load, interfaces)
            savings = raw_cost - lambda_E
            
            state = LambdaState(
                time_step=t,
                raw_load=new_load,
                raw_cost=raw_cost,
                residual_load=residual_load,
                lambda_E=lambda_E,
                lambda_sigma=lambda_sigma,
                bottleneck=bottleneck,
                action=action,
                relaxation_savings=savings
            )
            
            history.append(state)
            
            if verbose:
                status = "âœ“" if is_admissible(residual_load, interfaces) else "âœ—"
                print(f"  t={t}: {status} Î›_E={lambda_E:.2f}, Î›_Ïƒ={lambda_sigma:.1%}, "
                      f"saved={savings:.2f}, bn={bottleneck}")
    
    return history


# =============================================================================
# EXAMPLES
# =============================================================================

def example_lambda_emergence():
    """Demonstrate Î› emerging as irreducible residual."""
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘  EXAMPLE: Lambda Emergence                                           â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    # Create network
    I1 = Interface("I1", capacity=12.0, epsilon=1.0, eta=0.4)
    I2 = Interface("I2", capacity=10.0, epsilon=1.2, eta=0.5)
    I3 = Interface("I3", capacity=15.0, epsilon=0.8, eta=0.3)
    
    network = Network(
        nodes=["A", "B", "C", "D"],
        edges=[
            Edge("A", "B", I1),
            Edge("B", "C", I2),
            Edge("C", "D", I3),
            Edge("A", "C", I2),  # Alternative route
            Edge("B", "D", I3),  # Alternative route
            Edge("A", "D", I1),  # Direct route
        ]
    )
    
    print("\nNetwork:")
    for e in network.edges:
        print(f"  {e.u} â†” {e.v} via {e.interface.name} "
              f"(C={e.interface.capacity}, N_max={e.interface.max_n()})")
    
    # Create obligation stream: repeatedly demand Aâ†”D correlations
    obligations = [
        Obligation(id=i, source="A", target="D", demand=1)
        for i in range(15)
    ]
    
    history = estimate_lambda_floor(network, obligations, relax_every=2)
    
    # Analysis
    print("\n" + "-" * 40)
    print("Î› FLOOR ANALYSIS")
    print("-" * 40)
    
    if history:
        print(f"\n{'Step':>6} {'Î›_E':>8} {'Î›_Ïƒ':>8} {'Action':>10} {'Saved':>8}")
        print("-" * 46)
        
        for s in history:
            print(f"{s.time_step:>6} {s.lambda_E:>8.2f} {s.lambda_sigma:>7.1%} "
                  f"{s.action:>10.2f} {s.relaxation_savings:>8.2f}")
        
        # Show evolution
        print("\nKey observations:")
        
        if len(history) >= 2:
            lambda_growth = history[-1].lambda_E - history[0].lambda_E
            print(f"  - Î›_E grew from {history[0].lambda_E:.2f} to {history[-1].lambda_E:.2f}")
            print(f"  - Total Î› growth: {lambda_growth:.2f}")
            
            total_savings = sum(s.relaxation_savings for s in history)
            print(f"  - Total relaxation savings: {total_savings:.2f}")
            
            if history[-1].lambda_sigma > 0.8:
                print(f"  - âš ï¸  Near saturation (Î›_Ïƒ = {history[-1].lambda_sigma:.0%})")
    
    return history


def example_lambda_with_competition():
    """Demonstrate Î› under competing obligations."""
    print("\n" + "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘  EXAMPLE: Lambda with Competing Obligations                          â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    # Network with a bottleneck
    I_wide = Interface("wide", capacity=20.0, epsilon=0.8, eta=0.2)
    I_narrow = Interface("narrow", capacity=6.0, epsilon=1.0, eta=0.5)
    
    network = Network(
        nodes=["A", "B", "C"],
        edges=[
            Edge("A", "B", I_wide),
            Edge("B", "C", I_narrow),  # Bottleneck!
            Edge("A", "C", I_wide),
        ]
    )
    
    print("\nNetwork with bottleneck:")
    print("  A â•â•wideâ•â• B â”€â”€narrowâ”€â”€ C")
    print("   â•²                    â•±")
    print("    â•²â•â•â•â•â•â•wideâ•â•â•â•â•â•â•â•±")
    print(f"\n  narrow: C={I_narrow.capacity}, N_max={I_narrow.max_n()}")
    print(f"  wide: C={I_wide.capacity}, N_max={I_wide.max_n()}")
    
    # Obligations that compete for the bottleneck
    obligations = []
    for i in range(12):
        if i % 2 == 0:
            obligations.append(Obligation(id=i, source="A", target="C", demand=1))
        else:
            obligations.append(Obligation(id=i, source="B", target="C", demand=1))
    
    print(f"\nObligation stream: alternating Aâ†”C and Bâ†”C demands")
    
    history = estimate_lambda_floor(network, obligations, relax_every=2)
    
    # Show how Î› concentrates at the bottleneck
    print("\n" + "-" * 40)
    print("BOTTLENECK ANALYSIS")
    print("-" * 40)
    
    if history:
        narrow_loads = []
        for s in history:
            narrow_loads.append(s.residual_load["narrow"])
        
        print(f"\nLoad on 'narrow' interface over time:")
        for s in history:
            load_narrow = s.residual_load["narrow"]
            load_wide = s.residual_load["wide"]
            bar = "â–ˆ" * load_narrow + "â–‘" * (I_narrow.max_n() - load_narrow)
            print(f"  t={s.time_step}: narrow=[{bar}] {load_narrow}, wide={load_wide}")
        
        print(f"\n  â†’ Î› concentrates at bottleneck: {history[-1].bottleneck}")
    
    return history


def example_lambda_saturation():
    """Show Î› behavior at saturation."""
    print("\n" + "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘  EXAMPLE: Lambda at Saturation                                       â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    # Small capacity network
    I1 = Interface("I1", capacity=8.0, epsilon=1.0, eta=0.5)
    
    network = Network(
        nodes=["A", "B"],
        edges=[Edge("A", "B", I1)]
    )
    
    N_max = I1.max_n()
    print(f"\nSimple Aâ†”B network with C={I1.capacity}, N_max={N_max}")
    
    # Try to add more obligations than capacity allows
    obligations = [
        Obligation(id=i, source="A", target="B", demand=1)
        for i in range(N_max + 3)
    ]
    
    history = estimate_lambda_floor(network, obligations, relax_every=1)
    
    print("\n" + "-" * 40)
    print("SATURATION BEHAVIOR")
    print("-" * 40)
    
    if history:
        print(f"\n{'Step':>6} {'Load':>6} {'Î›_Ïƒ':>8} {'Headroom':>10}")
        print("-" * 36)
        
        for s in history:
            load = s.residual_load["I1"]
            headroom = I1.headroom(load)
            bar = "â–ˆ" * load + "â–‘" * max(0, N_max - load)
            print(f"{s.time_step:>6} {load:>6} {s.lambda_sigma:>7.1%} {headroom:>10.2f}  [{bar}]")
        
        print(f"\n  Saturation hit after {len(history)} obligations")
        print(f"  Final Î›_Ïƒ = {history[-1].lambda_sigma:.0%}")
        print(f"  â†’ Beyond this, no admissible dynamics exists")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘                       LAMBDA FLOOR ENGINE                            â•‘")
    print("â•‘                                                                      â•‘")
    print("â•‘  Î› = Irreducible Residual Enforcement Cost                           â•‘")
    print("â•‘  (What remains after optimal rerouting)                              â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    example_lambda_emergence()
    example_lambda_with_competition()
    example_lambda_saturation()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: LAMBDA AS CAPACITY FLOOR")
    print("=" * 70)
    print("""
KEY RESULTS:

1. Î› DEFINITION
   Î› = total_cost(L_residual)
   where L_residual = argmin over admissible reroutings
   
   Î› is NOT what you add. Î› is what REMAINS.

2. Î› METRICS
   - Î›_E: Total residual enforcement cost
   - Î›_Ïƒ: Saturation fraction at bottleneck
   - Relaxation savings: cost eliminated by rerouting

3. Î› BEHAVIOR
   - Early time: relaxation removes most cost (Î› small)
   - Later: residual grows, cannot be rerouted away
   - At saturation: Î›_Ïƒ â†’ 1, dynamics blocked

4. PHYSICAL INTERPRETATION
   - Î› = "cosmological constant" of enforcement
   - Represents commitments that cannot be locally discharged
   - Grows as records accumulate
   - Sets the floor for any dynamical trajectory

UNIFICATION COMPLETE:
  Enforceability â†’ Admissibility â†’ Composability 
           â†’ Geometry â†’ Time â†’ Î›
  
  All from enforcement cost minimization.
""")


if __name__ == "__main__":
    main()

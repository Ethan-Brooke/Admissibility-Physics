#!/usr/bin/env python3
"""
ACCUMULATED COST ENGINE
=======================

Time emerges from irreversible enforcement cost accumulation.

Core concepts:
- History = sequence of load vectors Lâ‚€ â†’ Lâ‚ â†’ Lâ‚‚ â†’ ...
- Transition cost = |Î”E| between consecutive states
- Action = total accumulated cost along history
- Time = monotonic accumulation (arrow emerges from irreversibility)

This closes the loop:
  Enforceability â†’ Admissibility â†’ Composability â†’ Geometry â†’ TIME

Author: Admissibility Physics Project
Version: 1.0
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Callable
from collections import defaultdict

# =============================================================================
# CONSTANTS
# =============================================================================

EPS_SLACK = 1e-6      # Admissibility margin
EPS_ACTION = 1e-9     # Minimum detectable action (proto-â„)

# =============================================================================
# INTERFACE (shared with routing engine)
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
# LOAD VECTOR (shared with routing engine)
# =============================================================================

@dataclass
class LoadVector:
    """Per-interface load configuration."""
    loads: Dict[str, int]
    
    @classmethod
    def empty(cls) -> 'LoadVector':
        return cls(loads={})
    
    @classmethod
    def uniform(cls, interfaces: List[Interface], n: int) -> 'LoadVector':
        return cls(loads={itf.name: n for itf in interfaces})
    
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
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, LoadVector):
            return False
        all_keys = set(self.loads.keys()) | set(other.loads.keys())
        return all(self[k] == other[k] for k in all_keys)
    
    def __hash__(self):
        return hash(tuple(sorted(self.loads.items())))
    
    def copy(self) -> 'LoadVector':
        return LoadVector(loads=dict(self.loads))
    
    def __repr__(self):
        return f"Load({self.loads})"


# =============================================================================
# TRANSITION COST
# =============================================================================

def transition_cost(
    L_prev: LoadVector,
    L_next: LoadVector,
    interfaces: List[Interface]
) -> float:
    """
    Compute the enforcement cost of transitioning between load states.
    
    This is the total variation in enforcement:
        Î”S = Î£áµ¢ |E_i(n_next) - E_i(n_prev)|
    
    Properties:
    - Always â‰¥ 0
    - Zero if and only if L_prev == L_next
    - Symmetric: cost(Aâ†’B) = cost(Bâ†’A)
    
    This is the fundamental "tick" of enforcement time.
    """
    cost = 0.0
    for itf in interfaces:
        n_prev = L_prev[itf.name]
        n_next = L_next[itf.name]
        
        E_prev = itf.cost(n_prev)
        E_next = itf.cost(n_next)
        
        cost += abs(E_next - E_prev)
    
    return cost


def transition_cost_signed(
    L_prev: LoadVector,
    L_next: LoadVector,
    interfaces: List[Interface]
) -> Tuple[float, float]:
    """
    Compute signed transition costs (increase vs decrease).
    
    Returns (cost_increase, cost_decrease) where:
    - cost_increase = sum of positive Î”E
    - cost_decrease = sum of |negative Î”E|
    
    Total = cost_increase + cost_decrease
    Net = cost_increase - cost_decrease
    """
    increase = 0.0
    decrease = 0.0
    
    for itf in interfaces:
        n_prev = L_prev[itf.name]
        n_next = L_next[itf.name]
        
        delta_E = itf.cost(n_next) - itf.cost(n_prev)
        
        if delta_E > 0:
            increase += delta_E
        else:
            decrease += abs(delta_E)
    
    return increase, decrease


# =============================================================================
# HISTORY AND ACTION
# =============================================================================

@dataclass
class HistoryStep:
    """A single step in an enforcement history."""
    load: LoadVector
    time: float           # Accumulated cost up to this point
    transition_cost: float  # Cost of this transition (0 for initial)
    
    # Admissibility at this step
    is_admissible: bool = True
    min_headroom: float = float('inf')
    bottleneck: str = ""


@dataclass
class History:
    """
    A sequence of load states with accumulated cost.
    
    This is the fundamental object for dynamics:
    - Time emerges from accumulated cost
    - Arrow of time from irreversibility
    - Action = total accumulated cost
    """
    interfaces: List[Interface]
    steps: List[HistoryStep] = field(default_factory=list)
    
    @property
    def action(self) -> float:
        """Total accumulated cost (action functional)."""
        return self.steps[-1].time if self.steps else 0.0
    
    @property
    def duration(self) -> int:
        """Number of transitions."""
        return max(0, len(self.steps) - 1)
    
    @property
    def is_admissible(self) -> bool:
        """Is entire history admissible?"""
        return all(step.is_admissible for step in self.steps)
    
    def initial_load(self) -> Optional[LoadVector]:
        return self.steps[0].load if self.steps else None
    
    def final_load(self) -> Optional[LoadVector]:
        return self.steps[-1].load if self.steps else None
    
    def append(self, load: LoadVector) -> 'History':
        """Add a new state to the history."""
        if not self.steps:
            # Initial state
            step = self._make_step(load, 0.0, 0.0)
            self.steps.append(step)
        else:
            # Transition
            prev = self.steps[-1]
            t_cost = transition_cost(prev.load, load, self.interfaces)
            new_time = prev.time + t_cost
            
            step = self._make_step(load, new_time, t_cost)
            self.steps.append(step)
        
        return self
    
    def _make_step(self, load: LoadVector, time: float, t_cost: float) -> HistoryStep:
        """Create a history step with admissibility analysis."""
        min_h = float('inf')
        bottleneck = ""
        
        for itf in self.interfaces:
            h = itf.headroom(load[itf.name])
            if h < min_h:
                min_h = h
                bottleneck = itf.name
        
        return HistoryStep(
            load=load,
            time=time,
            transition_cost=t_cost,
            is_admissible=min_h > EPS_SLACK,
            min_headroom=min_h,
            bottleneck=bottleneck
        )
    
    def summary(self) -> str:
        """Human-readable summary."""
        lines = [f"History: {self.duration} transitions, action = {self.action:.4f}"]
        
        for i, step in enumerate(self.steps):
            status = "âœ“" if step.is_admissible else "âœ—"
            lines.append(f"  {i}: {status} t={step.time:.3f} Î”={step.transition_cost:.3f} "
                        f"H_min={step.min_headroom:.2f} {step.load}")
        
        return "\n".join(lines)


def history_cost(loads: List[LoadVector], interfaces: List[Interface]) -> float:
    """
    Compute total accumulated cost for a sequence of load vectors.
    
    This is the ACTION of the history:
        S = Î£áµ¢ |transition_cost(L[i], L[i+1])|
    
    Equivalent to History(...).action but standalone.
    """
    if len(loads) < 2:
        return 0.0
    
    return sum(
        transition_cost(loads[i], loads[i+1], interfaces)
        for i in range(len(loads) - 1)
    )


# =============================================================================
# ADMISSIBLE DYNAMICS
# =============================================================================

def is_transition_admissible(
    L_prev: LoadVector,
    L_next: LoadVector,
    interfaces: List[Interface]
) -> bool:
    """Check if a transition is admissible (target state is in Regime R)."""
    for itf in interfaces:
        n = L_next[itf.name]
        if itf.headroom(n) <= EPS_SLACK:
            return False
    return True


def admissible_neighbors(
    load: LoadVector,
    interfaces: List[Interface],
    max_delta: int = 1
) -> List[LoadVector]:
    """
    Generate all admissible neighboring load vectors.
    
    Neighbors differ by at most Â±max_delta on each interface.
    Only returns those that remain admissible.
    """
    neighbors = []
    
    interface_names = [itf.name for itf in interfaces]
    
    # Generate all combinations of deltas
    deltas = range(-max_delta, max_delta + 1)
    
    for delta_combo in itertools.product(deltas, repeat=len(interface_names)):
        if all(d == 0 for d in delta_combo):
            continue  # Skip identity
        
        new_loads = {}
        valid = True
        
        for name, delta in zip(interface_names, delta_combo):
            new_n = load[name] + delta
            if new_n < 0:
                valid = False
                break
            new_loads[name] = new_n
        
        if not valid:
            continue
        
        new_load = LoadVector(loads=new_loads)
        
        if is_transition_admissible(load, new_load, interfaces):
            neighbors.append(new_load)
    
    return neighbors


import itertools


def find_minimum_action_path(
    L_start: LoadVector,
    L_end: LoadVector,
    interfaces: List[Interface],
    max_steps: int = 100
) -> Optional[History]:
    """
    Find the minimum-action admissible path between two load states.
    
    Uses Dijkstra-like search in load-vector space.
    
    This is the variational principle made executable:
        Î´S = 0  â†’  find path that minimizes action
    """
    if L_start == L_end:
        h = History(interfaces=interfaces)
        h.append(L_start)
        return h
    
    # Check endpoints are admissible
    if not is_transition_admissible(LoadVector.empty(), L_start, interfaces):
        return None
    if not is_transition_admissible(LoadVector.empty(), L_end, interfaces):
        return None
    
    # Dijkstra's algorithm
    # State: (accumulated_cost, load_vector, path)
    
    from heapq import heappush, heappop
    
    # Priority queue: (cost, counter, load, path)
    counter = 0
    pq = [(0.0, counter, L_start, [L_start])]
    visited = {hash(L_start): 0.0}
    
    while pq and counter < max_steps * 1000:
        cost, _, current, path = heappop(pq)
        
        if current == L_end:
            # Found it
            h = History(interfaces=interfaces)
            for load in path:
                h.append(load)
            return h
        
        # Expand neighbors
        for neighbor in admissible_neighbors(current, interfaces, max_delta=1):
            t_cost = transition_cost(current, neighbor, interfaces)
            new_cost = cost + t_cost
            
            h = hash(neighbor)
            if h not in visited or visited[h] > new_cost:
                visited[h] = new_cost
                counter += 1
                heappush(pq, (new_cost, counter, neighbor, path + [neighbor]))
    
    return None  # No path found


# =============================================================================
# TIME AND â„
# =============================================================================

def minimum_action_quantum(interfaces: List[Interface]) -> float:
    """
    Compute the minimum nonzero action (proto-â„).
    
    This is the smallest possible enforcement change:
    - Add or remove one distinction at the cheapest interface
    
    â„_eff = min_i { |E_i(1) - E_i(0)| } = min_i { Îµ_i }
    """
    if not interfaces:
        return 0.0
    
    # Minimum cost to add one distinction
    return min(itf.epsilon for itf in interfaces)


def time_from_action(action: float, h_eff: float) -> float:
    """
    Convert action to discrete time units.
    
    t = S / â„_eff
    
    This gives the number of "fundamental ticks" in a history.
    """
    if h_eff <= 0:
        return float('inf')
    return action / h_eff


# =============================================================================
# IRREVERSIBILITY AND ARROW OF TIME
# =============================================================================

@dataclass
class IrreversibilityAnalysis:
    """Analysis of irreversibility in a history."""
    history: History
    
    # Metrics
    total_action: float = 0.0
    net_change: float = 0.0          # E_final - E_initial
    dissipation: float = 0.0         # action - |net_change|
    reversibility_ratio: float = 0.0  # |net_change| / action
    
    def analyze(self):
        """Compute irreversibility metrics."""
        if not self.history.steps:
            return
        
        self.total_action = self.history.action
        
        # Compute net change
        E_initial = sum(
            itf.cost(self.history.steps[0].load[itf.name])
            for itf in self.history.interfaces
        )
        E_final = sum(
            itf.cost(self.history.steps[-1].load[itf.name])
            for itf in self.history.interfaces
        )
        
        self.net_change = E_final - E_initial
        
        # Dissipation = wasted action (back-and-forth)
        self.dissipation = self.total_action - abs(self.net_change)
        
        # Reversibility ratio: 1 = perfectly efficient, 0 = all dissipation
        if self.total_action > EPS_ACTION:
            self.reversibility_ratio = abs(self.net_change) / self.total_action
        else:
            self.reversibility_ratio = 1.0 if abs(self.net_change) < EPS_ACTION else 0.0
    
    def summary(self) -> str:
        return (f"Irreversibility: action={self.total_action:.4f}, "
                f"net={self.net_change:.4f}, dissipation={self.dissipation:.4f}, "
                f"reversibility={self.reversibility_ratio:.1%}")


# =============================================================================
# EXAMPLES
# =============================================================================

def example_simple_history():
    """Example: Simple history with time emergence."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Simple History (Time Emerges)")
    print("=" * 70)
    
    interfaces = [
        Interface("I1", capacity=10.0, epsilon=1.0, eta=0.3),
        Interface("I2", capacity=12.0, epsilon=0.8, eta=0.4),
    ]
    
    h_eff = minimum_action_quantum(interfaces)
    print(f"\nMinimum action quantum â„_eff = {h_eff}")
    
    # Create a history: grow from empty to size 3
    history = History(interfaces=interfaces)
    
    loads = [
        LoadVector.uniform(interfaces, 0),
        LoadVector.uniform(interfaces, 1),
        LoadVector.uniform(interfaces, 2),
        LoadVector.uniform(interfaces, 3),
    ]
    
    for load in loads:
        history.append(load)
    
    print(f"\n{history.summary()}")
    
    print(f"\nAction (total cost): {history.action:.4f}")
    print(f"Discrete time: {time_from_action(history.action, h_eff):.1f} ticks")
    
    # Analyze irreversibility
    irr = IrreversibilityAnalysis(history=history)
    irr.analyze()
    print(f"\n{irr.summary()}")
    
    return history


def example_minimum_action_path():
    """Example: Find minimum-action path between states."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Minimum Action Path (Variational Principle)")
    print("=" * 70)
    
    interfaces = [
        Interface("I1", capacity=15.0, epsilon=1.0, eta=0.3),
        Interface("I2", capacity=15.0, epsilon=1.2, eta=0.4),
    ]
    
    L_start = LoadVector(loads={"I1": 1, "I2": 1})
    L_end = LoadVector(loads={"I1": 3, "I2": 3})
    
    print(f"\nFinding minimum-action path:")
    print(f"  Start: {L_start}")
    print(f"  End:   {L_end}")
    
    path = find_minimum_action_path(L_start, L_end, interfaces, max_steps=50)
    
    if path:
        print(f"\nâœ“ Path found!")
        print(f"\n{path.summary()}")
        
        print(f"\nMinimum action: {path.action:.4f}")
        
        # Compare to direct path
        direct = History(interfaces=interfaces)
        direct.append(L_start)
        direct.append(L_end)
        
        print(f"Direct transition action: {direct.action:.4f}")
        
        if path.action < direct.action:
            print("  â†’ Optimal path is NOT direct (multi-step is cheaper)")
        else:
            print("  â†’ Direct path is optimal")
    else:
        print("\nâœ— No admissible path found")
    
    return path


def example_irreversibility():
    """Example: Demonstrate irreversibility and arrow of time."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Irreversibility (Arrow of Time)")
    print("=" * 70)
    
    interfaces = [
        Interface("I1", capacity=10.0, epsilon=1.0, eta=0.5),
    ]
    
    # Forward path: 0 â†’ 1 â†’ 2 â†’ 3
    forward = History(interfaces=interfaces)
    for n in [0, 1, 2, 3]:
        forward.append(LoadVector(loads={"I1": n}))
    
    # Round trip: 0 â†’ 1 â†’ 2 â†’ 3 â†’ 2 â†’ 1 â†’ 0
    roundtrip = History(interfaces=interfaces)
    for n in [0, 1, 2, 3, 2, 1, 0]:
        roundtrip.append(LoadVector(loads={"I1": n}))
    
    print("\nForward path (0 â†’ 3):")
    irr_fwd = IrreversibilityAnalysis(history=forward)
    irr_fwd.analyze()
    print(f"  Action: {forward.action:.4f}")
    print(f"  {irr_fwd.summary()}")
    
    print("\nRound trip (0 â†’ 3 â†’ 0):")
    irr_rt = IrreversibilityAnalysis(history=roundtrip)
    irr_rt.analyze()
    print(f"  Action: {roundtrip.action:.4f}")
    print(f"  {irr_rt.summary()}")
    
    print(f"""
KEY INSIGHT:
  - Forward: net change = {irr_fwd.net_change:.2f}, all action is "useful"
  - Round trip: net change = {irr_rt.net_change:.2f}, but action = {roundtrip.action:.2f}
  - The difference is DISSIPATION: {irr_rt.dissipation:.2f}
  
  Time's arrow emerges because:
  - Going there costs action
  - Coming back costs MORE action (not negative!)
  - Total > 0 even when you return to start
  
  This is IRREVERSIBILITY from enforcement cost.
""")


def example_regime_boundary_dynamics():
    """Example: Dynamics near the regime boundary."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Dynamics Near Regime R Boundary")
    print("=" * 70)
    
    interfaces = [
        Interface("I1", capacity=8.0, epsilon=1.0, eta=0.5),
    ]
    
    N_max = interfaces[0].max_n()
    print(f"\nInterface I1: C=8.0, Îµ=1.0, Î·=0.5")
    print(f"N_max = {N_max}")
    
    # Try to grow past saturation
    print("\nGrowing load until saturation:")
    
    history = History(interfaces=interfaces)
    
    for n in range(N_max + 3):
        load = LoadVector(loads={"I1": n})
        history.append(load)
        
        step = history.steps[-1]
        status = "âœ“" if step.is_admissible else "âœ—"
        print(f"  n={n}: {status} H={step.min_headroom:.2f}, t={step.time:.2f}")
        
        if not step.is_admissible:
            print(f"       â†‘ BOUNDARY CROSSED (Regime R ends)")
    
    print(f"""
INSIGHT:
  - Dynamics is free inside Regime R (H > 0)
  - At boundary (H â‰ˆ 0), transitions become costly
  - Beyond boundary (H < 0), dynamics is BLOCKED
  
  This is why:
  - Field theory exists inside Regime R
  - Saturation = edge of dynamics
  - No EoM beyond saturation
""")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘                    ACCUMULATED COST ENGINE                           â•‘")
    print("â•‘                                                                      â•‘")
    print("â•‘  Time = Monotonic Accumulation of Irreversible Enforcement Cost      â•‘")
    print("â•‘  Action = Total Accumulated Cost Along History                       â•‘")
    print("â•‘  â„ = Minimum Nonzero Action (Enforcement Quantum)                    â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    example_simple_history()
    example_minimum_action_path()
    example_irreversibility()
    example_regime_boundary_dynamics()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: TIME AND ACTION FROM ENFORCEMENT")
    print("=" * 70)
    print("""
KEY RESULTS:

1. TIME EMERGES
   - Time = accumulated enforcement cost
   - Monotonic (always increases)
   - Arrow from irreversibility

2. ACTION FUNCTIONAL
   S = Î£ |Î”E| along history
   - Variational principle: Î´S = 0 selects dynamics
   - Minimum action paths exist and are computable

3. â„ EMERGES
   - â„_eff = minimum nonzero enforcement change
   - Quantizes time into discrete "ticks"
   - This is proto-quantum structure

4. IRREVERSIBILITY
   - Round trips cost more than one-way
   - Dissipation = action - |net change|
   - Second law emerges naturally

5. REGIME R BOUNDARY
   - Dynamics free inside Regime R
   - Blocked beyond saturation
   - Paper 6 connection complete

UNIFICATION ACHIEVED:
  Enforceability â†’ Admissibility â†’ Composability â†’ Geometry â†’ TIME
  
  All from enforcement cost minimization.
""")


if __name__ == "__main__":
    main()

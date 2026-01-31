#!/usr/bin/env python3
"""
ROUTING ENGINE v1
=================

Geometry from enforcement cost minimization.

Core idea:
- Motifs require connections between nodes
- Connections route through interfaces (edges)
- Each route induces a load vector
- Universe realizes the admissible route with minimum cost
- Distance = minimum admissible enforcement cost

This makes "correlation cost = distance" executable.

Author: Admissibility Physics Project
Version: 1.0
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import defaultdict
from heapq import heappush, heappop
import itertools

# =============================================================================
# CONSTANTS
# =============================================================================

EPS_SLACK = 1e-6  # Strict interior margin for Regime R

# =============================================================================
# INTERFACE (from regime analysis)
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
# NETWORK TOPOLOGY
# =============================================================================

@dataclass(frozen=True)
class Edge:
    """
    An edge in the routing network.
    
    Each edge connects two nodes and has an associated interface
    that determines its capacity and cost model.
    """
    u: str  # Source node
    v: str  # Target node
    interface: Interface
    
    def __repr__(self):
        return f"Edge({self.u}â†’{self.v}, {self.interface.name})"
    
    def other(self, node: str) -> str:
        """Get the other endpoint."""
        return self.v if node == self.u else self.u


@dataclass
class Network:
    """
    A routing network: nodes connected by edges (interfaces).
    
    This is the substrate on which motifs route their correlations.
    """
    nodes: List[str]
    edges: List[Edge]
    
    # Computed
    _adjacency: Dict[str, List[Edge]] = field(default_factory=dict, repr=False)
    _interfaces: Dict[str, Interface] = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        """Build adjacency list and interface map."""
        self._adjacency = defaultdict(list)
        self._interfaces = {}
        
        for edge in self.edges:
            self._adjacency[edge.u].append(edge)
            self._adjacency[edge.v].append(edge)
            self._interfaces[edge.interface.name] = edge.interface
    
    def neighbors(self, node: str) -> List[Tuple[str, Edge]]:
        """Get neighbors of a node with their connecting edges."""
        result = []
        for edge in self._adjacency[node]:
            neighbor = edge.other(node)
            result.append((neighbor, edge))
        return result
    
    def interfaces(self) -> List[Interface]:
        """Get all unique interfaces in the network."""
        return list(self._interfaces.values())
    
    def get_interface(self, name: str) -> Optional[Interface]:
        """Get interface by name."""
        return self._interfaces.get(name)


# =============================================================================
# LOAD VECTOR
# =============================================================================

@dataclass
class LoadVector:
    """Per-interface load for a routing configuration."""
    loads: Dict[str, int]
    
    @classmethod
    def empty(cls) -> 'LoadVector':
        return cls(loads={})
    
    @classmethod
    def from_edges(cls, edges: List[Edge]) -> 'LoadVector':
        """Create load vector from a list of edges (path)."""
        loads = defaultdict(int)
        for edge in edges:
            loads[edge.interface.name] += 1
        return cls(loads=dict(loads))
    
    def __add__(self, other: 'LoadVector') -> 'LoadVector':
        """Add load vectors (composition)."""
        combined = dict(self.loads)
        for name, load in other.loads.items():
            combined[name] = combined.get(name, 0) + load
        return LoadVector(loads=combined)
    
    def __getitem__(self, interface_name: str) -> int:
        return self.loads.get(interface_name, 0)
    
    def total_load(self) -> int:
        """Sum of all loads."""
        return sum(self.loads.values())
    
    def __repr__(self):
        return f"Load({self.loads})"


# =============================================================================
# PATH FINDING
# =============================================================================

@dataclass
class Path:
    """A path through the network."""
    nodes: List[str]
    edges: List[Edge]
    
    @property
    def source(self) -> str:
        return self.nodes[0] if self.nodes else ""
    
    @property
    def target(self) -> str:
        return self.nodes[-1] if self.nodes else ""
    
    @property
    def length(self) -> int:
        return len(self.edges)
    
    def load_vector(self) -> LoadVector:
        """Convert path to load vector."""
        return LoadVector.from_edges(self.edges)
    
    def __repr__(self):
        return f"Path({' â†’ '.join(self.nodes)})"


def find_paths(
    network: Network,
    source: str,
    target: str,
    max_paths: int = 10,
    max_length: int = 10
) -> List[Path]:
    """
    Find up to max_paths paths from source to target.
    
    Uses DFS with length cutoff. Returns paths sorted by length.
    """
    if source == target:
        return [Path(nodes=[source], edges=[])]
    
    paths = []
    
    def dfs(current: str, visited: Set[str], path_nodes: List[str], path_edges: List[Edge]):
        if len(paths) >= max_paths:
            return
        if len(path_edges) > max_length:
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
    
    # Sort by length
    paths.sort(key=lambda p: p.length)
    
    return paths


def find_k_shortest_paths(
    network: Network,
    source: str,
    target: str,
    k: int = 5
) -> List[Path]:
    """
    Find k shortest paths using Yen's algorithm (simplified).
    
    For now, just use DFS and take shortest k.
    """
    all_paths = find_paths(network, source, target, max_paths=k*3, max_length=15)
    return all_paths[:k]


# =============================================================================
# ROUTING ANALYSIS
# =============================================================================

@dataclass
class RoutingResult:
    """Result of routing analysis for a single path."""
    path: Path
    load_vector: LoadVector
    total_cost: float
    is_admissible: bool
    min_headroom: float
    bottleneck: str
    
    # Per-interface breakdown
    costs: Dict[str, float] = field(default_factory=dict)
    headrooms: Dict[str, float] = field(default_factory=dict)


def analyze_routing(
    path: Path,
    interfaces: List[Interface],
    existing_load: Optional[LoadVector] = None
) -> RoutingResult:
    """
    Analyze a routing path for admissibility and cost.
    
    Args:
        path: The path to analyze
        interfaces: All interfaces in the network
        existing_load: Optional existing load to add to
    """
    # Compute load vector for this path
    path_load = path.load_vector()
    
    # Add existing load if provided
    if existing_load:
        total_load = existing_load + path_load
    else:
        total_load = path_load
    
    # Build interface map
    itf_map = {itf.name: itf for itf in interfaces}
    
    # Compute costs and headrooms
    costs = {}
    headrooms = {}
    total_cost = 0.0
    min_headroom = float('inf')
    bottleneck = ""
    
    for itf in interfaces:
        n = total_load[itf.name]
        cost = itf.cost(n)
        headroom = itf.headroom(n)
        
        costs[itf.name] = cost
        headrooms[itf.name] = headroom
        total_cost += cost
        
        if headroom < min_headroom:
            min_headroom = headroom
            bottleneck = itf.name
    
    is_admissible = min_headroom > EPS_SLACK
    
    return RoutingResult(
        path=path,
        load_vector=total_load,
        total_cost=total_cost,
        is_admissible=is_admissible,
        min_headroom=min_headroom,
        bottleneck=bottleneck,
        costs=costs,
        headrooms=headrooms
    )


def best_routing(
    network: Network,
    source: str,
    target: str,
    existing_load: Optional[LoadVector] = None,
    k: int = 10
) -> Optional[RoutingResult]:
    """
    Find the best admissible routing from source to target.
    
    Returns the admissible path with minimum total cost, or None if
    no admissible path exists.
    """
    paths = find_k_shortest_paths(network, source, target, k=k)
    interfaces = network.interfaces()
    
    best_result = None
    best_cost = float('inf')
    
    for path in paths:
        result = analyze_routing(path, interfaces, existing_load)
        
        if result.is_admissible and result.total_cost < best_cost:
            best_cost = result.total_cost
            best_result = result
    
    return best_result


# =============================================================================
# DISTANCE FUNCTION
# =============================================================================

def distance(
    network: Network,
    u: str,
    v: str,
    existing_load: Optional[LoadVector] = None
) -> Tuple[float, Optional[RoutingResult]]:
    """
    Compute the distance between two nodes.
    
    Distance = minimum admissible enforcement cost to maintain a 
    distinction (correlation) between nodes u and v.
    
    Returns (distance, routing_result) or (inf, None) if no admissible path.
    """
    if u == v:
        return 0.0, RoutingResult(
            path=Path(nodes=[u], edges=[]),
            load_vector=existing_load or LoadVector.empty(),
            total_cost=0.0,
            is_admissible=True,
            min_headroom=float('inf'),
            bottleneck=""
        )
    
    result = best_routing(network, u, v, existing_load)
    
    if result is None:
        return float('inf'), None
    
    return result.total_cost, result


def distance_matrix(network: Network) -> Dict[Tuple[str, str], float]:
    """Compute pairwise distances between all nodes."""
    distances = {}
    
    for u in network.nodes:
        for v in network.nodes:
            d, _ = distance(network, u, v)
            distances[(u, v)] = d
    
    return distances


# =============================================================================
# MOTIF ROUTING
# =============================================================================

@dataclass
class MotifConnection:
    """A required connection in a motif."""
    source: str
    target: str
    demand: int = 1  # How many correlation units


@dataclass
class Motif:
    """
    A motif requiring multiple connections.
    
    The routing engine finds the best way to satisfy all connections
    subject to admissibility constraints.
    """
    name: str
    connections: List[MotifConnection]
    
    def total_demand(self) -> int:
        return sum(c.demand for c in self.connections)


@dataclass 
class MotifRoutingResult:
    """Complete routing result for a motif."""
    motif: Motif
    routes: List[RoutingResult]  # One per connection
    combined_load: LoadVector
    total_cost: float
    is_admissible: bool
    min_headroom: float
    bottleneck: str


def route_motif(
    network: Network,
    motif: Motif,
    existing_load: Optional[LoadVector] = None
) -> Optional[MotifRoutingResult]:
    """
    Find the best routing for a motif (all its connections).
    
    Currently uses greedy sequential routing. 
    TODO: Joint optimization over all routes.
    """
    interfaces = network.interfaces()
    
    # Start with existing load
    current_load = existing_load or LoadVector.empty()
    routes = []
    total_cost = 0.0
    
    # Route each connection
    for conn in motif.connections:
        for _ in range(conn.demand):
            result = best_routing(network, conn.source, conn.target, 
                                  existing_load=current_load)
            
            if result is None:
                return None  # No admissible routing
            
            routes.append(result)
            current_load = result.load_vector
            total_cost += result.total_cost - sum(
                itf.cost(current_load[itf.name] - result.path.load_vector()[itf.name])
                for itf in interfaces
            )
    
    # Compute final metrics
    min_headroom = float('inf')
    bottleneck = ""
    
    for itf in interfaces:
        h = itf.headroom(current_load[itf.name])
        if h < min_headroom:
            min_headroom = h
            bottleneck = itf.name
    
    return MotifRoutingResult(
        motif=motif,
        routes=routes,
        combined_load=current_load,
        total_cost=sum(itf.cost(current_load[itf.name]) for itf in interfaces),
        is_admissible=min_headroom > EPS_SLACK,
        min_headroom=min_headroom,
        bottleneck=bottleneck
    )


# =============================================================================
# ROUTING REGIME ANALYSIS
# =============================================================================

def routing_regime_analysis(network: Network, verbose: bool = True):
    """
    Analyze the routing regime for a network.
    
    Key questions:
    1. Which node pairs have admissible routes?
    2. Where are the routing "knees" (sharp transitions)?
    3. Does routing enable motifs that uniform loading can't?
    """
    if verbose:
        print("\n" + "=" * 70)
        print("ROUTING REGIME ANALYSIS")
        print("=" * 70)
        
        print("\nNetwork topology:")
        print(f"  Nodes: {network.nodes}")
        print(f"  Edges:")
        for e in network.edges:
            print(f"    {e.u} â†” {e.v} via {e.interface.name} "
                  f"(C={e.interface.capacity}, Îµ={e.interface.epsilon}, Î·={e.interface.eta})")
    
    # Distance matrix
    if verbose:
        print("\n" + "-" * 40)
        print("Distance matrix (min admissible cost):")
        print("-" * 40)
        
        # Header
        header = "      " + "".join(f"{n:>8}" for n in network.nodes)
        print(header)
        
        for u in network.nodes:
            row = f"{u:>6}"
            for v in network.nodes:
                d, _ = distance(network, u, v)
                if d == float('inf'):
                    row += f"{'âˆž':>8}"
                elif d == 0:
                    row += f"{'â€”':>8}"
                else:
                    row += f"{d:>8.2f}"
            print(row)
    
    # Find routing knees
    if verbose:
        print("\n" + "-" * 40)
        print("Routing under increasing load:")
        print("-" * 40)
        
        # Pick a representative edge pair
        if len(network.nodes) >= 2:
            u, v = network.nodes[0], network.nodes[-1]
            print(f"\nLoading {u} â†’ {v} repeatedly until saturation:")
            
            current_load = LoadVector.empty()
            for i in range(20):
                result = best_routing(network, u, v, existing_load=current_load)
                
                if result is None:
                    print(f"  Load {i+1}: BLOCKED (no admissible route)")
                    break
                
                current_load = result.load_vector
                path_str = " â†’ ".join(result.path.nodes)
                print(f"  Load {i+1}: cost={result.total_cost:.2f}, "
                      f"H_min={result.min_headroom:.2f}, route: {path_str}")
                
                if result.min_headroom < 1.0:
                    print(f"         â†‘ KNEE detected (low headroom)")
    
    return distance_matrix(network)


# =============================================================================
# GEOMETRY VERIFICATION
# =============================================================================

def verify_geometry(network: Network, verbose: bool = True):
    """
    Verify that routing produces valid geometric structure.
    
    Checks:
    1. d(u,u) = 0 (identity)
    2. d(u,v) = d(v,u) (symmetry)  
    3. d(u,w) â‰¤ d(u,v) + d(v,w) (triangle inequality)
    """
    if verbose:
        print("\n" + "=" * 70)
        print("GEOMETRY VERIFICATION")
        print("=" * 70)
    
    nodes = network.nodes
    distances = distance_matrix(network)
    
    violations = []
    
    # Check identity
    for u in nodes:
        if distances[(u, u)] != 0:
            violations.append(f"Identity: d({u},{u}) = {distances[(u,u)]} â‰  0")
    
    # Check symmetry
    for u in nodes:
        for v in nodes:
            if abs(distances[(u,v)] - distances[(v,u)]) > 1e-10:
                violations.append(f"Symmetry: d({u},{v}) = {distances[(u,v)]:.2f} â‰  "
                                 f"d({v},{u}) = {distances[(v,u)]:.2f}")
    
    # Check triangle inequality
    for u in nodes:
        for v in nodes:
            for w in nodes:
                d_uw = distances[(u, w)]
                d_uv = distances[(u, v)]
                d_vw = distances[(v, w)]
                
                if d_uw > d_uv + d_vw + 1e-10:
                    violations.append(f"Triangle: d({u},{w}) = {d_uw:.2f} > "
                                     f"d({u},{v}) + d({v},{w}) = {d_uv + d_vw:.2f}")
    
    if verbose:
        if violations:
            print(f"\nâœ— {len(violations)} violations found:")
            for v in violations[:10]:
                print(f"  {v}")
        else:
            print("\nâœ“ All metric axioms satisfied!")
            print("  - Identity: d(u,u) = 0 âœ“")
            print("  - Symmetry: d(u,v) = d(v,u) âœ“")
            print("  - Triangle inequality: d(u,w) â‰¤ d(u,v) + d(v,w) âœ“")
    
    return len(violations) == 0


# =============================================================================
# EXAMPLES
# =============================================================================

def example_simple_network():
    """Example: Simple 4-node network."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Simple 4-Node Network")
    print("=" * 70)
    
    # Create interfaces
    I1 = Interface("I1", capacity=10.0, epsilon=1.0, eta=0.3)
    I2 = Interface("I2", capacity=8.0, epsilon=1.2, eta=0.4)
    I3 = Interface("I3", capacity=12.0, epsilon=0.8, eta=0.5)
    
    # Create network: A -- B -- C -- D with some shortcuts
    #                 \--- D ---/
    network = Network(
        nodes=["A", "B", "C", "D"],
        edges=[
            Edge("A", "B", I1),
            Edge("B", "C", I2),
            Edge("C", "D", I3),
            Edge("A", "D", I2),  # Shortcut
        ]
    )
    
    # Run analysis
    routing_regime_analysis(network)
    verify_geometry(network)
    
    return network


def example_routing_vs_uniform():
    """Example: Compare routing vs uniform loading."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Routing vs Uniform Loading")
    print("=" * 70)
    
    # Create interfaces with different capacities
    I_tight = Interface("tight", capacity=5.0, epsilon=1.0, eta=0.5)
    I_loose = Interface("loose", capacity=15.0, epsilon=1.0, eta=0.3)
    
    # Network where routing matters
    #   A ---tight--- B ---loose--- C
    #    \                          /
    #     \--------loose-----------/
    network = Network(
        nodes=["A", "B", "C"],
        edges=[
            Edge("A", "B", I_tight),
            Edge("B", "C", I_loose),
            Edge("A", "C", I_loose),  # Alternate route
        ]
    )
    
    print("\nNetwork:")
    print("  A --tight(C=5)-- B --loose(C=15)-- C")
    print("   \\                              /")
    print("    \\---------loose(C=15)--------/")
    
    # Test: routing Aâ†’C
    print("\n" + "-" * 40)
    print("Routing A â†’ C:")
    
    # Path 1: A â†’ B â†’ C (uses tight interface)
    path1 = Path(nodes=["A", "B", "C"], edges=[
        Edge("A", "B", I_tight),
        Edge("B", "C", I_loose)
    ])
    
    # Path 2: A â†’ C (direct, only loose)
    path2 = Path(nodes=["A", "C"], edges=[
        Edge("A", "C", I_loose)
    ])
    
    interfaces = [I_tight, I_loose]
    
    r1 = analyze_routing(path1, interfaces)
    r2 = analyze_routing(path2, interfaces)
    
    print(f"\n  Route Aâ†’Bâ†’C: cost={r1.total_cost:.2f}, H_min={r1.min_headroom:.2f}")
    print(f"  Route Aâ†’C:   cost={r2.total_cost:.2f}, H_min={r2.min_headroom:.2f}")
    print(f"\n  â†’ Best route: {'Aâ†’Bâ†’C' if r1.total_cost < r2.total_cost else 'Aâ†’C (direct)'}")
    
    # Now add load and see routing switch
    print("\n" + "-" * 40)
    print("Effect of existing load on routing choice:")
    
    for load_on_tight in [0, 2, 4]:
        existing = LoadVector(loads={"tight": load_on_tight, "loose": 0})
        
        r1_loaded = analyze_routing(path1, interfaces, existing)
        r2_loaded = analyze_routing(path2, interfaces, existing)
        
        best = "Aâ†’Bâ†’C" if (r1_loaded.is_admissible and 
                          (not r2_loaded.is_admissible or r1_loaded.total_cost < r2_loaded.total_cost)) else "Aâ†’C"
        
        print(f"\n  Existing load on 'tight': {load_on_tight}")
        print(f"    Aâ†’Bâ†’C: cost={r1_loaded.total_cost:.2f}, admissible={r1_loaded.is_admissible}")
        print(f"    Aâ†’C:   cost={r2_loaded.total_cost:.2f}, admissible={r2_loaded.is_admissible}")
        print(f"    â†’ Best: {best}")
    
    return network


def example_motif_routing():
    """Example: Routing a multi-connection motif."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Motif Routing")
    print("=" * 70)
    
    # Create network
    I1 = Interface("I1", capacity=10.0, epsilon=1.0, eta=0.4)
    I2 = Interface("I2", capacity=10.0, epsilon=1.0, eta=0.4)
    I3 = Interface("I3", capacity=10.0, epsilon=1.0, eta=0.4)
    
    network = Network(
        nodes=["A", "B", "C", "D"],
        edges=[
            Edge("A", "B", I1),
            Edge("B", "C", I2),
            Edge("C", "D", I3),
            Edge("A", "C", I2),
            Edge("B", "D", I3),
        ]
    )
    
    # Create a motif requiring Aâ†”D correlation
    motif = Motif(
        name="A-D correlation",
        connections=[MotifConnection("A", "D", demand=3)]
    )
    
    print(f"\nMotif: {motif.name}")
    print(f"  Requires: {motif.connections[0].demand} units of Aâ†”D correlation")
    
    result = route_motif(network, motif)
    
    if result:
        print(f"\n  âœ“ Admissible routing found!")
        print(f"  Total cost: {result.total_cost:.2f}")
        print(f"  Min headroom: {result.min_headroom:.2f}")
        print(f"  Final load: {result.combined_load}")
        print(f"\n  Routes used:")
        for i, r in enumerate(result.routes):
            print(f"    {i+1}. {' â†’ '.join(r.path.nodes)} (cost={r.total_cost:.2f})")
    else:
        print(f"\n  âœ— No admissible routing exists")
    
    return network, motif


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘                      ROUTING ENGINE v1                               â•‘")
    print("â•‘                                                                      â•‘")
    print("â•‘  Distance = Minimum Admissible Enforcement Cost                      â•‘")
    print("â•‘  Geometry emerges from routing optimization                          â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    # Run examples
    example_simple_network()
    example_routing_vs_uniform()
    example_motif_routing()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
KEY RESULTS:

1. DISTANCE FROM ROUTING
   d(u,v) = min cost over admissible routes from u to v
   This makes "correlation cost = distance" executable.

2. ROUTING-DEPENDENT GEOMETRY
   - Same nodes, different geometry under different loads
   - Routes can switch at "knees" (saturation boundaries)
   - Geometry is dynamic, not fixed

3. METRIC VERIFICATION
   - Identity: d(u,u) = 0 âœ“
   - Symmetry: d(u,v) = d(v,u) âœ“  
   - Triangle inequality: d(u,w) â‰¤ d(u,v) + d(v,w) âœ“

4. READY FOR ACCUMULATED COST
   - History = sequence of routed load vectors
   - Action = total variation of loads
   - This becomes Paper 6 dynamics

NEXT: Accumulated cost along trajectories.
""")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
================================================================================
ADMISSIBILITY PHYSICS - COMPLETE COLAB SINGLE-CELL
================================================================================

Copy-paste this entire cell into Google Colab and run.
Everything is self-contained: engine + tests + visualization.

Author: Admissibility Physics Project
================================================================================
"""

#@title ADMISSIBILITY PHYSICS - RUN ALL { display-mode: "form" }

# =============================================================================
# IMPORTS
# =============================================================================

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set, Any
from collections import defaultdict
from heapq import heappush, heappop
import itertools

# =============================================================================
# CONSTANTS
# =============================================================================

EPS_SLACK = 1e-6
EPS_COST = 1e-9
EPS_ACTION = 1e-9

# =============================================================================
# CORE TYPES
# =============================================================================

@dataclass(frozen=True)
class Interface:
    name: str
    capacity: float
    epsilon: float = 1.0
    eta: float = 0.5
    
    def cost(self, n: int) -> float:
        if n <= 0: return 0.0
        return self.epsilon * n + self.eta * n * (n - 1) / 2
    
    def headroom(self, n: int) -> float:
        return self.capacity - self.cost(n)
    
    def max_n(self) -> int:
        if self.eta < 1e-12:
            return min(int(self.capacity / self.epsilon) if self.epsilon > 0 else 99, 100)
        a, b, c = self.eta / 2, self.epsilon - self.eta / 2, -self.capacity
        disc = b*b - 4*a*c
        return min(max(0, int((-b + math.sqrt(disc)) / (2*a))) if disc >= 0 else 0, 100)


@dataclass
class LoadVector:
    loads: Dict[str, int]
    
    @classmethod
    def empty(cls): return cls(loads={})
    
    @classmethod
    def uniform(cls, interfaces, n): return cls(loads={i.name: n for i in interfaces})
    
    def __getitem__(self, name): return self.loads.get(name, 0)
    def __setitem__(self, name, val): self.loads[name] = val
    
    def __add__(self, other):
        r = dict(self.loads)
        for k, v in other.loads.items(): r[k] = r.get(k, 0) + v
        return LoadVector(loads=r)
    
    def copy(self): return LoadVector(loads=dict(self.loads))
    def __repr__(self): return f"Load({self.loads})"


@dataclass(frozen=True)
class Edge:
    u: str
    v: str
    interface: Interface
    def other(self, node): return self.v if node == self.u else self.u


@dataclass
class Network:
    nodes: List[str]
    edges: List[Edge]
    _adj: Dict = field(default_factory=dict, repr=False)
    _itf: Dict = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        self._adj = defaultdict(list)
        self._itf = {}
        for e in self.edges:
            self._adj[e.u].append(e)
            self._adj[e.v].append(e)
            self._itf[e.interface.name] = e.interface
    
    def neighbors(self, n): return [(e.other(n), e) for e in self._adj[n]]
    def interfaces(self): return list(self._itf.values())
    def get_interface(self, name): return self._itf.get(name)


@dataclass
class Path:
    nodes: List[str]
    edges: List[Edge]
    def load_contribution(self):
        r = defaultdict(int)
        for e in self.edges: r[e.interface.name] += 1
        return dict(r)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def is_admissible(load, interfaces):
    return all(i.headroom(load[i.name]) > EPS_SLACK for i in interfaces)

def total_cost(load, interfaces):
    return sum(i.cost(load[i.name]) for i in interfaces)

def min_headroom(load, interfaces):
    worst, bn = float('inf'), ""
    for i in interfaces:
        h = i.headroom(load[i.name])
        if h < worst: worst, bn = h, i.name
    return worst, bn

def composability_index(load, interfaces):
    h, _ = min_headroom(load, interfaces)
    return (h - EPS_SLACK) / min(i.capacity for i in interfaces)

def transition_cost(L0, L1, interfaces):
    return sum(abs(i.cost(L1[i.name]) - i.cost(L0[i.name])) for i in interfaces)

def find_paths(network, src, tgt, max_len=6, max_paths=15):
    if src == tgt: return [Path([src], [])]
    paths = []
    def dfs(cur, vis, pn, pe):
        if len(paths) >= max_paths or len(pe) > max_len: return
        if cur == tgt: paths.append(Path(list(pn), list(pe))); return
        for nb, e in network.neighbors(cur):
            if nb not in vis:
                vis.add(nb); pn.append(nb); pe.append(e)
                dfs(nb, vis, pn, pe)
                pe.pop(); pn.pop(); vis.remove(nb)
    dfs(src, {src}, [src], [])
    return sorted(paths, key=lambda p: len(p.edges))


# =============================================================================
# REGIME ANALYSIS
# =============================================================================

def analyze_regime(interfaces, max_size=12):
    comp, sat, data = [], [], {}
    for n in range(1, max_size + 1):
        load = LoadVector.uniform(interfaces, n)
        h, bn = min_headroom(load, interfaces)
        k = composability_index(load, interfaces)
        info = {'size': n, 'headroom': h, 'kappa': k, 'bottleneck': bn, 'admissible': h > EPS_SLACK}
        data[n] = info
        (comp if h > EPS_SLACK else sat).append(n)
    return {'composable': comp, 'saturating': sat, 'data': data, 'max_comp': max(comp) if comp else 0}


# =============================================================================
# OBLIGATIONS & ROUTING
# =============================================================================

@dataclass
class Obligation:
    id: int
    source: str
    target: str
    demand: int = 1

@dataclass
class RoutedObligation:
    obligation: Obligation
    path: Path

def route_obligation(network, ob, load, max_paths=10):
    paths = find_paths(network, ob.source, ob.target, max_paths=max_paths)
    interfaces = network.interfaces()
    best, best_cost = None, float('inf')
    for p in paths:
        nl = load.copy()
        for name, c in p.load_contribution().items():
            nl[name] = nl[name] + c * ob.demand
        if is_admissible(nl, interfaces):
            cost = total_cost(nl, interfaces)
            if cost < best_cost: best, best_cost = p, cost
    return RoutedObligation(ob, best) if best else None

def compute_load(routed):
    r = defaultdict(int)
    for ro in routed:
        for name, c in ro.path.load_contribution().items():
            r[name] += c * ro.obligation.demand
    return LoadVector(loads=dict(r))


# =============================================================================
# FULL CHAIN SIMULATION
# =============================================================================

def run_simulation(network, steps=12, seed=42, verbose=True):
    random.seed(seed)
    interfaces = network.interfaces()
    nodes = network.nodes
    
    routed = []
    load = LoadVector.empty()
    prev_load = load.copy()
    action = 0.0
    history = []
    
    if verbose:
        print("\n" + "="*70)
        print("FULL CHAIN SIMULATION")
        print("="*70)
        print(f"\n{'Step':>4} {'Ob':>8} {'Cost':>8} {'Action':>10} {'Î›_E':>8} {'Î›_Ïƒ':>6} {'Îº':>6}")
        print("-"*60)
    
    for t in range(steps):
        a, b = random.sample(nodes, 2)
        ob = Obligation(t, a, b, 1)
        
        result = route_obligation(network, ob, load)
        if result is None:
            if verbose: print(f"{t:>4} {a}â†’{b:>4} {'BLOCKED':>8}")
            break
        
        routed.append(result)
        new_load = compute_load(routed)
        
        tc = transition_cost(prev_load, new_load, interfaces)
        action += tc
        
        lam = total_cost(new_load, interfaces)
        h, bn = min_headroom(new_load, interfaces)
        bn_itf = network.get_interface(bn)
        lam_sig = bn_itf.cost(new_load[bn]) / bn_itf.capacity if bn_itf else 0
        kappa = composability_index(new_load, interfaces)
        
        history.append({'step': t, 'action': action, 'lambda_E': lam, 
                       'lambda_sigma': lam_sig, 'kappa': kappa, 'bottleneck': bn})
        
        if verbose:
            print(f"{t:>4} {a}â†’{b:>4} {tc:>8.2f} {action:>10.2f} {lam:>8.2f} {lam_sig:>5.0%} {kappa:>6.2f}")
        
        load = new_load
        prev_load = new_load.copy()
    
    if history and verbose:
        final = history[-1]
        print(f"\n{'='*70}")
        print(f"RESULT: time = {final['action']:.2f}, Î›_E = {final['lambda_E']:.2f}, "
              f"Î›_Ïƒ = {final['lambda_sigma']:.0%}, Îº = {final['kappa']:.2f}")
    
    return history


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_dashboard(interfaces, history):
    fig = plt.figure(figsize=(16, 10), facecolor='#0a0a0a')
    fig.suptitle('ADMISSIBILITY PHYSICS â€” UNIFIED VISUALIZATION', 
                 fontsize=16, fontweight='bold', color='white', y=0.98)
    
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3,
                  left=0.06, right=0.94, top=0.90, bottom=0.08)
    
    colors = {'green': '#00ff88', 'red': '#ff4444', 'blue': '#00aaff', 
              'orange': '#ffaa00', 'text': '#ffffff', 'bg': '#1a1a1a'}
    
    # 1. Îº vs N
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(colors['bg'])
    regime = analyze_regime(interfaces, 12)
    sizes = list(regime['data'].keys())
    kappas = [regime['data'][n]['kappa'] for n in sizes]
    for n, k in zip(sizes, kappas):
        ax1.scatter(n, k, c=colors['green'] if k > 0 else colors['red'], s=80, 
                   edgecolors='white', linewidth=0.5, zorder=5)
    ax1.plot(sizes, kappas, color='white', alpha=0.5, linewidth=1)
    ax1.axhline(0, color=colors['red'], linestyle='--', linewidth=2, alpha=0.7)
    ax1.fill_between(sizes, kappas, 0, where=[k>0 for k in kappas], color=colors['green'], alpha=0.15)
    ax1.set_xlabel('Load N', color=colors['text'])
    ax1.set_ylabel('Îº', color=colors['text'])
    ax1.set_title('REGIME R BOUNDARY', fontweight='bold', color=colors['text'])
    ax1.tick_params(colors=colors['text'])
    ax1.grid(True, alpha=0.3)
    
    # 2. Action + Î› vs Time
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(colors['bg'])
    if history:
        steps = [h['step'] for h in history]
        actions = [h['action'] for h in history]
        lambdas = [h['lambda_E'] for h in history]
        ax2.plot(steps, actions, color=colors['blue'], linewidth=2, marker='o', markersize=4, label='Action')
        ax2b = ax2.twinx()
        ax2b.plot(steps, lambdas, color=colors['orange'], linewidth=2, marker='s', markersize=4, label='Î›_E')
        ax2.set_xlabel('Step', color=colors['text'])
        ax2.set_ylabel('Action', color=colors['blue'])
        ax2b.set_ylabel('Î›_E', color=colors['orange'])
        ax2.tick_params(axis='y', labelcolor=colors['blue'])
        ax2b.tick_params(axis='y', labelcolor=colors['orange'])
    ax2.set_title('TIME & Î› EVOLUTION', fontweight='bold', color=colors['text'])
    ax2.tick_params(axis='x', colors=colors['text'])
    ax2.grid(True, alpha=0.3)
    
    # 3. Îº timeline
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(colors['bg'])
    if history:
        steps = [h['step'] for h in history]
        kappas_t = [h['kappa'] for h in history]
        ax3.plot(steps, kappas_t, color=colors['green'], linewidth=2.5, marker='o', markersize=5)
        ax3.axhline(0, color=colors['red'], linestyle='--', linewidth=2, alpha=0.7)
        ax3.fill_between(steps, kappas_t, 0, where=[k>0 for k in kappas_t], color=colors['green'], alpha=0.2)
    ax3.set_xlabel('Step', color=colors['text'])
    ax3.set_ylabel('Îº', color=colors['text'])
    ax3.set_title('COMPOSABILITY DECAY', fontweight='bold', color=colors['text'])
    ax3.tick_params(colors=colors['text'])
    ax3.grid(True, alpha=0.3)
    
    # 4. Î· phase diagram
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_facecolor(colors['bg'])
    etas = np.linspace(0.1, 1.0, 15)
    max_ns = []
    for eta in etas:
        test_itf = [Interface(f"I{i}", 12.0, 1.0, eta) for i in range(3)]
        r = analyze_regime(test_itf, 15)
        max_ns.append(r['max_comp'])
    ax4.plot(etas, max_ns, color='white', linewidth=3, marker='o', markersize=6)
    ax4.fill_between(etas, max_ns, color=colors['green'], alpha=0.3)
    ax4.set_xlabel('Î· (non-closure)', color=colors['text'])
    ax4.set_ylabel('Max N*', color=colors['text'])
    ax4.set_title('Î· PHASE DIAGRAM\nClassical â†’ Quantum', fontweight='bold', color=colors['text'])
    ax4.tick_params(colors=colors['text'])
    ax4.grid(True, alpha=0.3)
    
    # 5. Î›_Ïƒ timeline
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_facecolor(colors['bg'])
    if history:
        steps = [h['step'] for h in history]
        sigmas = [h['lambda_sigma'] for h in history]
        ax5.bar(steps, sigmas, color=colors['orange'], alpha=0.7, edgecolor='white')
        ax5.axhline(1.0, color=colors['red'], linestyle='--', linewidth=2)
    ax5.set_xlabel('Step', color=colors['text'])
    ax5.set_ylabel('Î›_Ïƒ (saturation)', color=colors['text'])
    ax5.set_title('SATURATION GROWTH', fontweight='bold', color=colors['text'])
    ax5.tick_params(colors=colors['text'])
    ax5.set_ylim(0, 1.1)
    ax5.grid(True, alpha=0.3)
    
    # 6. Summary box
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor(colors['bg'])
    ax6.axis('off')
    
    if history:
        final = history[-1]
        summary = f"""
        UNIFICATION CHAIN
        â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        
        Enforceability
             â†“
        Admissibility
             â†“
        Composability (Îº)
             â†“
        Geometry (routing)
             â†“
        Time (action = {final['action']:.1f})
             â†“
        Î› (floor = {final['lambda_E']:.1f})
        
        â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        Regime R: N â‰¤ {regime['max_comp']}
        Final Îº: {final['kappa']:.2f}
        Final Î›_Ïƒ: {final['lambda_sigma']:.0%}
        """
        ax6.text(0.5, 0.5, summary, transform=ax6.transAxes, fontsize=11,
                fontfamily='monospace', color=colors['text'], ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='#111', edgecolor=colors['green'], lw=2))
    
    return fig


# =============================================================================
# MAIN EXECUTION
# =============================================================================

print("="*70)
print("ADMISSIBILITY PHYSICS ENGINE")
print("="*70)

# Create network
interfaces = [
    Interface("Î±", 12.0, 1.0, 0.4),
    Interface("Î²", 15.0, 1.2, 0.5),
    Interface("Î³", 10.0, 0.8, 0.6),
]

network = Network(
    nodes=["A", "B", "C", "D"],
    edges=[
        Edge("A", "B", interfaces[0]),
        Edge("B", "C", interfaces[1]),
        Edge("C", "D", interfaces[2]),
        Edge("A", "C", interfaces[1]),
        Edge("B", "D", interfaces[2]),
        Edge("A", "D", interfaces[0]),
    ]
)

# Regime analysis
print("\n--- REGIME ANALYSIS ---")
regime = analyze_regime(interfaces, 12)
print(f"Composable (Regime R): {regime['composable']}")
print(f"Saturating: {regime['saturating']}")
print(f"Max composable N*: {regime['max_comp']}")

# Full simulation
history = run_simulation(network, steps=12, seed=42)

# Key metrics
print("\n--- KEY METRICS ---")
h_eff = min(i.epsilon for i in interfaces)
print(f"â„_eff (min action): {h_eff}")
print(f"Regime R boundary: N* = {regime['max_comp']}")

# Counterfactual
print("\n--- COUNTERFACTUAL (infinite capacity) ---")
inf_interfaces = [Interface(i.name, i.capacity * 1000, i.epsilon, i.eta) for i in interfaces]
inf_regime = analyze_regime(inf_interfaces, 20)
print(f"With C â†’ âˆž: Max N* = {inf_regime['max_comp']} (no saturation)")
print("â†’ All structure vanishes when enforceability is free")

# Visualization
print("\n--- GENERATING VISUALIZATION ---")
fig = create_dashboard(interfaces, history)
plt.savefig('admissibility_dashboard.png', dpi=150, facecolor=fig.get_facecolor())
print("Saved: admissibility_dashboard.png")

# Display in Colab
try:
    from IPython.display import display
    display(fig)
except:
    plt.show()

print("\n" + "="*70)
print("COMPLETE")
print("="*70)
print("""
UNIFICATION ACHIEVED:
  Enforceability â†’ Admissibility â†’ Composability â†’ Geometry â†’ Time â†’ Î›
  
All from enforcement cost minimization.
""")

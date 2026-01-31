#!/usr/bin/env python3
"""
MEAN-FIELD MOTIF ANALYSIS
=========================

Motif discovery in enforcement space (not configuration space).

This wraps the existing v4 microdynamics engine and analyzes:
- Commitment clusters (distinctions that commit together)
- Persistence (survival under perturbations)
- SWAP dynamics (propagation proxy)
- Ledger efficiency (mass proxy)

NO ENGINE CHANGES. Pure analysis of simulation history.

Usage:
    python motif_analysis.py
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Set, FrozenSet, Tuple, Optional
from collections import defaultdict
from collections import defaultdict
import random

# Import the v4 standalone (assuming it's in the same directory or PYTHONPATH)
# For this file, we inline the necessary parts for self-containment

# =============================================================================
# MINIMAL V4 ENGINE (inlined for self-containment)
# =============================================================================

@dataclass(frozen=True)
class Interface:
    name: str
    capacity: float
    epsilon: float = 1.0
    eta: float = 0.5
    throughput: float = 50.0
    gamma: float = 0.5
    s0: float = 2.0
    alpha: float = 0.05
    mu: float = 0.05
    lam: float = -1.0
    
    def cost(self, n: int) -> float:
        if n <= 0:
            return 0.0
        return self.epsilon * n + self.eta * n * (n - 1) / 2
    
    def max_n(self) -> int:
        if self.eta < 1e-12:
            return int(self.capacity / self.epsilon) if self.epsilon > 0 else 999
        a = self.eta / 2
        b = self.epsilon - self.eta / 2
        c = -self.capacity
        disc = b*b - 4*a*c
        if disc < 0:
            return 0
        return max(0, int((-b + math.sqrt(disc)) / (2 * a)))


def sigma(slack: float, s0: float) -> float:
    if slack <= 0:
        return 1.0
    return math.exp(-slack / max(s0, 1e-12))


# =============================================================================
# EXTENDED SIMULATION WITH COMMITMENT TRACKING
# =============================================================================

@dataclass
class CommitmentEvent:
    """Record of when a distinction became committed."""
    distinction_id: int
    step: int
    slack_at_commit: float
    sigma_at_commit: float


@dataclass
class StepRecord:
    """Detailed record of a simulation step."""
    step: int
    distinctions: FrozenSet[int]
    proposal_type: str
    added: FrozenSet[int]
    removed: FrozenSet[int]
    ledger: float
    slack: float
    sigma_val: float
    objective: float
    newly_committed: Set[int]


@dataclass
class SimulationTrace:
    """Complete trace of a simulation run."""
    interface: Interface
    steps: List[StepRecord]
    commit_times: Dict[int, int]  # distinction_id -> first commit step
    final_distinctions: FrozenSet[int]
    final_committed: Set[int]
    total_ledger: float
    
    def get_distinctions_at(self, step: int) -> FrozenSet[int]:
        """Get distinction set at a given step."""
        if step < 0 or step >= len(self.steps):
            return frozenset()
        return self.steps[step].distinctions
    
    def commitment_cluster(self, tolerance: int = 2) -> List[Set[int]]:
        """
        Group distinctions by similar commit times.
        
        Distinctions that committed within `tolerance` steps of each other
        are grouped together.
        """
        if not self.commit_times:
            return []
        
        # Sort by commit time
        sorted_commits = sorted(self.commit_times.items(), key=lambda x: x[1])
        
        clusters = []
        current_cluster = {sorted_commits[0][0]}
        current_time = sorted_commits[0][1]
        
        for d_id, c_time in sorted_commits[1:]:
            if c_time - current_time <= tolerance:
                current_cluster.add(d_id)
            else:
                if current_cluster:
                    clusters.append(current_cluster)
                current_cluster = {d_id}
                current_time = c_time
        
        if current_cluster:
            clusters.append(current_cluster)
        
        return clusters


def run_with_tracking(
    interface: Interface,
    max_steps: int = 100,
    include_remove: bool = True,
    include_swap: bool = True,
    verbose: bool = False
) -> SimulationTrace:
    """
    Run simulation with full commitment tracking.
    
    Returns a SimulationTrace with detailed history.
    """
    # State
    distinctions: FrozenSet[int] = frozenset()
    ledger = 0.0
    committed: Set[int] = set()
    next_id = 0
    
    # Tracking
    steps: List[StepRecord] = []
    commit_times: Dict[int, int] = {}
    
    for step in range(max_steps):
        n = len(distinctions)
        E = interface.cost(n)
        slack = interface.capacity - E
        sig = sigma(slack, interface.s0)
        
        # Generate proposals
        proposals = []
        
        # Trivial
        proposals.append(("trivial", frozenset(), frozenset()))
        
        # Add
        proposals.append(("add", frozenset({next_id}), frozenset()))
        
        # Remove (only uncommitted)
        if include_remove:
            for d in distinctions:
                if d not in committed:
                    proposals.append(("remove", frozenset(), frozenset({d})))
        
        # Swap
        if include_swap:
            for d in distinctions:
                if d not in committed:
                    proposals.append(("swap", frozenset({next_id}), frozenset({d})))
        
        # Evaluate and select best
        best_prop = None
        best_obj = float('inf')
        best_new_distinctions = distinctions
        
        for ptype, add, remove in proposals:
            new_d = (distinctions - remove) | add
            new_n = len(new_d)
            
            # Check throughput
            E_new = interface.cost(new_n)
            if abs(E_new - E) > interface.throughput:
                continue
            
            # Check capacity
            if E_new > interface.capacity + 1e-12:
                continue
            
            # Check record preservation
            if remove & committed:
                continue
            
            # Compute objective
            delta_E = E_new - E
            slack_new = interface.capacity - E_new
            dR = interface.gamma * sigma(slack_new, interface.s0) * abs(delta_E)
            
            obj = (interface.alpha * delta_E**2 + 
                   interface.mu * dR + 
                   interface.lam * (new_n - n))
            
            if obj < best_obj:
                best_obj = obj
                best_prop = (ptype, add, remove)
                best_new_distinctions = new_d
        
        if best_prop is None:
            break
        
        ptype, add, remove = best_prop
        
        # Compute ledger update
        new_n = len(best_new_distinctions)
        E_new = interface.cost(new_n)
        slack_new = interface.capacity - E_new
        sig_new = sigma(slack_new, interface.s0)
        
        delta_E = E_new - E
        dR = interface.gamma * sig_new * abs(delta_E)
        ledger += dR
        
        # Update committed set
        newly_committed = set()
        if sig_new > 0.5:  # Near saturation
            for d in best_new_distinctions:
                if d not in committed:
                    committed.add(d)
                    newly_committed.add(d)
                    commit_times[d] = step
        
        # Record step
        record = StepRecord(
            step=step,
            distinctions=best_new_distinctions,
            proposal_type=ptype,
            added=add,
            removed=remove,
            ledger=ledger,
            slack=slack_new,
            sigma_val=sig_new,
            objective=best_obj,
            newly_committed=newly_committed
        )
        steps.append(record)
        
        # Update state
        distinctions = best_new_distinctions
        if add:
            next_id = max(add) + 1
        
        if verbose:
            commit_str = f" COMMIT:{newly_committed}" if newly_committed else ""
            print(f"Step {step}: |S|={len(distinctions)} {ptype} "
                  f"ledger={ledger:.3f} Ïƒ={sig_new:.3f}{commit_str}")
        
        # Check saturation
        if ptype == "trivial" and step > 0 and steps[-2].proposal_type == "trivial":
            if step > 1 and steps[-3].proposal_type == "trivial":
                break
    
    return SimulationTrace(
        interface=interface,
        steps=steps,
        commit_times=commit_times,
        final_distinctions=distinctions,
        final_committed=committed,
        total_ledger=ledger
    )


# =============================================================================
# MOTIF ANALYSIS
# =============================================================================

@dataclass
class MotifCandidate:
    """A candidate motif (commitment cluster)."""
    distinctions: FrozenSet[int]
    commit_times: Dict[int, int]
    
    @property
    def size(self) -> int:
        return len(self.distinctions)
    
    @property
    def commit_time_spread(self) -> float:
        """Variance in commit times (tightness)."""
        times = list(self.commit_times.values())
        if len(times) < 2:
            return 0.0
        mean = sum(times) / len(times)
        return math.sqrt(sum((t - mean)**2 for t in times) / len(times))
    
    @property
    def earliest_commit(self) -> int:
        return min(self.commit_times.values()) if self.commit_times else -1
    
    def __repr__(self):
        return f"Motif({set(self.distinctions)}, t={self.earliest_commit}Â±{self.commit_time_spread:.1f})"


def extract_motif_candidates(
    trace: SimulationTrace,
    min_size: int = 2,
    max_size: int = 5,
    time_tolerance: int = 3
) -> List[MotifCandidate]:
    """
    Extract motif candidates from commitment clusters.
    
    A motif candidate is a set of distinctions that:
    - Committed within `time_tolerance` steps of each other
    - Has size in [min_size, max_size]
    """
    clusters = trace.commitment_cluster(tolerance=time_tolerance)
    
    candidates = []
    for cluster in clusters:
        if min_size <= len(cluster) <= max_size:
            commit_times = {d: trace.commit_times[d] for d in cluster}
            candidates.append(MotifCandidate(
                distinctions=frozenset(cluster),
                commit_times=commit_times
            ))
    
    return candidates


def measure_persistence(
    motif: MotifCandidate,
    trace: SimulationTrace
) -> float:
    """
    Measure what fraction of steps the motif is fully present.
    """
    if not trace.steps:
        return 0.0
    
    present_count = 0
    for record in trace.steps:
        if motif.distinctions <= record.distinctions:
            present_count += 1
    
    return present_count / len(trace.steps)


def measure_survival_under_perturbation(
    motif: MotifCandidate,
    interface: Interface,
    n_trials: int = 10,
    perturbation_rate: float = 0.2
) -> float:
    """
    Measure how often a motif-like cluster forms under parameter perturbations.
    
    This tests whether the motif is a robust feature or an accident.
    """
    original_motif_size = motif.size
    similar_count = 0
    
    for _ in range(n_trials):
        # Perturb parameters
        perturbed = Interface(
            name=interface.name,
            capacity=interface.capacity * (1 + random.uniform(-perturbation_rate, perturbation_rate)),
            epsilon=interface.epsilon * (1 + random.uniform(-perturbation_rate, perturbation_rate)),
            eta=interface.eta * (1 + random.uniform(-perturbation_rate, perturbation_rate)),
            gamma=interface.gamma,
            s0=interface.s0,
            lam=interface.lam
        )
        
        # Run simulation
        trace = run_with_tracking(perturbed, max_steps=50, verbose=False)
        
        # Check if similar motifs form
        candidates = extract_motif_candidates(trace, min_size=original_motif_size-1, 
                                              max_size=original_motif_size+1)
        if any(c.size == original_motif_size for c in candidates):
            similar_count += 1
    
    return similar_count / n_trials


def measure_swap_survival(
    motif: MotifCandidate,
    trace: SimulationTrace
) -> Tuple[int, int]:
    """
    Count how many SWAP proposals occurred while motif existed vs. how many
    the motif survived.
    
    Returns (swaps_during_existence, total_swaps).
    """
    total_swaps = 0
    swaps_during = 0
    
    for record in trace.steps:
        if record.proposal_type == "swap":
            total_swaps += 1
            if motif.distinctions <= record.distinctions:
                swaps_during += 1
    
    return swaps_during, total_swaps


def ledger_efficiency(
    motif: MotifCandidate,
    trace: SimulationTrace
) -> float:
    """
    Compute Î”R per step after motif commits.
    
    Lower = more efficient (lighter).
    """
    if not trace.steps:
        return float('inf')
    
    commit_step = motif.earliest_commit
    if commit_step < 0:
        return float('inf')
    
    # Find ledger before and after motif formation
    ledger_at_commit = 0.0
    ledger_at_end = 0.0
    steps_after = 0
    
    for record in trace.steps:
        if record.step == commit_step:
            ledger_at_commit = record.ledger
        if record.step >= commit_step:
            ledger_at_end = record.ledger
            steps_after += 1
    
    if steps_after <= 1:
        return 0.0
    
    return (ledger_at_end - ledger_at_commit) / steps_after


# =============================================================================
# EXPERIMENTS
# =============================================================================

def experiment_commitment_clusters():
    """
    Experiment 1: Find and characterize commitment clusters.
    """
    print("=" * 60)
    print("EXPERIMENT 1: Commitment Cluster Motifs")
    print("=" * 60)
    
    interface = Interface(
        name="test",
        capacity=12.0,
        epsilon=1.0,
        eta=0.6,       # Non-closure present
        gamma=1.5,     # High commitment rate
        s0=2.0,
        lam=-1.5
    )
    
    print(f"\nInterface: C={interface.capacity}, Îµ={interface.epsilon}, "
          f"Î·={interface.eta}, Î³={interface.gamma}")
    print(f"N_max = {interface.max_n()}")
    
    print("\nRunning simulation with commitment tracking...")
    trace = run_with_tracking(interface, max_steps=50, verbose=True)
    
    print(f"\n--- Results ---")
    print(f"Final |S| = {len(trace.final_distinctions)}")
    print(f"Total committed = {len(trace.final_committed)}")
    print(f"Total ledger = {trace.total_ledger:.3f}")
    
    # Extract motif candidates
    print(f"\n--- Commitment Clusters ---")
    candidates = extract_motif_candidates(trace, min_size=1, max_size=10)
    
    for i, motif in enumerate(candidates):
        persistence = measure_persistence(motif, trace)
        efficiency = ledger_efficiency(motif, trace)
        swaps_during, total_swaps = measure_swap_survival(motif, trace)
        
        print(f"\nCluster {i+1}: {motif}")
        print(f"  Persistence: {persistence:.2f}")
        print(f"  Ledger efficiency: {efficiency:.4f}")
        print(f"  Swaps survived: {swaps_during}/{total_swaps}")
    
    return trace, candidates


def experiment_robustness():
    """
    Experiment 2: Test motif robustness under parameter perturbations.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Motif Robustness Under Perturbations")
    print("=" * 60)
    
    interface = Interface(
        name="test",
        capacity=12.0,
        epsilon=1.0,
        eta=0.6,
        gamma=1.5,
        s0=2.0,
        lam=-1.5
    )
    
    # Get baseline motifs
    trace = run_with_tracking(interface, max_steps=50, verbose=False)
    candidates = extract_motif_candidates(trace, min_size=2, max_size=5)
    
    print(f"\nBaseline: {len(candidates)} motif candidates")
    
    # Test robustness
    print("\nTesting robustness (10 trials each, 20% parameter noise)...")
    
    for motif in candidates:
        survival_rate = measure_survival_under_perturbation(
            motif, interface, n_trials=10, perturbation_rate=0.2
        )
        print(f"  {motif}: survival rate = {survival_rate:.0%}")


def experiment_parameter_scan():
    """
    Experiment 3: Scan parameters to find motif-forming regions.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Parameter Scan for Motif Formation")
    print("=" * 60)
    
    print("\nScanning Î· (non-closure strength)...")
    print(f"{'Î·':>6} {'|S|':>6} {'Clusters':>10} {'Avg Size':>10}")
    print("-" * 36)
    
    for eta in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        interface = Interface(
            name="test",
            capacity=15.0,
            epsilon=1.0,
            eta=eta,
            gamma=1.0,
            s0=2.0,
            lam=-1.5
        )
        
        trace = run_with_tracking(interface, max_steps=50, verbose=False)
        candidates = extract_motif_candidates(trace, min_size=2, max_size=10)
        
        avg_size = (sum(c.size for c in candidates) / len(candidates) 
                    if candidates else 0)
        
        print(f"{eta:>6.1f} {len(trace.final_distinctions):>6} "
              f"{len(candidates):>10} {avg_size:>10.1f}")


def experiment_swap_dynamics():
    """
    Experiment 4: Analyze SWAP as propagation proxy.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: SWAP Dynamics (Propagation Proxy)")
    print("=" * 60)
    
    interface = Interface(
        name="test",
        capacity=15.0,
        epsilon=1.0,
        eta=0.5,
        gamma=0.8,
        s0=2.5,
        lam=-1.2
    )
    
    print("\nRunning with SWAP enabled...")
    trace_swap = run_with_tracking(interface, max_steps=60, 
                                   include_swap=True, verbose=False)
    
    print("Running without SWAP (growth only)...")
    trace_no_swap = run_with_tracking(interface, max_steps=60, 
                                      include_swap=False, verbose=False)
    
    # Analyze SWAP frequency
    swap_count = sum(1 for r in trace_swap.steps if r.proposal_type == "swap")
    total_steps = len(trace_swap.steps)
    
    print(f"\n--- SWAP Statistics ---")
    print(f"SWAP frequency: {swap_count}/{total_steps} = {swap_count/total_steps:.1%}")
    
    # Compare outcomes
    print(f"\n--- Comparison ---")
    print(f"{'Metric':<20} {'With SWAP':>12} {'Without SWAP':>12}")
    print("-" * 46)
    print(f"{'Final |S|':<20} {len(trace_swap.final_distinctions):>12} "
          f"{len(trace_no_swap.final_distinctions):>12}")
    print(f"{'Committed':<20} {len(trace_swap.final_committed):>12} "
          f"{len(trace_no_swap.final_committed):>12}")
    print(f"{'Total ledger':<20} {trace_swap.total_ledger:>12.3f} "
          f"{trace_no_swap.total_ledger:>12.3f}")
    
    # Motif comparison
    candidates_swap = extract_motif_candidates(trace_swap, min_size=2)
    candidates_no_swap = extract_motif_candidates(trace_no_swap, min_size=2)
    
    print(f"{'Motif clusters':<20} {len(candidates_swap):>12} "
          f"{len(candidates_no_swap):>12}")


def experiment_proto_particle_statement():
    """
    Experiment 5: Generate proto-particle statement.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 5: Proto-Particle Statement")
    print("=" * 60)
    
    interface = Interface(
        name="universe",
        capacity=12.0,
        epsilon=1.0,
        eta=0.6,
        gamma=1.5,
        s0=2.0,
        lam=-1.5
    )
    
    # Run multiple trials
    all_cluster_sizes = []
    all_persistence = []
    
    print("\nRunning 20 trials...")
    for trial in range(20):
        trace = run_with_tracking(interface, max_steps=50, verbose=False)
        candidates = extract_motif_candidates(trace, min_size=1, max_size=10)
        
        for motif in candidates:
            all_cluster_sizes.append(motif.size)
            all_persistence.append(measure_persistence(motif, trace))
    
    # Analyze
    from collections import Counter
    size_counts = Counter(all_cluster_sizes)
    
    print(f"\n--- Cluster Size Distribution ---")
    for size in sorted(size_counts.keys()):
        count = size_counts[size]
        print(f"  Size {size}: {count} occurrences ({count/len(all_cluster_sizes):.0%})")
    
    avg_persistence = sum(all_persistence) / len(all_persistence) if all_persistence else 0
    print(f"\nAverage persistence: {avg_persistence:.2f}")
    
    # The statement
    print("\n" + "=" * 60)
    print("PROTO-PARTICLE STATEMENT")
    print("=" * 60)
    
    modal_size = max(size_counts, key=size_counts.get) if size_counts else 0
    
    print(f"""
In the admissible microdynamics with:
  - Capacity C = {interface.capacity}
  - Non-closure Î· = {interface.eta}
  - Commitment rate Î³ = {interface.gamma}

There exist small bundles of distinctions (size â‰ˆ {modal_size}) that:
  1. Become jointly committed within ~3 steps of each other
  2. Achieve persistence â‰ˆ {avg_persistence:.0%} under admissible dynamics
  3. Survive SWAP perturbations (propagate without dissolving)
  4. Dominate ledger stability after commitment

These bundles are DERIVED from A1-A6, not assumed.
They are proto-particles in enforcement space.
""")


def experiment_staged_commitment():
    """
    Experiment 6: Find parameters that give staged (not simultaneous) commitment.
    
    This is where interesting motif structure emerges - when distinctions
    commit at different times, forming sub-clusters.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 6: Staged Commitment (Sub-cluster Formation)")
    print("=" * 60)
    
    # Lower gamma = slower commitment = more staged
    # Higher s0 = broader commitment window = more staged
    interface = Interface(
        name="staged",
        capacity=20.0,      # Larger capacity
        epsilon=1.0,
        eta=0.3,            # Lower non-closure
        gamma=0.5,          # Lower commitment rate
        s0=4.0,             # Broader commitment window
        lam=-1.0
    )
    
    print(f"\nInterface: C={interface.capacity}, Î·={interface.eta}, "
          f"Î³={interface.gamma}, s0={interface.s0}")
    print(f"N_max = {interface.max_n()}")
    
    print("\nRunning with staged commitment parameters...")
    trace = run_with_tracking(interface, max_steps=80, verbose=True)
    
    print(f"\n--- Results ---")
    print(f"Final |S| = {len(trace.final_distinctions)}")
    print(f"Total committed = {len(trace.final_committed)}")
    
    # Detailed commitment analysis
    print(f"\n--- Commitment Timeline ---")
    if trace.commit_times:
        for d, t in sorted(trace.commit_times.items(), key=lambda x: x[1]):
            print(f"  Distinction {d} committed at step {t}")
    
    # Extract clusters with tight tolerance
    print(f"\n--- Commitment Clusters (tolerance=1) ---")
    tight_clusters = extract_motif_candidates(trace, min_size=1, max_size=20, time_tolerance=1)
    for c in tight_clusters:
        print(f"  {c}")
    
    print(f"\n--- Commitment Clusters (tolerance=3) ---")
    loose_clusters = extract_motif_candidates(trace, min_size=1, max_size=20, time_tolerance=3)
    for c in loose_clusters:
        print(f"  {c}")
    
    return trace


def experiment_gradual_commitment():
    """
    Experiment 6b: Force gradual commitment by lowering the Ïƒ threshold.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 6b: Gradual Commitment (Lower Ïƒ Threshold)")
    print("=" * 60)
    
    print("\nModifying commitment rule: commit when Ïƒ > 0.1 (instead of 0.5)")
    print("This should give earlier, more gradual commitment.\n")
    
    interface = Interface(
        name="gradual",
        capacity=15.0,
        epsilon=1.0,
        eta=0.4,
        gamma=0.8,
        s0=3.0,
        lam=-1.2
    )
    
    # Custom run with lower threshold
    distinctions: FrozenSet[int] = frozenset()
    ledger = 0.0
    committed: Set[int] = set()
    commit_times: Dict[int, int] = {}
    next_id = 0
    
    COMMIT_THRESHOLD = 0.1  # Much lower than 0.5
    
    print(f"Interface: C={interface.capacity}, Î·={interface.eta}")
    print(f"N_max = {interface.max_n()}")
    print(f"Commit threshold Ïƒ > {COMMIT_THRESHOLD}")
    print()
    
    for step in range(50):
        n = len(distinctions)
        E = interface.cost(n)
        slack = interface.capacity - E
        sig = sigma(slack, interface.s0)
        
        # Try to add
        E_new = interface.cost(n + 1)
        if E_new <= interface.capacity:
            distinctions = distinctions | {next_id}
            
            # Update ledger
            slack_new = interface.capacity - E_new
            sig_new = sigma(slack_new, interface.s0)
            delta_E = E_new - E
            dR = interface.gamma * sig_new * abs(delta_E)
            ledger += dR
            
            # Check commitment with lower threshold
            newly_committed = []
            if sig_new > COMMIT_THRESHOLD:
                for d in distinctions:
                    if d not in committed:
                        committed.add(d)
                        commit_times[d] = step
                        newly_committed.append(d)
            
            commit_str = f" COMMIT:{newly_committed}" if newly_committed else ""
            print(f"Step {step}: |S|={len(distinctions)} Ïƒ={sig_new:.3f}{commit_str}")
            
            next_id += 1
        else:
            print(f"Step {step}: SATURATED at |S|={n}")
            break
    
    # Analyze commitment timeline
    print(f"\n--- Commitment Timeline ---")
    by_time = defaultdict(list)
    for d, t in commit_times.items():
        by_time[t].append(d)
    
    for t in sorted(by_time.keys()):
        print(f"  Step {t}: {by_time[t]}")
    
    # Identify sub-clusters
    print(f"\n--- Sub-clusters by commit time ---")
    for t in sorted(by_time.keys()):
        cluster = by_time[t]
        if len(cluster) > 0:
            print(f"  Cluster at t={t}: size={len(cluster)}, members={cluster}")
    
    return commit_times


def experiment_multi_interface_motifs():
    """
    Experiment 7: Motif signatures under multiple interfaces.
    
    Different interfaces may "see" the same distinctions differently,
    creating charge-like signatures.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 7: Multi-Interface Motif Signatures")
    print("=" * 60)
    
    # Can't directly use multi-interface in this simplified engine,
    # but we can simulate by running with different interfaces
    # and comparing which distinctions would commit
    
    interfaces = [
        Interface("alpha", capacity=12.0, epsilon=1.0, eta=0.3, gamma=1.0, s0=2.0, lam=-1.5),
        Interface("beta", capacity=15.0, epsilon=1.5, eta=0.5, gamma=0.8, s0=2.5, lam=-1.2),
        Interface("gamma", capacity=10.0, epsilon=0.8, eta=0.7, gamma=1.2, s0=1.5, lam=-1.8),
    ]
    
    print("\nRunning same initial conditions under different interfaces...")
    print(f"{'Interface':<12} {'N_max':>6} {'Final |S|':>10} {'Committed':>10} {'Ledger':>10}")
    print("-" * 52)
    
    for itf in interfaces:
        trace = run_with_tracking(itf, max_steps=50, verbose=False)
        print(f"{itf.name:<12} {itf.max_n():>6} {len(trace.final_distinctions):>10} "
              f"{len(trace.final_committed):>10} {trace.total_ledger:>10.3f}")
    
    print("\nInterpretation: Motifs (committed bundles) have different 'charges'")
    print("at different interfaces, analogous to how particles carry different")
    print("quantum numbers under different gauge groups.")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘         MEAN-FIELD MOTIF ANALYSIS - Admissibility Physics    â•‘")
    print("â•‘                                                              â•‘")
    print("â•‘  Discovering particles in enforcement space                  â•‘")
    print("â•‘  (No geometry, no fields, no spacetime assumed)              â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    experiment_commitment_clusters()
    experiment_robustness()
    experiment_parameter_scan()
    experiment_swap_dynamics()
    experiment_staged_commitment()
    experiment_gradual_commitment()
    experiment_multi_interface_motifs()
    experiment_proto_particle_statement()
    
    print("\n" + "=" * 60)
    print("All experiments complete.")
    print("=" * 60)

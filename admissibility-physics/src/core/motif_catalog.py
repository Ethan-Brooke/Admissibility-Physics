#!/usr/bin/env python3
"""
CANONICAL MOTIF CATALOG
=======================

Systematic survey of motifs across parameter space.

Produces the "periodic table" of admissible motifs:
- Size distribution
- Persistence by size
- Ledger efficiency (mass proxy)
- Interface signatures (charge proxy)
- Frequency of occurrence

Usage:
    python motif_catalog.py
    python motif_catalog.py --full  # Extended survey
"""

from __future__ import annotations
import math
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, FrozenSet, Tuple, Optional
from collections import defaultdict, Counter
import random
import sys

# Import the formal definition
from motif_definition import (
    COMMIT_WINDOW, PERSISTENCE_MIN, LEDGER_MAX, SIGMA_THRESHOLD,
    is_valid_motif
)

# =============================================================================
# MINIMAL ENGINE (inlined)
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
        return max(0, int((-b + math.sqrt(disc)) / (2 * a))) if disc >= 0 else 0


def sigma(slack: float, s0: float) -> float:
    if slack <= 0:
        return 1.0
    return math.exp(-slack / max(s0, 1e-12))


# =============================================================================
# CATALOG DATA STRUCTURES
# =============================================================================

@dataclass
class MotifRecord:
    """Record of a single motif observation."""
    size: int
    commit_time: int
    commit_spread: float
    persistence: float
    ledger_efficiency: float
    swap_survival: float
    interface_signature: Dict[str, float]
    is_valid: bool
    violations: List[str]
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CatalogEntry:
    """Aggregated statistics for a motif size class."""
    size: int
    count: int = 0
    valid_count: int = 0
    
    persistence_mean: float = 0.0
    persistence_std: float = 0.0
    
    ledger_mean: float = 0.0
    ledger_std: float = 0.0
    
    commit_spread_mean: float = 0.0
    
    signature_mean: Dict[str, float] = field(default_factory=dict)
    
    def update_from_records(self, records: List[MotifRecord]):
        """Compute statistics from a list of records."""
        if not records:
            return
        
        self.count = len(records)
        self.valid_count = sum(1 for r in records if r.is_valid)
        
        persistences = [r.persistence for r in records]
        self.persistence_mean = sum(persistences) / len(persistences)
        self.persistence_std = math.sqrt(
            sum((p - self.persistence_mean)**2 for p in persistences) / len(persistences)
        ) if len(persistences) > 1 else 0.0
        
        ledgers = [r.ledger_efficiency for r in records if r.ledger_efficiency < float('inf')]
        if ledgers:
            self.ledger_mean = sum(ledgers) / len(ledgers)
            self.ledger_std = math.sqrt(
                sum((l - self.ledger_mean)**2 for l in ledgers) / len(ledgers)
            ) if len(ledgers) > 1 else 0.0
        
        spreads = [r.commit_spread for r in records]
        self.commit_spread_mean = sum(spreads) / len(spreads)
        
        # Aggregate signatures
        all_interfaces = set()
        for r in records:
            all_interfaces |= set(r.interface_signature.keys())
        
        for itf in all_interfaces:
            sigs = [r.interface_signature.get(itf, 0) for r in records]
            self.signature_mean[itf] = sum(sigs) / len(sigs)


@dataclass
class MotifCatalog:
    """Complete catalog of motifs from a survey."""
    parameters: Dict[str, any]
    entries: Dict[int, CatalogEntry]  # size -> entry
    raw_records: List[MotifRecord]
    total_trials: int
    
    def to_dict(self) -> dict:
        return {
            "parameters": self.parameters,
            "total_trials": self.total_trials,
            "entries": {k: asdict(v) for k, v in self.entries.items()},
            "summary": self.summary()
        }
    
    def summary(self) -> dict:
        total_motifs = sum(e.count for e in self.entries.values())
        valid_motifs = sum(e.valid_count for e in self.entries.values())
        
        return {
            "total_motifs_observed": total_motifs,
            "valid_motifs": valid_motifs,
            "validity_rate": valid_motifs / total_motifs if total_motifs > 0 else 0,
            "size_distribution": {k: v.count for k, v in self.entries.items()},
            "most_common_size": max(self.entries.keys(), key=lambda k: self.entries[k].count) if self.entries else None
        }
    
    def print_table(self):
        """Print the catalog as a table."""
        print("\n" + "=" * 80)
        print("CANONICAL MOTIF CATALOG")
        print("=" * 80)
        
        print(f"\nParameters: {self.parameters}")
        print(f"Total trials: {self.total_trials}")
        
        summary = self.summary()
        print(f"Total motifs: {summary['total_motifs_observed']}")
        print(f"Valid motifs: {summary['valid_motifs']} ({summary['validity_rate']:.0%})")
        
        print(f"\n{'Size':>6} {'Count':>8} {'Valid':>8} {'P(mean)':>10} {'P(std)':>8} "
              f"{'L(mean)':>10} {'Spread':>8}")
        print("-" * 70)
        
        for size in sorted(self.entries.keys()):
            e = self.entries[size]
            print(f"{size:>6} {e.count:>8} {e.valid_count:>8} "
                  f"{e.persistence_mean:>10.3f} {e.persistence_std:>8.3f} "
                  f"{e.ledger_mean:>10.4f} {e.commit_spread_mean:>8.2f}")
        
        if any(e.signature_mean for e in self.entries.values()):
            print("\nInterface Signatures (mean):")
            all_itfs = set()
            for e in self.entries.values():
                all_itfs |= set(e.signature_mean.keys())
            
            header = f"{'Size':>6}" + "".join(f"{itf[:8]:>10}" for itf in sorted(all_itfs))
            print(header)
            print("-" * len(header))
            
            for size in sorted(self.entries.keys()):
                e = self.entries[size]
                row = f"{size:>6}"
                for itf in sorted(all_itfs):
                    row += f"{e.signature_mean.get(itf, 0):>10.2f}"
                print(row)


# =============================================================================
# SIMULATION WITH TRACKING
# =============================================================================

def run_trial(
    interface: Interface,
    max_steps: int = 100,
    commit_threshold: float = SIGMA_THRESHOLD
) -> Tuple[List[MotifRecord], Dict]:
    """
    Run a single trial and extract motif records.
    """
    distinctions: FrozenSet[int] = frozenset()
    ledger = 0.0
    committed: Set[int] = set()
    commit_times: Dict[int, int] = {}
    next_id = 0
    
    step_records = []
    
    for step in range(max_steps):
        n = len(distinctions)
        E = interface.cost(n)
        slack = interface.capacity - E
        sig = sigma(slack, interface.s0)
        
        # Try to add
        E_new = interface.cost(n + 1)
        delta_E = E_new - E
        
        # Check if admissible
        if E_new > interface.capacity or abs(delta_E) > interface.throughput:
            # Saturated
            step_records.append({
                'step': step, 'n': n, 'ledger': ledger, 
                'sigma': sig, 'action': 'saturated'
            })
            break
        
        # Add distinction
        distinctions = distinctions | {next_id}
        
        # Update ledger
        slack_new = interface.capacity - E_new
        sig_new = sigma(slack_new, interface.s0)
        dR = interface.gamma * sig_new * abs(delta_E)
        ledger += dR
        
        # Check commitment
        newly_committed = []
        if sig_new > commit_threshold:
            for d in distinctions:
                if d not in committed:
                    committed.add(d)
                    commit_times[d] = step
                    newly_committed.append(d)
        
        step_records.append({
            'step': step, 'n': len(distinctions), 'ledger': ledger,
            'sigma': sig_new, 'action': 'add', 'committed': newly_committed
        })
        
        next_id += 1
    
    # Extract motif records from commit clusters
    motif_records = []
    
    if commit_times:
        # Group by commit time
        by_time: Dict[int, List[int]] = defaultdict(list)
        for d, t in commit_times.items():
            by_time[t].append(d)
        
        # Each time-cluster is a potential motif
        for t, members in by_time.items():
            size = len(members)
            spread = 0.0  # All committed at same step
            
            # Compute persistence (fraction of remaining steps)
            total_post_steps = max_steps - t
            present_steps = sum(1 for rec in step_records if rec['step'] >= t)
            persistence = present_steps / total_post_steps if total_post_steps > 0 else 1.0
            
            # Ledger efficiency
            ledger_at_commit = next(
                (rec['ledger'] for rec in step_records if rec['step'] == t), 0
            )
            ledger_at_end = step_records[-1]['ledger'] if step_records else 0
            steps_after = len([rec for rec in step_records if rec['step'] >= t])
            
            ledger_eff = (ledger_at_end - ledger_at_commit) / steps_after if steps_after > 0 else 0
            
            # Interface signature
            signature = {interface.name: interface.cost(size)}
            
            # Check validity
            is_valid, violations = is_valid_motif(
                {m: t for m in members},
                persistence,
                ledger_eff
            )
            
            motif_records.append(MotifRecord(
                size=size,
                commit_time=t,
                commit_spread=spread,
                persistence=persistence,
                ledger_efficiency=ledger_eff,
                swap_survival=1.0,  # No SWAP in this simplified run
                interface_signature=signature,
                is_valid=is_valid,
                violations=violations
            ))
    
    run_info = {
        'final_n': len(distinctions),
        'total_committed': len(committed),
        'total_ledger': ledger,
        'steps': len(step_records)
    }
    
    return motif_records, run_info


# =============================================================================
# CATALOG GENERATION
# =============================================================================

def generate_catalog(
    interfaces: List[Interface],
    n_trials: int = 50,
    max_steps: int = 100,
    commit_threshold: float = SIGMA_THRESHOLD,
    verbose: bool = True
) -> MotifCatalog:
    """
    Generate a canonical motif catalog by surveying parameter space.
    """
    all_records: List[MotifRecord] = []
    
    if verbose:
        print(f"Generating catalog: {n_trials} trials per interface, "
              f"{len(interfaces)} interfaces")
        print(f"Commit threshold Ïƒ > {commit_threshold}")
    
    for itf in interfaces:
        if verbose:
            print(f"\n  Interface: {itf.name} (N_max={itf.max_n()})")
        
        for trial in range(n_trials):
            records, info = run_trial(itf, max_steps, commit_threshold)
            
            # Update signatures to include all interfaces
            for rec in records:
                for other_itf in interfaces:
                    if other_itf.name not in rec.interface_signature:
                        rec.interface_signature[other_itf.name] = other_itf.cost(rec.size)
            
            all_records.extend(records)
        
        if verbose:
            print(f"    Collected {len([r for r in all_records if r.interface_signature.get(itf.name)])} records")
    
    # Aggregate by size
    entries: Dict[int, CatalogEntry] = {}
    records_by_size: Dict[int, List[MotifRecord]] = defaultdict(list)
    
    for rec in all_records:
        records_by_size[rec.size].append(rec)
    
    for size, recs in records_by_size.items():
        entry = CatalogEntry(size=size)
        entry.update_from_records(recs)
        entries[size] = entry
    
    parameters = {
        "interfaces": [
            {"name": itf.name, "capacity": itf.capacity, "epsilon": itf.epsilon, 
             "eta": itf.eta, "N_max": itf.max_n()}
            for itf in interfaces
        ],
        "n_trials": n_trials,
        "max_steps": max_steps,
        "commit_threshold": commit_threshold
    }
    
    return MotifCatalog(
        parameters=parameters,
        entries=entries,
        raw_records=all_records,
        total_trials=n_trials * len(interfaces)
    )


def parameter_sweep(
    base_interface: Interface,
    param_name: str,
    values: List[float],
    n_trials: int = 20,
    verbose: bool = True
) -> Dict[float, MotifCatalog]:
    """
    Sweep a single parameter and generate catalogs.
    """
    results = {}
    
    if verbose:
        print(f"\nParameter sweep: {param_name}")
        print("=" * 50)
    
    for val in values:
        # Create interface with modified parameter
        kwargs = {
            "name": f"{param_name}={val}",
            "capacity": base_interface.capacity,
            "epsilon": base_interface.epsilon,
            "eta": base_interface.eta,
            "gamma": base_interface.gamma,
            "s0": base_interface.s0,
            "lam": base_interface.lam
        }
        kwargs[param_name] = val
        
        itf = Interface(**kwargs)
        
        if verbose:
            print(f"\n  {param_name}={val}, N_max={itf.max_n()}")
        
        catalog = generate_catalog([itf], n_trials=n_trials, verbose=False)
        results[val] = catalog
        
        if verbose:
            summary = catalog.summary()
            print(f"    Motifs: {summary['total_motifs_observed']}, "
                  f"Valid: {summary['valid_motifs']}")
    
    return results


# =============================================================================
# MULTI-INTERFACE CHARGE SURVEY
# =============================================================================

def charge_vector_survey(
    interfaces: List[Interface],
    n_trials: int = 30,
    verbose: bool = True
) -> Dict[int, Dict[str, float]]:
    """
    Compute charge vectors Q(M) for motifs under multiple interfaces.
    
    Returns: {size: {interface_name: mean_charge}}
    """
    if verbose:
        print("\n" + "=" * 60)
        print("CHARGE VECTOR SURVEY")
        print("=" * 60)
    
    # Run each interface separately
    charge_by_size: Dict[int, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    
    for itf in interfaces:
        if verbose:
            print(f"\nRunning interface: {itf.name}")
        
        for trial in range(n_trials):
            records, _ = run_trial(itf, max_steps=100)
            
            for rec in records:
                # Charge at this interface = enforcement load
                charge = itf.cost(rec.size)
                charge_by_size[rec.size][itf.name].append(charge)
    
    # Compute means
    result: Dict[int, Dict[str, float]] = {}
    
    for size in sorted(charge_by_size.keys()):
        result[size] = {}
        for itf_name, charges in charge_by_size[size].items():
            result[size][itf_name] = sum(charges) / len(charges) if charges else 0
    
    if verbose:
        print("\nCharge Vectors Q(M) by Size:")
        header = f"{'Size':>6}" + "".join(f"{itf.name[:10]:>12}" for itf in interfaces)
        print(header)
        print("-" * len(header))
        
        for size in sorted(result.keys()):
            row = f"{size:>6}"
            for itf in interfaces:
                row += f"{result[size].get(itf.name, 0):>12.2f}"
            print(row)
    
    return result


# =============================================================================
# MAIN
# =============================================================================

def main(full: bool = False):
    print("â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
    print("â•‘              CANONICAL MOTIF CATALOG GENERATOR               â•‘")
    print("â•‘                                                              â•‘")
    print("â•‘  The 'Periodic Table' of Admissible Motifs                   â•‘")
    print("â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
    
    # Define standard interfaces (SM-like)
    interfaces = [
        Interface("alpha", capacity=12.0, epsilon=1.0, eta=0.4, gamma=0.8, lam=-1.5),
        Interface("beta", capacity=15.0, epsilon=1.2, eta=0.5, gamma=0.7, lam=-1.3),
        Interface("gamma", capacity=10.0, epsilon=0.8, eta=0.6, gamma=1.0, lam=-1.8),
    ]
    
    n_trials = 100 if full else 30
    
    # Generate main catalog
    print("\n" + "=" * 60)
    print("MAIN CATALOG")
    print("=" * 60)
    
    catalog = generate_catalog(interfaces, n_trials=n_trials, commit_threshold=0.3)
    catalog.print_table()
    
    # Multi-interface charge survey
    charge_vectors = charge_vector_survey(interfaces, n_trials=n_trials)
    
    # Parameter sweeps (if full)
    if full:
        print("\n" + "=" * 60)
        print("PARAMETER SWEEPS")
        print("=" * 60)
        
        base = Interface("base", capacity=15.0, epsilon=1.0, eta=0.5, gamma=0.8)
        
        # Eta sweep
        eta_results = parameter_sweep(base, "eta", [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        
        print("\nÎ· Sweep Summary:")
        print(f"{'Î·':>6} {'Motifs':>8} {'Modal Size':>12}")
        for eta, cat in sorted(eta_results.items()):
            summary = cat.summary()
            print(f"{eta:>6.1f} {summary['total_motifs_observed']:>8} "
                  f"{summary['most_common_size'] or 'N/A':>12}")
    
    # Save catalog
    print("\n" + "=" * 60)
    print("SAVING CATALOG")
    print("=" * 60)
    
    catalog_dict = catalog.to_dict()
    with open('motif_catalog.json', 'w') as f:
        json.dump(catalog_dict, f, indent=2, default=str)
    
    print("Saved to motif_catalog.json")
    
    # Final summary
    print("\n" + "=" * 60)
    print("CATALOG SUMMARY")
    print("=" * 60)
    
    summary = catalog.summary()
    print(f"""
Total motifs observed: {summary['total_motifs_observed']}
Valid motifs (M1-M3): {summary['valid_motifs']} ({summary['validity_rate']:.0%})
Most common size: {summary['most_common_size']}

Size distribution: {summary['size_distribution']}

This catalog shows which motif sizes emerge robustly under
admissible microdynamics with SM-like interface structure.

Interpretation:
- Size = particle type
- Persistence = stability
- Ledger efficiency = mass
- Charge vector = quantum numbers
""")


if __name__ == "__main__":
    full_mode = "--full" in sys.argv
    main(full=full_mode)

# Admissibility Physics: Interface Calculus Framework

A complete mathematical framework deriving quantum mechanics, gauge theory, general relativity, and the Standard Model from first principles.

## Overview

This repository contains the **Interface Calculus** framework—a unified mathematical approach built on five axioms governing how physical distinctions can be maintained under finite resources. From these axioms alone, we derive:

1. **Quantum mechanics** as the unique non-classical representation (Hilbert space from complementation)
2. **Gauge theory** as local enforcement structure (fiber bundles from locality)
3. **N_gen = 3 fermion generations** from capacity saturation at shared interfaces
4. **General Relativity** from non-factorization of internal/external enforcement
5. **d = 4 spacetime dimensions** from uniqueness of geometric response
6. **Λ ~ H₀²** from irreducible residual at the cosmological horizon

## Repository Structure

```
admissibility-physics/
├── docs/                           # Mathematical documentation
│   ├── ADMISSIBILITY_PHYSICS_v7_DEFINITIVE.md   # Main paper (peer review document)
│   ├── capacity_saturation_theorem.md
│   └── archive/                    # Previous versions
│
├── src/                            # Source code
│   ├── theorems/                   # Individual theorem implementations
│   │   ├── theorem1_rigorous_derivation.py
│   │   ├── theorem2_final.py
│   │   ├── theorem3_corrected.py
│   │   ├── theorem4_corrected.py
│   │   ├── theorem5_corrected.py
│   │   ├── theorem6_capacity_partition.py
│   │   ├── theorem6B_capacity_running_fixed.py
│   │   ├── theorem7B_gravity_from_nonfactorization.py
│   │   └── theorems_7_8_9_10_gravity_complete.py
│   │
│   ├── core/                       # Core framework implementations
│   │   ├── admissibility_unified_V5.py    # Latest unified implementation
│   │   ├── motif_definition.py
│   │   ├── motif_analysis.py
│   │   ├── motif_catalog.py
│   │   └── motif_regime_v2.py
│   │
│   └── utils/                      # Utility modules
│       ├── routing_engine_v1.py
│       ├── accumulated_cost.py
│       ├── lambda_floor.py
│       └── unification_analysis.py
│
├── notebooks/                      # Jupyter/Colab notebooks
│   └── admissibility_colab_single_cell.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/admissibility-physics.git
cd admissibility-physics
pip install -r requirements.txt
```

## Quick Start

```python
# Run the main unified framework
python src/core/admissibility_unified_V5.py

# Run individual theorem verifications
python src/theorems/theorem1_rigorous_derivation.py
```

## Key Concepts

### Primitive Notions

- **Distinction Space (D)**: Set of binary "this versus that" distinctions—the most elementary unit of physical information
- **Interface (I)**: Locus where distinctions must be enforced
- **Capacity (C_i)**: Maximum enforcement load an interface can sustain
- **Enforcement Functional (E_i)**: Maps sets of distinctions to non-negative costs

### The Five Axioms

1. **Finiteness (A1)**: Every interface has finite capacity
2. **Non-Closure (A2)**: Admissible sets are not closed under union
3. **Complementation (A3)**: Every distinction has an admissible complement
4. **Locality (A4)**: Enforcement structure respects causal locality
5. **Minimality (A5)**: Systems evolve to minimize total enforcement cost

## Documentation

The complete mathematical framework with rigorous proofs is available in:
- [`docs/ADMISSIBILITY_PHYSICS_v7_DEFINITIVE.md`](docs/ADMISSIBILITY_PHYSICS_v7_DEFINITIVE.md)

## Theorem Overview

| Theorem | Result | File |
|---------|--------|------|
| 1 | Non-closure → No global joint refinement | `theorem1_rigorous_derivation.py` |
| 2 | Complementation → Hilbert space structure | `theorem2_final.py` |
| 3 | Locality → Fiber bundle structure | `theorem3_corrected.py` |
| 4 | Interface coupling → Gauge groups | `theorem4_corrected.py` |
| 5 | Capacity saturation → N_gen = 3 | `theorem5_corrected.py` |
| 6 | Capacity partition theorem | `theorem6_capacity_partition.py` |
| 7-10 | Gravity from non-factorization | `theorems_7_8_9_10_gravity_complete.py` |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this work in your research, please cite:

Ethan Brooke

## Contact

[Brooke.Ethan@gmail.com ]

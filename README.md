# CT-NIfTI Boundary Pipeline

A Python-based portfolio implementation for extracting simulation-ready
boundary-condition surfaces from CT-derived NIfTI volumes.

## Overview

Numerical analysis of CT-derived engineering specimens requires more than the
voxel geometry itself. Loads and supports must be associated with well-defined
physical surfaces while preserving consistency between voxel coordinates,
physical coordinates, exported geometry, and the downstream simulation domain.

This project reconstructs a focused workflow for:

- loading CT-derived NIfTI volumes
- preparing image volumes for numerical-analysis workflows
- handling voxel-to-physical coordinate transformations
- selecting local regions of interest
- identifying exposed material surfaces
- exporting selected boundary surfaces as STL geometry
- generating metadata for simulation handover
- validating geometric and coordinate consistency

## Project Context

This repository is an **independent portfolio reconstruction** inspired by my
contribution to a collaborative 12-ECTS Digital Engineering research project at
Bauhaus-Universität Weimar:

**Development of an Image-to-Analysis Pipeline for the Modeling of Fracture Processes**

The original research project investigated an end-to-end workflow connecting
CT-derived specimen geometry with Finite Cell Method (FCM) and phase-field
fracture simulations.

The original project involved multiple contributors and an existing research
software environment. This repository does **not** reproduce or claim ownership
of the complete university research codebase.

## My Contribution to the Original Project

My work focused primarily on the interface between CT-derived image data and
simulation-ready inputs.

This included:

- working with CT/NIfTI preprocessing workflows such as cropping and reorientation
- understanding and maintaining consistency between voxel indices and physical coordinates
- developing NIfTI-based boundary-condition surface extraction
- converting exposed voxel faces into simulation-ready STL surfaces
- supporting metadata and JSON-based simulation handover
- integrating and validating the workflow within an existing research software environment
- working collaboratively with Git/GitLab branches and an existing codebase

## Workflow

```text
CT-derived volume
        │
        ▼
NIfTI preprocessing
        │
        ▼
Coordinate handling
        │
        ▼
Region-of-interest selection
        │
        ▼
Boundary surface extraction
        │
        ▼
STL + metadata export
        │
        ▼
Simulation-ready inputs
```

## Portfolio Implementation

The public implementation is being rebuilt independently using synthetic or
publicly shareable data.

The goal is to demonstrate the underlying engineering and software concepts
without distributing private research datasets or reproducing the complete
original university codebase.

Planned components include:

- synthetic NIfTI specimen generation
- preprocessing utilities
- voxel/physical coordinate transformations
- directional boundary extraction
- STL export
- metadata export
- visualization
- automated validation tests

## Repository Structure

```text
ct-nifti-boundary-pipeline/
├── docs/
├── examples/
├── notebooks/
├── results/
├── src/
│   └── ct_pipeline/
├── tests/
├── .gitignore
├── ATTRIBUTION.md
├── README.md
└── requirements.txt
```

## Status

🚧 **Under active development**

The original academic project is complete. This repository is a clean,
independent portfolio reconstruction intended to demonstrate and strengthen the
technical skills developed during that work.

## License and Attribution

See `ATTRIBUTION.md` for information about the original academic project and
the scope of this reconstruction.

A software license for the independently written portfolio implementation will
be added once the first reusable code modules are finalized.

# CT NIfTI Boundary Pipeline

A reproducible Python pipeline for extracting physically meaningful
boundary surfaces from CT-derived NIfTI volumes and exporting them as
STL geometry.

## Overview

This project demonstrates an end-to-end workflow:

**CT volume → preprocessing → segmentation → boundary selection →
physical surface reconstruction → STL export → validation**

## Features

-   NIfTI volume loading and inspection
-   Affine-aware voxel-to-physical coordinate transformations
-   Canonical RAS reorientation
-   CT intensity segmentation using Otsu thresholding
-   Directional boundary patch extraction
-   Voxel-face based surface reconstruction
-   STL export
-   JSON metadata generation
-   Automated geometry validation

## Workflow

    CT NIfTI Volume
            |
            v
    Volume Inspection
            |
            v
    Preprocessing
            |
            v
    Segmentation
            |
            v
    Boundary Selection
            |
            v
    Surface Reconstruction
            |
            v
    STL Export
            |
            v
    Validation

## Repository Structure

    examples/
    src/ct_pipeline/
    tests/
    docs/
    results/
    requirements.txt
    pyproject.toml

## Installation

``` bash
git clone https://github.com/ijazahmadraoof/ct-nifti-boundary-pipeline.git
cd ct-nifti-boundary-pipeline
python -m venv .venv
```

Activate environment:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

## Demo

Run:

``` bash
python examples/01_inspect_nifti.py
python examples/03_crop_and_reorient.py
python examples/05_segment_real_cube.py
python examples/06_select_real_boundary_patch.py
```

Outputs include:

-   boundary visualization
-   STL surface file
-   extraction metadata JSON

## Testing

Run:

``` bash
pytest -v
```

The test suite covers coordinate transformations, preprocessing,
segmentation, surface generation, STL export, and validation.

## Technologies

-   Python
-   NumPy
-   SciPy
-   NiBabel
-   Matplotlib
-   PyTest

## Skills Demonstrated

-   Scientific Python programming
-   CT image processing
-   Computational geometry
-   Coordinate systems
-   Simulation preprocessing
-   Reproducible engineering workflows

## Author

Ijaz Ahmad Raoof

Master's Student in Digital Engineering\
Bauhaus University Weimar

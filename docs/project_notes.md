# Project Notes

This file is a lightweight development record for the public portfolio reconstruction.

It complements `contribution_summary.md`, which documents my role in the original collaborative university project and distinguishes it from the later independent portfolio implementation.

## Goals

The reconstruction was designed to:

- rebuild the CT/NIfTI-to-boundary-surface concepts independently
- avoid publishing private research datasets
- use a synthetic reference case with known spatial metadata
- keep the implementation modular and testable
- preserve the distinction between the original collaborative university project and this public portfolio implementation
- produce code whose engineering decisions can be reviewed and explained clearly

## Development Record

### 1. Repository foundation — complete

- created a `src/`-layout Python repository
- added `.gitignore` and `.gitattributes`
- added project context and attribution
- configured `pyproject.toml`
- created an editable development installation
- separated local/private data from tracked source code

### 2. NIfTI inspection and synthetic reference volume — complete

Implemented:

- NIfTI loading
- shape and data-type inspection
- voxel spacing inspection
- qform/sform inspection
- affine-source detection
- orientation reporting
- intensity statistics
- synthetic T-shaped specimen generation
- explicit millimetre units
- known voxel spacing and physical origin
- explicit qform and sform

Main files:

- `src/ct_pipeline/io.py`
- `src/ct_pipeline/synthetic.py`
- `examples/01_inspect_nifti.py`
- `examples/02_create_synthetic_volume.py`

### 3. Coordinate transformations — complete

Implemented:

- voxel-centre to physical-coordinate conversion
- physical-coordinate to continuous voxel-coordinate conversion
- outer voxel-cell corner calculation
- physical volume bounds

Important design point:

NIfTI voxel indices describe voxel centres, while exported surface geometry lies on voxel-cell faces at offsets of `±0.5` voxel.

Main file:

- `src/ct_pipeline/coordinates.py`

### 4. Geometry-preserving preprocessing — complete

Implemented:

- 3D cropping
- affine update after cropping
- spatial-unit preservation
- canonical RAS reorientation
- checks that reorientation preserves physical bounds

Main files:

- `src/ct_pipeline/preprocessing.py`
- `examples/03_crop_and_reorient.py`

### 5. Material segmentation — complete

Implemented:

- lower-threshold material masking
- Otsu threshold estimation
- intensity histogram diagnostic
- segmentation-slice comparison

The Otsu result used for the local CT cube is treated as a computational candidate threshold, not as a calibrated material property.

Main files:

- `src/ct_pipeline/segmentation.py`
- `examples/05_segment_real_cube.py`

### 6. Directional boundary detection — complete

Implemented exposed-face detection for:

- `+X`
- `-X`
- `+Y`
- `-Y`
- `+Z`
- `-Z`

Core rule:

```text
material voxel + empty neighbour in requested direction
                         ↓
                 exposed boundary face
```

Main file:

- `src/ct_pipeline/boundary.py`

### 7. Boundary-patch selection — complete

Implemented:

- fractional X/Y/Z ROI selection
- directional outer-surface band filtering
- largest connected component filtering
- configurable 3D connectivity

This layer prevents the workflow from simply exporting every internal material/void interface.

Main file:

- `src/ct_pipeline/selection.py`

### 8. Surface geometry and STL export — complete

Implemented:

- four voxel-face corner coordinates per selected face
- affine transformation into physical space
- square-face triangulation
- outward-normal correction under reflected affines
- ASCII STL writing

Main files:

- `src/ct_pipeline/surface.py`
- `src/ct_pipeline/stl_export.py`
- `examples/04_export_synthetic_boundary.py`

### 9. Metadata and automated validation — complete

Implemented JSON metadata containing:

- boundary name and direction
- segmentation method / threshold
- ROI ranges
- surface-band setting
- connected-component setting
- selected voxel count
- triangle count
- physical bounds
- affine source
- spatial units
- orientation
- STL filename

Implemented geometry checks for:

- non-empty surface
- triangle-array shape
- two triangles per selected voxel face
- finite coordinates
- non-degenerate triangles
- directionally consistent physical normals

Main files:

- `src/ct_pipeline/metadata.py`
- `src/ct_pipeline/validation.py`

### 10. Local CT-derived validation example — complete

A small CT-derived cube was used locally to test the workflow on realistic heterogeneous image data.

Observed characteristics:

- `256 × 256 × 256` volume
- dominant high-intensity material phase
- visible low-intensity pores/voids
- missing qform/sform
- unspecified spatial units
- NiBabel fallback affine interpretation

The local-data workflow:

```text
load local cube
    ↓
inspect spatial metadata
    ↓
canonical working orientation
    ↓
Otsu diagnostic threshold
    ↓
material mask
    ↓
direction + ROI + surface band
    ↓
largest connected patch
    ↓
physical-space triangles
    ↓
STL + JSON
    ↓
validation
```

The research dataset is intentionally not tracked in Git.

Main files:

- `examples/05_segment_real_cube.py`
- `examples/06_select_real_boundary_patch.py`

### 11. Public end-to-end synthetic demonstration — complete

The final public demo uses only generated data and runs the complete portfolio pipeline without the original research dataset.

Run:

```bash
python examples/07_full_synthetic_pipeline.py
```

The demo generates:

- synthetic NIfTI
- segmentation diagnostic
- boundary overlay
- STL boundary surface
- JSON metadata
- validation report in the console

## Testing

The repository contains automated tests covering the core numerical and geometry operations.

The goal of the tests is not only software correctness but also engineering traceability: coordinate conversion, face direction, triangle count, and surface normals are checked explicitly rather than validated only by appearance.

## Current Status

The planned portfolio reconstruction is complete.

Future changes should be limited to maintenance, documentation improvements, or clearly scoped extensions. Additional unrelated features should not be added simply to make the repository larger.

## Optional Future Extensions

Possible extensions, if they become useful for a specific engineering or research requirement:

- interactive 3D visualization
- an optional lightweight GUI
- comparison with marching-cubes surfaces
- direct solver integration
- support for additional image formats or datasets

These are **not required** for the current portfolio project to be considered complete.

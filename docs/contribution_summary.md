# Contribution and Scope

## Purpose

This document clarifies:

1. the scope of my contribution to the original collaborative university project, and
2. the additional work implemented later in this independent public portfolio reconstruction.

The distinction is important because the original project involved multiple contributors and an existing research software environment.

## Original Collaborative Project

**Project:** Development of an Image-to-Analysis Pipeline for the Modeling of Fracture Processes  
**Program:** M.Sc. Digital Engineering  
**Institution:** Bauhaus-Universität Weimar  
**Project type:** Collaborative 12-ECTS research project

The broader collaborative project included work on CT preprocessing and material characterization, simulation-boundary preparation, Finite Cell Method (FCM) boundary-condition handling, JSON-driven simulation configuration, and phase-field fracture simulation.

## My Contribution to the Original Project

My work focused primarily on the interface between **CT-derived image data** and **simulation-ready boundary inputs**.

### CT/NIfTI preprocessing workflow

I worked with the preprocessing workflow required to prepare CT-derived NIfTI data for simulation handover, including:

- cropping concepts and region isolation
- orientation and reorientation
- voxel spacing and physical-coordinate awareness
- alignment between the prepared NIfTI, exported STL surfaces, and the solver domain

I did not develop the complete preprocessing GUI from scratch. My role required understanding and working with the existing preprocessing environment so that downstream boundary extraction remained coordinate-consistent.

### Directional boundary-surface extraction

A central part of my contribution was the boundary-condition surface workflow:

1. select a local region of interest
2. create or use a material/void threshold mask
3. choose a direction (`+X`, `-X`, `+Y`, `-Y`, `+Z`, or `-Z`)
4. identify material voxels with an empty neighbour in that direction
5. convert each exposed square voxel face into two triangles
6. transform voxel-face corners into physical coordinates
7. export the selected surface as STL geometry

This allowed boundary-condition surfaces to be derived directly from the CT/NIfTI geometry rather than being created manually in a potentially inconsistent coordinate system.

### ROI and cleanup controls

The original workflow included controls for:

- directional face selection
- local percentage-based X/Y/Z ranges
- threshold settings
- surface-band filtering
- largest-component cleanup

These controls supported the extraction of local load/support markers rather than every material/void interface in the volume.

### STL and metadata handover

I contributed to the handover from image processing to simulation by working on:

- boundary STL export
- physical-coordinate consistency
- metadata/JSON-based handover
- validation of exported boundary surfaces

The intended outputs from this stage were:

- preprocessed NIfTI geometry
- boundary STL markers for loads/supports
- export metadata / JSON for the downstream simulation workflow

### Validation

The validation approach included checking:

- visual alignment of the STL with the selected CT surface
- coordinate bounds
- intended direction
- downstream solver intersection

The key engineering requirement was that the exported geometry remain consistent with the NIfTI coordinate system and usable by the downstream simulation workflow.

### Software collaboration

I worked within an existing collaborative software environment and contributed through Git/GitLab branches rather than developing the complete research codebase independently.

## Scope Boundaries

The original project contained substantial work outside my individual contribution.

This repository does not claim that I developed:

- the complete CT-analysis GUI
- the complete raw-CT correction workflow
- the complete pore/material characterization workflow
- the FCM solver
- the phase-field fracture formulation
- the full C++ simulation system
- the complete end-to-end university research codebase

Those components belonged to the broader collaborative project.

## Independent Portfolio Reconstruction

This public repository was rebuilt independently to demonstrate and strengthen the concepts related to my original contribution.

The portfolio implementation adds several components that are **new portfolio engineering work** rather than one-to-one reproductions of what I implemented during the university project.

### Portfolio-specific additions

The reconstruction includes:

- a synthetic T-shaped NIfTI specimen with known spacing, origin, qform, sform, and millimetre units
- reusable NIfTI inspection utilities
- explicit voxel-to-physical and physical-to-voxel coordinate functions
- geometry-preserving cropping
- canonical RAS reorientation utilities
- Otsu threshold estimation for the local CT diagnostic
- directional exposed-face detection
- fractional ROI selection
- surface-band filtering
- connected-component filtering
- standalone physical-space triangulation
- standalone ASCII STL export
- JSON metadata generation
- automated boundary-geometry validation
- automated tests
- public synthetic examples
- local real-data validation examples
- portfolio documentation

## How the Portfolio Code Maps to the Contribution

| Engineering concern | Portfolio modules |
|---|---|
| NIfTI loading and spatial inspection | `src/ct_pipeline/io.py` |
| Voxel / physical coordinates | `src/ct_pipeline/coordinates.py` |
| Cropping and reorientation | `src/ct_pipeline/preprocessing.py` |
| Material mask creation | `src/ct_pipeline/segmentation.py` |
| Directional exposed-face detection | `src/ct_pipeline/boundary.py` |
| ROI / surface-band / component selection | `src/ct_pipeline/selection.py` |
| Physical-space triangle generation | `src/ct_pipeline/surface.py` |
| STL export | `src/ct_pipeline/stl_export.py` |
| JSON handover metadata | `src/ct_pipeline/metadata.py` |
| Geometry checks | `src/ct_pipeline/validation.py` |
| Diagnostic figures | `src/ct_pipeline/visualization.py` |
| Public reproducible demonstration | `examples/07_full_synthetic_pipeline.py` |

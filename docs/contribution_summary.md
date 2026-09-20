# Individual Contribution Summary

## Purpose of This Document

This document separates two things clearly:

1. my contribution to the original collaborative university project, and
2. the additional work completed later for this independent public portfolio reconstruction.

This distinction is important because the original project involved multiple contributors and an existing research software environment.

## Original University Project

**Project:** Development of an Image-to-Analysis Pipeline for the Modeling of Fracture Processes  
**Program:** M.Sc. Digital Engineering  
**Institution:** Bauhaus-Universität Weimar  
**Project type:** Collaborative 12-ECTS research project

The wider project connected CT-derived specimen data to numerical fracture analysis. The complete team workflow included work on CT preprocessing and material characterization, simulation-boundary preparation, Finite Cell Method (FCM) boundary-condition handling, JSON-driven simulation configuration, and phase-field fracture simulation.

## My Contribution to the Original Project

My work focused primarily on the interface between **CT-derived image data** and **simulation-ready boundary inputs**.

### CT/NIfTI preprocessing workflow

I worked with the preprocessing workflow required to prepare CT-derived NIfTI data for simulation handover, including:

- cropping concepts and region isolation
- orientation and reorientation
- voxel spacing and physical-coordinate awareness
- alignment between the prepared NIfTI, exported STL surfaces, and the solver domain

I did **not** develop the complete preprocessing GUI from scratch. My role required understanding and working with the existing preprocessing environment so that downstream boundary extraction remained coordinate-consistent.

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

The key engineering idea was that a surface that merely looks correct is not sufficient; the geometry also needs to be consistent with the NIfTI coordinate system and usable by the simulation.

### Software collaboration

I worked within an existing collaborative software environment and contributed through Git/GitLab branches rather than developing the complete research codebase independently.

## What I Did Not Claim

The original project contained significant work outside my individual contribution.

I do **not** claim to have developed:

- the complete CT-analysis GUI
- the complete raw-CT correction workflow
- the complete pore/material characterization workflow
- the FCM solver
- the phase-field fracture formulation
- the full C++ simulation system
- the complete end-to-end university research codebase

Those components formed part of the broader collaborative project.

## Independent Portfolio Reconstruction

This public repository was rebuilt independently to demonstrate and strengthen the concepts related to my original contribution.

The portfolio implementation adds several components that should be understood as **new portfolio engineering work**, not necessarily one-to-one reproductions of what I implemented during the university project.

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

## One-Sentence Interview Summary

> In the original collaborative project, I worked mainly on the CT/NIfTI-to-simulation handover: understanding preprocessing and coordinate consistency, extracting directional boundary-condition surfaces from voxel data, exporting them as STL markers, and supporting metadata and validation for downstream simulation; this GitHub repository independently rebuilds those ideas in a smaller, tested Python package.

## Short Interview Version

If asked, "What did you personally do?", a concise answer is:

> My contribution was mainly between the CT data and the solver. I worked with the NIfTI preprocessing workflow, had to keep voxel and physical coordinates consistent, and developed the logic for selecting a local directional surface from the CT volume and exporting it as an STL boundary marker. I also worked on the metadata/JSON handover and validation inside the existing research software workflow. I did not develop the complete fracture solver or the entire GUI. The GitHub project is my independent reconstruction of that part, with additional tests and reproducible examples.

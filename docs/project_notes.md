# Project Notes

Use this file as a lightweight development log for the portfolio reconstruction.

## Goals

- Rebuild the core workflow independently.
- Use synthetic or publicly shareable data.
- Keep the implementation small, testable, and easy to explain in an interview.
- Preserve a clear distinction between the original university research project
  and this public portfolio implementation.

## Development Log

### Initial setup

- Created professional repository structure.
- Added project context and attribution.
- Defined the planned CT/NIfTI → boundary extraction → STL/metadata workflow.

## Next Steps

1. Create a synthetic 3D specimen volume.
2. Save it as a NIfTI file with a known affine transform.
3. Implement NIfTI loading and basic inspection.
4. Add preprocessing utilities.
5. Implement coordinate transformations.
6. Implement directional boundary-surface extraction.
7. Export selected surfaces to STL.
8. Add metadata export.
9. Add visualization and validation tests.

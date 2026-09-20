"""Run the complete public synthetic CT-to-boundary demonstration."""

from pathlib import Path

import nibabel as nib
import numpy as np

from ct_pipeline.io import (
    get_affine_source,
    load_nifti,
)
from ct_pipeline.metadata import (
    build_boundary_metadata,
    write_metadata_json,
)
from ct_pipeline.segmentation import (
    threshold_material,
)
from ct_pipeline.selection import (
    select_boundary_patch,
)
from ct_pipeline.stl_export import (
    write_ascii_stl,
)
from ct_pipeline.surface import (
    voxel_faces_to_triangles,
)
from ct_pipeline.synthetic import (
    save_synthetic_nifti,
)
from ct_pipeline.validation import (
    require_valid_boundary,
    validate_boundary_surface,
)
from ct_pipeline.visualization import (
    save_boundary_overlay,
    save_segmentation_slices,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Generate, process, validate, and export a synthetic boundary surface."""

    output_dir = (
        PROJECT_ROOT
        / "results"
        / "full_synthetic_demo"
    )

    nifti_path = (
        output_dir
        / "synthetic_t_shape.nii.gz"
    )

    # ------------------------------------------------------------------
    # 1. Generate a reproducible NIfTI specimen
    # ------------------------------------------------------------------

    save_synthetic_nifti(
        nifti_path,
        voxel_spacing=(0.25, 0.25, 0.50),
        origin=(10.0, 20.0, 30.0),
    )

    image = load_nifti(
        nifti_path
    )

    data = np.asarray(
        image.dataobj,
        dtype=float,
    )

    # ------------------------------------------------------------------
    # 2. Segment material
    # ------------------------------------------------------------------
    #
    # The synthetic volume is binary:
    #   0 = background
    #   1 = material
    #
    # A fixed threshold is therefore transparent and reproducible.
    # ------------------------------------------------------------------

    threshold = 0.5

    material_mask = threshold_material(
        data,
        threshold=threshold,
    )

    # ------------------------------------------------------------------
    # 3. Select a directional boundary patch
    # ------------------------------------------------------------------

    direction = "+Z"

    x_range = (0.0, 1.0)
    y_range = (0.0, 1.0)
    z_range = (0.5, 1.0)

    surface_band_voxels = 1
    largest_component = True
    connectivity = 1

    selected = select_boundary_patch(
        material_mask,
        direction=direction,
        x_range=x_range,
        y_range=y_range,
        z_range=z_range,
        surface_band_voxels=surface_band_voxels,
        largest_component=largest_component,
        connectivity=connectivity,
    )

    selected_indices = np.argwhere(
        selected
    )

    # ------------------------------------------------------------------
    # 4. Convert exposed voxel faces to physical-space triangles
    # ------------------------------------------------------------------

    triangles = voxel_faces_to_triangles(
        selected_indices,
        direction,
        image.affine,
    )

    # ------------------------------------------------------------------
    # 5. Validate before export
    # ------------------------------------------------------------------

    validation = validate_boundary_surface(
        triangles,
        selected_voxel_count=len(
            selected_indices
        ),
        direction=direction,
        affine=image.affine,
    )

    require_valid_boundary(
        validation
    )

    # ------------------------------------------------------------------
    # 6. Export STL geometry
    # ------------------------------------------------------------------

    stl_path = (
        output_dir
        / "synthetic_plus_z_boundary.stl"
    )

    write_ascii_stl(
        triangles,
        stl_path,
        solid_name="synthetic_plus_z_boundary",
    )

    # ------------------------------------------------------------------
    # 7. Export metadata
    # ------------------------------------------------------------------

    affine_source = get_affine_source(
        image
    )

    spatial_units, _ = (
        image.header.get_xyzt_units()
    )

    orientation = nib.aff2axcodes(
        image.affine
    )

    metadata = build_boundary_metadata(
        boundary_name="synthetic_plus_z",
        direction=direction,
        threshold_method="fixed_binary_demo",
        threshold_value=threshold,
        x_range=x_range,
        y_range=y_range,
        z_range=z_range,
        surface_band_voxels=surface_band_voxels,
        largest_component=largest_component,
        connectivity=connectivity,
        selected_voxel_count=len(
            selected_indices
        ),
        triangles=triangles,
        affine_source=affine_source,
        spatial_units=(
            spatial_units
            or "unknown"
        ),
        orientation=orientation,
        stl_file=stl_path.name,
    )

    metadata_path = write_metadata_json(
        metadata,
        output_dir
        / "synthetic_plus_z_boundary.json",
    )

    # ------------------------------------------------------------------
    # 8. Create reproducible diagnostic figures
    # ------------------------------------------------------------------

    segmentation_path = save_segmentation_slices(
        image,
        material_mask,
        output_dir
        / "01_segmentation.png",
    )

    overlay_path = save_boundary_overlay(
        image,
        selected,
        direction,
        output_dir
        / "02_boundary_overlay.png",
        title=(
            "Synthetic T-shape — "
            "selected +Z boundary"
        ),
    )

    # ------------------------------------------------------------------
    # 9. Console summary
    # ------------------------------------------------------------------

    print(
        "\nFull synthetic CT-to-boundary demonstration"
    )
    print("=" * 64)

    print(
        f"NIfTI shape:            "
        f"{image.shape}"
    )

    print(
        f"Affine source:          "
        f"{affine_source}"
    )

    print(
        f"Spatial units:          "
        f"{spatial_units or 'unknown'}"
    )

    print(
        f"Orientation:            "
        f"{''.join(orientation)}"
    )

    print(
        f"Threshold:              "
        f"{threshold}"
    )

    print(
        f"Boundary direction:     "
        f"{direction}"
    )

    print(
        f"Selected boundary voxels: "
        f"{len(selected_indices):,}"
    )

    print(
        f"Generated triangles:      "
        f"{len(triangles):,}"
    )

    if len(triangles) > 0:
        print(
            "\nPhysical surface bounds"
        )
        print("-" * 64)

        print(
            "Minimum: "
            f"{triangles.min(axis=(0, 1))}"
        )

        print(
            "Maximum: "
            f"{triangles.max(axis=(0, 1))}"
        )

    print("\nValidation")
    print("-" * 64)

    for name, value in validation.items():
        if isinstance(value, bool):
            print(
                f"{name:28} "
                f"{'PASS' if value else 'FAIL'}"
            )

    print("\nOutputs")
    print("-" * 64)

    print(
        f"NIfTI:        "
        f"{nifti_path}"
    )

    print(
        f"Segmentation: "
        f"{segmentation_path}"
    )

    print(
        f"Overlay:      "
        f"{overlay_path}"
    )

    print(
        f"STL:          "
        f"{stl_path}"
    )

    print(
        f"Metadata:     "
        f"{metadata_path}"
    )


if __name__ == "__main__":
    main()

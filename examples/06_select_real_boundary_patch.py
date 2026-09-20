"""Select and export a demonstration BC patch from local CT data."""

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
from ct_pipeline.preprocessing import (
    reorient_to_canonical,
)
from ct_pipeline.segmentation import (
    estimate_otsu_threshold,
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
from ct_pipeline.validation import (
    require_valid_boundary,
    validate_boundary_surface,
)
from ct_pipeline.visualization import (
    save_boundary_overlay,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Run the real CT boundary-patch demonstration."""

    # ------------------------------------------------------------------
    # Input and output paths
    # ------------------------------------------------------------------

    input_path = (
        PROJECT_ROOT
        / "local_data"
        / "cube_split_01.nii"
    )

    output_dir = (
        PROJECT_ROOT
        / "results"
        / "real_cube_boundary"
    )

    # ------------------------------------------------------------------
    # Load the original NIfTI volume
    # ------------------------------------------------------------------

    original_image = load_nifti(
        input_path
    )

    original_affine_source = (
        get_affine_source(
            original_image
        )
    )

    # ------------------------------------------------------------------
    # Reorient to a consistent canonical representation
    # ------------------------------------------------------------------
    #
    # The original cube has no defined qform/sform, so its affine comes
    # from NiBabel's fallback interpretation.
    #
    # Canonicalization gives us a consistent RAS voxel-axis convention
    # for directional controls, but it does not make the original spatial
    # metadata authoritative.
    # ------------------------------------------------------------------

    image = reorient_to_canonical(
        original_image
    )

    working_orientation = (
        nib.aff2axcodes(
            image.affine
        )
    )

    # ------------------------------------------------------------------
    # Load voxel intensities
    # ------------------------------------------------------------------

    data = np.asarray(
        image.dataobj,
        dtype=float,
    )

    # ------------------------------------------------------------------
    # Estimate segmentation threshold
    # ------------------------------------------------------------------

    threshold = estimate_otsu_threshold(
        data,
        bins=256,
    )

    material_mask = threshold_material(
        data,
        threshold=threshold,
    )

    # ------------------------------------------------------------------
    # Boundary-selection parameters
    # ------------------------------------------------------------------
    #
    # These parameters define a demonstration region only.
    # They are not claimed to represent a physically calibrated load or
    # support location from the original experiment.
    # ------------------------------------------------------------------

    direction = "+Z"

    x_range = (0.25, 0.75)
    y_range = (0.25, 0.75)
    z_range = (0.75, 1.00)

    surface_band_voxels = 1
    largest_component = True
    connectivity = 1

    # ------------------------------------------------------------------
    # Select the directional boundary patch
    # ------------------------------------------------------------------

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
    # Convert selected voxel faces into physical-space triangles
    # ------------------------------------------------------------------

    triangles = voxel_faces_to_triangles(
        selected_indices,
        direction,
        image.affine,
    )

    # ------------------------------------------------------------------
    # Validate geometry before export
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
    # Export STL
    # ------------------------------------------------------------------

    stl_path = (
        output_dir
        / "demo_plus_z_boundary.stl"
    )

    write_ascii_stl(
        triangles,
        stl_path,
        solid_name="real_cube_demo_plus_z",
    )

    # ------------------------------------------------------------------
    # Create metadata
    # ------------------------------------------------------------------

    spatial_units, _ = (
        image.header.get_xyzt_units()
    )

    metadata = build_boundary_metadata(
        boundary_name="demo_plus_z",
        direction=direction,
        threshold_method="otsu",
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
        affine_source=original_affine_source,
        spatial_units=(
            spatial_units
            or "unknown"
        ),
        orientation=working_orientation,
        stl_file=stl_path.name,
    )

    metadata_path = (
        write_metadata_json(
            metadata,
            output_dir
            / "demo_plus_z_boundary.json",
        )
    )

    # ------------------------------------------------------------------
    # Create visual validation overlay
    # ------------------------------------------------------------------

    overlay_path = save_boundary_overlay(
        image,
        selected,
        direction,
        output_dir
        / "01_boundary_overlay.png",
        title=(
            "Real CT cube — "
            "demonstration boundary patch"
        ),
    )

    # ------------------------------------------------------------------
    # Console summary
    # ------------------------------------------------------------------

    print(
        "\nReal CT boundary-patch demonstration"
    )
    print("=" * 60)

    print(
        f"Original affine source: "
        f"{original_affine_source}"
    )

    print(
        f"Working orientation:    "
        f"{''.join(working_orientation)}"
    )

    print(
        f"Otsu threshold:         "
        f"{threshold:.6f}"
    )

    print(
        f"Direction:              "
        f"{direction}"
    )

    # ------------------------------------------------------------------
    # ROI information
    # ------------------------------------------------------------------

    print("\nROI")
    print("-" * 60)

    print(
        f"X: {x_range[0]:.0%} -> "
        f"{x_range[1]:.0%}"
    )

    print(
        f"Y: {y_range[0]:.0%} -> "
        f"{y_range[1]:.0%}"
    )

    print(
        f"Z: {z_range[0]:.0%} -> "
        f"{z_range[1]:.0%}"
    )

    print(
        f"Surface band: "
        f"{surface_band_voxels} voxel"
    )

    print(
        f"Largest component: "
        f"{'yes' if largest_component else 'no'}"
    )

    print(
        f"Connectivity: "
        f"{connectivity}"
    )

    # ------------------------------------------------------------------
    # Selected geometry
    # ------------------------------------------------------------------

    print("\nSelected geometry")
    print("-" * 60)

    print(
        f"Selected boundary voxels: "
        f"{len(selected_indices):,}"
    )

    print(
        f"Generated triangles:      "
        f"{len(triangles):,}"
    )

    if len(triangles) > 0:
        bounds_minimum = (
            triangles.min(
                axis=(0, 1)
            )
        )

        bounds_maximum = (
            triangles.max(
                axis=(0, 1)
            )
        )

        print(
            "\nCoordinate bounds"
        )
        print("-" * 60)

        print(
            f"Minimum: "
            f"{bounds_minimum}"
        )

        print(
            f"Maximum: "
            f"{bounds_maximum}"
        )

    # ------------------------------------------------------------------
    # Validation report
    # ------------------------------------------------------------------

    print("\nValidation")
    print("-" * 60)

    for name, value in (
        validation.items()
    ):
        if isinstance(value, bool):
            result = (
                "PASS"
                if value
                else "FAIL"
            )

            print(
                f"{name:28} "
                f"{result}"
            )

    # ------------------------------------------------------------------
    # Spatial metadata warning
    # ------------------------------------------------------------------

    if (
        original_affine_source
        == "fallback"
    ):
        print("\nWARNING")
        print("-" * 60)

        print(
            "The original dataset does not "
            "contain defined qform/sform "
            "spatial metadata."
        )

        print(
            "STL coordinates therefore follow "
            "the NIfTI fallback spatial "
            "interpretation."
        )

        print(
            "Canonical RAS reorientation does "
            "not establish an authoritative "
            "scanner coordinate system."
        )

    # ------------------------------------------------------------------
    # Output files
    # ------------------------------------------------------------------

    print("\nOutputs")
    print("-" * 60)

    print(
        f"Overlay:  "
        f"{overlay_path}"
    )

    print(
        f"STL:      "
        f"{stl_path}"
    )

    print(
        f"Metadata: "
        f"{metadata_path}"
    )


if __name__ == "__main__":
    main()
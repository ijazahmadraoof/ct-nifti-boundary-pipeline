"""Select and export a demonstration BC patch from local CT data."""

from pathlib import Path

import numpy as np

from ct_pipeline.io import (
    get_affine_source,
    load_nifti,
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
from ct_pipeline.visualization import (
    save_boundary_overlay,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
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

    original_image = load_nifti(input_path)

    original_affine_source = get_affine_source(
        original_image
    )

    # Work in canonical orientation so the directional controls have
    # a consistent RAS voxel-axis interpretation.
    image = reorient_to_canonical(
        original_image
    )

    data = np.asarray(
        image.dataobj,
        dtype=float,
    )

    threshold = estimate_otsu_threshold(
        data,
        bins=256,
    )

    material_mask = threshold_material(
        data,
        threshold=threshold,
    )

    direction = "+Z"

    # Demonstration ROI only. This is not being claimed as a
    # physically calibrated load/support region.
    selected = select_boundary_patch(
        material_mask,
        direction=direction,
        x_range=(0.25, 0.75),
        y_range=(0.25, 0.75),
        z_range=(0.75, 1.00),
        surface_band_voxels=1,
        largest_component=True,
        connectivity=1,
    )

    selected_indices = np.argwhere(
        selected
    )

    triangles = voxel_faces_to_triangles(
        selected_indices,
        direction,
        image.affine,
    )

    stl_path = (
        output_dir
        / "demo_plus_z_boundary.stl"
    )

    write_ascii_stl(
        triangles,
        stl_path,
        solid_name="real_cube_demo_plus_z",
    )

    overlay_path = save_boundary_overlay(
        image,
        selected,
        direction,
        output_dir / "01_boundary_overlay.png",
        title="Real CT cube — demonstration boundary patch",
    )

    print("\nReal CT boundary-patch demonstration")
    print("=" * 60)

    print(f"Original affine source: {original_affine_source}")
    print(f"Working orientation:    RAS")
    print(f"Otsu threshold:         {threshold:.6f}")
    print(f"Direction:              {direction}")

    print("\nROI")
    print("-" * 60)
    print("X: 25% -> 75%")
    print("Y: 25% -> 75%")
    print("Z: 75% -> 100%")
    print("Surface band: 1 voxel")
    print("Largest component: yes")

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
        print("\nCoordinate bounds")
        print("-" * 60)
        print(
            f"Minimum: "
            f"{triangles.min(axis=(0, 1))}"
        )
        print(
            f"Maximum: "
            f"{triangles.max(axis=(0, 1))}"
        )

    if original_affine_source == "fallback":
        print(
            "\nWARNING: The original dataset does not contain "
            "defined qform/sform spatial metadata."
        )
        print(
            "STL coordinates therefore follow the NIfTI fallback "
            "spatial interpretation."
        )

    print("\nOutputs")
    print("-" * 60)
    print(overlay_path)
    print(stl_path)


if __name__ == "__main__":
    main()
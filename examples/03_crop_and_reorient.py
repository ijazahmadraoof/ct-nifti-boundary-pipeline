"""Demonstrate cropping and canonical reorientation on local CT data."""

from pathlib import Path

import nibabel as nib
import numpy as np

from ct_pipeline.coordinates import physical_bounds
from ct_pipeline.io import get_affine_source, load_nifti
from ct_pipeline.preprocessing import crop_nifti, reorient_to_canonical
from ct_pipeline.visualization import save_orthogonal_slices


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
        / "real_cube_preprocessing"
    )

    image = load_nifti(input_path)

    print("\nOriginal volume")
    print("=" * 50)
    print(f"Shape:          {image.shape}")
    print(f"Orientation:    {nib.aff2axcodes(image.affine)}")
    print(f"Affine source:  {get_affine_source(image)}")

    if get_affine_source(image) == "fallback":
        print(
            "\nWARNING: This dataset has no defined qform/sform. "
            "The spatial transform below is a fallback interpretation."
        )

    save_orthogonal_slices(
        image,
        output_dir / "01_original.png",
        "Original CT-derived cube",
    )

    # Small diagnostic crop.
    # The specimen is already cropped; this simply exercises and validates
    # our geometry-preserving crop implementation.
    cropped = crop_nifti(
        image,
        x_range=(16, 240),
        y_range=(16, 240),
        z_range=(16, 240),
    )

    print("\nCropped volume")
    print("=" * 50)
    print(f"Shape:          {cropped.shape}")
    print(f"Orientation:    {nib.aff2axcodes(cropped.affine)}")

    save_orthogonal_slices(
        cropped,
        output_dir / "02_cropped.png",
        "Diagnostic crop",
    )

    minimum_before, maximum_before = physical_bounds(
        cropped.shape,
        cropped.affine,
    )

    canonical = reorient_to_canonical(cropped)

    minimum_after, maximum_after = physical_bounds(
        canonical.shape,
        canonical.affine,
    )

    print("\nCanonical volume")
    print("=" * 50)
    print(f"Shape:          {canonical.shape}")
    print(f"Orientation:    {nib.aff2axcodes(canonical.affine)}")

    print("\nPhysical bounds before reorientation:")
    print(f"Minimum: {minimum_before}")
    print(f"Maximum: {maximum_before}")

    print("\nPhysical bounds after reorientation:")
    print(f"Minimum: {minimum_after}")
    print(f"Maximum: {maximum_after}")

    bounds_preserved = (
        np.allclose(minimum_before, minimum_after)
        and np.allclose(maximum_before, maximum_after)
    )

    print(f"\nPhysical bounds preserved: {bounds_preserved}")

    save_orthogonal_slices(
        canonical,
        output_dir / "03_canonical.png",
        "Canonical RAS representation",
    )

    print(f"\nFigures written to:\n{output_dir}")


if __name__ == "__main__":
    main()
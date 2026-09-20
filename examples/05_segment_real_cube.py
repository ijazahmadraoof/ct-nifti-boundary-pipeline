"""Inspect and segment the local CT-derived cube."""

from pathlib import Path

import numpy as np

from ct_pipeline.io import load_nifti
from ct_pipeline.segmentation import (
    estimate_otsu_threshold,
    threshold_material,
)
from ct_pipeline.visualization import (
    save_intensity_histogram,
    save_segmentation_slices,
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
        / "real_cube_segmentation"
    )

    image = load_nifti(input_path)

    data = np.asarray(
        image.dataobj,
        dtype=float,
    )

    finite_values = data[np.isfinite(data)]

    percentiles = np.percentile(
        finite_values,
        [
            0,
            1,
            5,
            10,
            25,
            50,
            75,
            90,
            95,
            99,
            100,
        ],
    )

    threshold = estimate_otsu_threshold(
        data,
        bins=256,
    )

    material_mask = threshold_material(
        data,
        threshold=threshold,
    )

    total_voxels = material_mask.size
    material_voxels = int(
        material_mask.sum()
    )

    material_fraction = (
        material_voxels
        / total_voxels
    )

    print("\nReal CT cube segmentation diagnostic")
    print("=" * 55)

    print(f"Shape:               {image.shape}")
    print(
        f"Intensity range:     "
        f"{finite_values.min():.6f} -> "
        f"{finite_values.max():.6f}"
    )

    print("\nIntensity percentiles")
    print("-" * 55)

    labels = (
        "0%",
        "1%",
        "5%",
        "10%",
        "25%",
        "50%",
        "75%",
        "90%",
        "95%",
        "99%",
        "100%",
    )

    for label, value in zip(
        labels,
        percentiles,
    ):
        print(
            f"{label:>4}: {value:.6f}"
        )

    print("\nSegmentation")
    print("-" * 55)
    print(
        f"Otsu candidate threshold: "
        f"{threshold:.6f}"
    )
    print(
        f"Material voxels:          "
        f"{material_voxels:,}"
    )
    print(
        f"Material fraction:        "
        f"{material_fraction:.2%}"
    )

    histogram_path = save_intensity_histogram(
        image,
        output_dir / "01_intensity_histogram.png",
        threshold=threshold,
    )

    segmentation_path = save_segmentation_slices(
        image,
        material_mask,
        output_dir / "02_segmentation_slices.png",
    )

    print("\nDiagnostic figures")
    print("-" * 55)
    print(histogram_path)
    print(segmentation_path)


if __name__ == "__main__":
    main()
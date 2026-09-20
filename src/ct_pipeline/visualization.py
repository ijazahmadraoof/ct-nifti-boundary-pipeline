"""Visualization utilities for 3D engineering image volumes."""

from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np


def save_orthogonal_slices(
    image: nib.Nifti1Image,
    output_path: str | Path,
    title: str,
) -> Path:
    """
    Save orthogonal mid-plane views of a 3D NIfTI volume.

    The displayed planes correspond to constant voxel-index directions,
    rather than assuming anatomical terminology.
    """
    if len(image.shape) != 3:
        raise ValueError("Visualization currently supports only 3D volumes.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = np.asarray(image.dataobj)

    i_mid = data.shape[0] // 2
    j_mid = data.shape[1] // 2
    k_mid = data.shape[2] // 2

    slices = (
        data[i_mid, :, :].T,
        data[:, j_mid, :].T,
        data[:, :, k_mid].T,
    )

    labels = (
        f"i = {i_mid}",
        f"j = {j_mid}",
        f"k = {k_mid}",
    )

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    for axis, image_slice, label in zip(axes, slices, labels):
        axis.imshow(image_slice, cmap="gray", origin="lower")
        axis.set_title(label)
        axis.set_xlabel("voxel index")
        axis.set_ylabel("voxel index")

    fig.suptitle(title)
    fig.tight_layout()

    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

    return output_path

def save_intensity_histogram(
    image: nib.Nifti1Image,
    output_path: str | Path,
    threshold: float | None = None,
    bins: int = 256,
) -> Path:
    """Save the intensity distribution of a NIfTI volume."""
    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = np.asarray(
        image.dataobj,
        dtype=float,
    )

    values = data[np.isfinite(data)]

    fig, axis = plt.subplots(
        figsize=(8, 5)
    )

    axis.hist(
        values.ravel(),
        bins=bins,
    )

    axis.set_yscale("log")

    if threshold is not None:
        axis.axvline(
            threshold,
            linestyle="--",
            label=f"Candidate threshold = {threshold:.3f}",
        )
        axis.legend()

    axis.set_xlabel("Intensity")
    axis.set_ylabel("Voxel count")
    axis.set_title("CT intensity distribution")

    fig.tight_layout()
    fig.savefig(
        output_path,
        dpi=160,
        bbox_inches="tight",
    )
    plt.close(fig)

    return output_path


def save_segmentation_slices(
    image: nib.Nifti1Image,
    material_mask: np.ndarray,
    output_path: str | Path,
) -> Path:
    """
    Compare image intensities and binary segmentation on three mid-planes.
    """
    if material_mask.shape != image.shape:
        raise ValueError(
            "Material mask must have the same shape as the image."
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = np.asarray(image.dataobj)

    i_mid = data.shape[0] // 2
    j_mid = data.shape[1] // 2
    k_mid = data.shape[2] // 2

    image_slices = (
        data[i_mid, :, :].T,
        data[:, j_mid, :].T,
        data[:, :, k_mid].T,
    )

    mask_slices = (
        material_mask[i_mid, :, :].T,
        material_mask[:, j_mid, :].T,
        material_mask[:, :, k_mid].T,
    )

    labels = (
        f"i = {i_mid}",
        f"j = {j_mid}",
        f"k = {k_mid}",
    )

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(12, 8),
    )

    for column, label in enumerate(labels):
        axes[0, column].imshow(
            image_slices[column],
            cmap="gray",
            origin="lower",
        )
        axes[0, column].set_title(
            f"Intensity: {label}"
        )

        axes[1, column].imshow(
            mask_slices[column],
            cmap="gray",
            origin="lower",
        )
        axes[1, column].set_title(
            f"Material mask: {label}"
        )

        for row in range(2):
            axes[row, column].set_xlabel(
                "voxel index"
            )
            axes[row, column].set_ylabel(
                "voxel index"
            )

    fig.suptitle(
        "CT segmentation diagnostic"
    )
    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=160,
        bbox_inches="tight",
    )
    plt.close(fig)

    return output_path
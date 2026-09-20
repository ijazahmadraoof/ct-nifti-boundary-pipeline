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
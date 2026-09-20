"""Material segmentation utilities for volumetric engineering image data."""

import numpy as np


def threshold_material(
    data: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """
    Create a binary material mask using a lower intensity threshold.

    Voxels with intensities greater than or equal to ``threshold`` are
    classified as material.

    Parameters
    ----------
    data:
        Three-dimensional image intensity array.

    threshold:
        Minimum intensity considered to represent material.

    Returns
    -------
    numpy.ndarray
        Boolean array where True represents material and False represents
        background or void.
    """
    if data.ndim != 3:
        raise ValueError("Material segmentation requires a 3D array.")

    return np.isfinite(data) & (data >= threshold)
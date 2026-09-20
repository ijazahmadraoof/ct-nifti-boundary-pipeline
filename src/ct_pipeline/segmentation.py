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

def estimate_otsu_threshold(
    data: np.ndarray,
    bins: int = 256,
) -> float:
    """
    Estimate a binary segmentation threshold using Otsu's method.

    Otsu's method searches for the intensity threshold that maximizes
    separation between two intensity classes.

    The result should be treated as a diagnostic candidate rather than
    an unquestioned physical material threshold.
    """
    values = np.asarray(data, dtype=float)
    values = values[np.isfinite(values)]

    if values.size == 0:
        raise ValueError("Cannot estimate a threshold from empty data.")

    if bins < 2:
        raise ValueError("bins must be at least 2.")

    minimum = float(values.min())
    maximum = float(values.max())

    if np.isclose(minimum, maximum):
        return minimum

    histogram, edges = np.histogram(
        values,
        bins=bins,
        range=(minimum, maximum),
    )

    centers = 0.5 * (
        edges[:-1] + edges[1:]
    )

    probabilities = (
        histogram.astype(float)
        / histogram.sum()
    )

    cumulative_probability = np.cumsum(
        probabilities
    )

    cumulative_mean = np.cumsum(
        probabilities * centers
    )

    total_mean = cumulative_mean[-1]

    denominator = (
        cumulative_probability
        * (1.0 - cumulative_probability)
    )

    between_class_variance = np.zeros_like(
        denominator
    )

    valid = denominator > 0.0

    between_class_variance[valid] = (
        (
            total_mean
            * cumulative_probability[valid]
            - cumulative_mean[valid]
        )
        ** 2
        / denominator[valid]
    )

    threshold_index = int(
        np.argmax(between_class_variance)
    )

    return float(centers[threshold_index])
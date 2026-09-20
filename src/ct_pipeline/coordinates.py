"""Coordinate transformations for voxel-based engineering image volumes."""

import numpy as np


def voxel_to_physical(
    voxel_coordinates: np.ndarray | list | tuple,
    affine: np.ndarray,
) -> np.ndarray:
    """
    Transform voxel-centre coordinates into physical coordinates.

    Parameters
    ----------
    voxel_coordinates:
        Single coordinate ``(i, j, k)`` or an array with shape (..., 3).

    affine:
        4x4 voxel-to-physical transformation matrix.

    Returns
    -------
    numpy.ndarray
        Physical coordinates with the same leading shape.
    """
    points = np.asarray(voxel_coordinates, dtype=float)

    if points.shape[-1] != 3:
        raise ValueError("Voxel coordinates must have shape (..., 3).")

    original_shape = points.shape
    flat_points = points.reshape(-1, 3)

    homogeneous = np.column_stack(
        [flat_points, np.ones(len(flat_points))]
    )

    transformed = homogeneous @ affine.T

    return transformed[:, :3].reshape(original_shape)


def physical_to_voxel(
    physical_coordinates: np.ndarray | list | tuple,
    affine: np.ndarray,
) -> np.ndarray:
    """
    Transform physical coordinates back into continuous voxel coordinates.

    The returned values are not rounded because a physical point does not
    necessarily lie exactly at a voxel centre.
    """
    inverse_affine = np.linalg.inv(affine)

    return voxel_to_physical(
        physical_coordinates,
        inverse_affine,
    )


def volume_corner_coordinates(shape: tuple[int, int, int]) -> np.ndarray:
    """
    Return the eight outer voxel-cell corners of a 3D volume.

    NIfTI voxel indices refer to voxel centres. Therefore, the outer extent of
    a volume spans from -0.5 to (size - 0.5) along each voxel axis.
    """
    if len(shape) != 3:
        raise ValueError("Shape must describe a 3D volume.")

    x_max = shape[0] - 0.5
    y_max = shape[1] - 0.5
    z_max = shape[2] - 0.5

    return np.array(
        [
            [-0.5, -0.5, -0.5],
            [-0.5, -0.5, z_max],
            [-0.5, y_max, -0.5],
            [-0.5, y_max, z_max],
            [x_max, -0.5, -0.5],
            [x_max, -0.5, z_max],
            [x_max, y_max, -0.5],
            [x_max, y_max, z_max],
        ],
        dtype=float,
    )


def physical_bounds(
    shape: tuple[int, int, int],
    affine: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate the axis-aligned physical bounds of a 3D NIfTI volume.

    Returns
    -------
    tuple
        ``(minimum_coordinates, maximum_coordinates)``
    """
    voxel_corners = volume_corner_coordinates(shape)
    physical_corners = voxel_to_physical(voxel_corners, affine)

    return (
        physical_corners.min(axis=0),
        physical_corners.max(axis=0),
    )
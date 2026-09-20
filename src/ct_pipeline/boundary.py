"""Directional boundary-surface detection on binary voxel volumes."""

from typing import Literal

import numpy as np


BoundaryDirection = Literal[
    "+X",
    "-X",
    "+Y",
    "-Y",
    "+Z",
    "-Z",
]


_DIRECTION_MAP: dict[str, tuple[int, int]] = {
    "+X": (0, 1),
    "-X": (0, -1),
    "+Y": (1, 1),
    "-Y": (1, -1),
    "+Z": (2, 1),
    "-Z": (2, -1),
}


def find_exposed_voxels(
    material_mask: np.ndarray,
    direction: BoundaryDirection,
) -> np.ndarray:
    """
    Identify material voxels exposed in one specified direction.

    A material voxel is considered exposed when its neighbouring voxel in the
    requested direction is background/void. Material voxels located directly
    on the outer volume boundary are also considered exposed.

    Parameters
    ----------
    material_mask:
        Three-dimensional boolean array where True represents material.

    direction:
        Direction in which exposure is tested:
        ``+X``, ``-X``, ``+Y``, ``-Y``, ``+Z`` or ``-Z``.

    Returns
    -------
    numpy.ndarray
        Boolean mask containing True only for exposed material voxels.
    """
    if material_mask.ndim != 3:
        raise ValueError("Boundary extraction requires a 3D material mask.")

    if material_mask.dtype != np.bool_:
        material_mask = material_mask.astype(bool)

    if direction not in _DIRECTION_MAP:
        raise ValueError(
            f"Unsupported direction: {direction}. "
            f"Choose one of {tuple(_DIRECTION_MAP)}."
        )

    axis, step = _DIRECTION_MAP[direction]

    exposed = np.zeros_like(material_mask, dtype=bool)

    current = [slice(None)] * 3
    neighbour = [slice(None)] * 3

    if step > 0:
        current[axis] = slice(0, -1)
        neighbour[axis] = slice(1, None)

        exposed[tuple(current)] = (
            material_mask[tuple(current)]
            & ~material_mask[tuple(neighbour)]
        )

        outer = [slice(None)] * 3
        outer[axis] = -1
        exposed[tuple(outer)] = material_mask[tuple(outer)]

    else:
        current[axis] = slice(1, None)
        neighbour[axis] = slice(0, -1)

        exposed[tuple(current)] = (
            material_mask[tuple(current)]
            & ~material_mask[tuple(neighbour)]
        )

        outer = [slice(None)] * 3
        outer[axis] = 0
        exposed[tuple(outer)] = material_mask[tuple(outer)]

    return exposed


def exposed_voxel_indices(
    material_mask: np.ndarray,
    direction: BoundaryDirection,
) -> np.ndarray:
    """
    Return ``(i, j, k)`` indices of exposed material voxels.
    """
    exposed = find_exposed_voxels(
        material_mask,
        direction,
    )

    return np.argwhere(exposed)
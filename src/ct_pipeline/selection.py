"""Selection utilities for simulation boundary-condition patches."""

import numpy as np
from scipy import ndimage

from ct_pipeline.boundary import (
    BoundaryDirection,
    find_exposed_voxels,
)


_DIRECTION_AXIS_STEP: dict[str, tuple[int, int]] = {
    "+X": (0, 1),
    "-X": (0, -1),
    "+Y": (1, 1),
    "-Y": (1, -1),
    "+Z": (2, 1),
    "-Z": (2, -1),
}


def _fraction_to_slice(
    length: int,
    fraction_range: tuple[float, float],
) -> slice:
    """
    Convert a normalized range in [0, 1] to a voxel-index slice.
    """
    start_fraction, stop_fraction = fraction_range

    if not (
        0.0 <= start_fraction < stop_fraction <= 1.0
    ):
        raise ValueError(
            "Fractional ROI ranges must satisfy "
            "0 <= start < stop <= 1."
        )

    start = int(np.floor(start_fraction * length))
    stop = int(np.ceil(stop_fraction * length))

    return slice(start, stop)


def apply_fractional_roi(
    mask: np.ndarray,
    x_range: tuple[float, float] = (0.0, 1.0),
    y_range: tuple[float, float] = (0.0, 1.0),
    z_range: tuple[float, float] = (0.0, 1.0),
) -> np.ndarray:
    """
    Restrict a 3D boolean mask to a fractional region of interest.

    For example, ``x_range=(0.2, 0.8)`` keeps the central 60 percent
    of the volume along voxel axis 0.
    """
    if mask.ndim != 3:
        raise ValueError("ROI selection requires a 3D mask.")

    slices = (
        _fraction_to_slice(mask.shape[0], x_range),
        _fraction_to_slice(mask.shape[1], y_range),
        _fraction_to_slice(mask.shape[2], z_range),
    )

    selected = np.zeros_like(mask, dtype=bool)
    selected[slices] = mask[slices]

    return selected


def filter_surface_band(
    exposed_mask: np.ndarray,
    direction: BoundaryDirection,
    band_voxels: int,
) -> np.ndarray:
    """
    Keep exposed voxels close to the directional outer surface.

    ``band_voxels=1`` keeps only the extreme exposed layer.
    Larger values allow additional layers immediately behind it.
    """
    if exposed_mask.ndim != 3:
        raise ValueError("Surface-band filtering requires a 3D mask.")

    if band_voxels < 1:
        raise ValueError("band_voxels must be at least 1.")

    if direction not in _DIRECTION_AXIS_STEP:
        raise ValueError(f"Unsupported direction: {direction}")

    indices = np.argwhere(exposed_mask)

    if len(indices) == 0:
        return np.zeros_like(exposed_mask, dtype=bool)

    axis, step = _DIRECTION_AXIS_STEP[direction]
    positions = indices[:, axis]

    if step > 0:
        extreme = positions.max()
        keep = positions >= extreme - band_voxels + 1
    else:
        extreme = positions.min()
        keep = positions <= extreme + band_voxels - 1

    selected_indices = indices[keep]

    selected = np.zeros_like(exposed_mask, dtype=bool)
    selected[tuple(selected_indices.T)] = True

    return selected


def keep_largest_component(
    mask: np.ndarray,
    connectivity: int = 1,
) -> np.ndarray:
    """
    Keep only the largest connected voxel component.

    Parameters
    ----------
    mask:
        Three-dimensional boolean mask.

    connectivity:
        SciPy 3D connectivity:
        1 = face-connected,
        2 = face/edge-connected,
        3 = face/edge/corner-connected.
    """
    if mask.ndim != 3:
        raise ValueError("Connected-component filtering requires a 3D mask.")

    if connectivity not in (1, 2, 3):
        raise ValueError("connectivity must be 1, 2, or 3.")

    structure = ndimage.generate_binary_structure(
        rank=3,
        connectivity=connectivity,
    )

    labels, component_count = ndimage.label(
        mask,
        structure=structure,
    )

    if component_count == 0:
        return np.zeros_like(mask, dtype=bool)

    component_sizes = np.bincount(labels.ravel())
    component_sizes[0] = 0

    largest_label = int(component_sizes.argmax())

    return labels == largest_label


def select_boundary_patch(
    material_mask: np.ndarray,
    direction: BoundaryDirection,
    *,
    x_range: tuple[float, float] = (0.0, 1.0),
    y_range: tuple[float, float] = (0.0, 1.0),
    z_range: tuple[float, float] = (0.0, 1.0),
    surface_band_voxels: int | None = None,
    largest_component: bool = False,
    connectivity: int = 1,
) -> np.ndarray:
    """
    Select a directional boundary-condition patch.

    Processing order:

    1. detect directional exposed material voxels
    2. restrict them to a fractional ROI
    3. optionally retain only the directional surface band
    4. optionally retain the largest connected component
    """
    selected = find_exposed_voxels(
        material_mask,
        direction,
    )

    selected = apply_fractional_roi(
        selected,
        x_range=x_range,
        y_range=y_range,
        z_range=z_range,
    )

    if surface_band_voxels is not None:
        selected = filter_surface_band(
            selected,
            direction,
            surface_band_voxels,
        )

    if largest_component:
        selected = keep_largest_component(
            selected,
            connectivity=connectivity,
        )

    return selected
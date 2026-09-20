"""Utilities for creating reproducible synthetic engineering image volumes."""

from pathlib import Path

import nibabel as nib
import numpy as np


def create_t_shape_volume(
    shape: tuple[int, int, int] = (96, 64, 128),
) -> np.ndarray:
    """
    Create a simple synthetic T-shaped specimen.

    The specimen is represented as a binary 3D voxel volume:
    0 = background
    1 = material
    """
    volume = np.zeros(shape, dtype=np.float32)

    nx, ny, nz = shape

    cx = nx // 2
    cy = ny // 2

    # Vertical stem.
    volume[
        cx - 10 : cx + 10,
        cy - 10 : cy + 10,
        15:95,
    ] = 1.0

    # Horizontal arms.
    volume[
        cx - 35 : cx + 35,
        cy - 10 : cy + 10,
        75:95,
    ] = 1.0

    return volume


def create_affine(
    voxel_spacing: tuple[float, float, float] = (0.25, 0.25, 0.50),
    origin: tuple[float, float, float] = (10.0, 20.0, 30.0),
) -> np.ndarray:
    """
    Create a simple axis-aligned voxel-to-physical coordinate transform.

    Physical coordinates are expressed in millimetres.
    """
    sx, sy, sz = voxel_spacing
    ox, oy, oz = origin

    return np.array(
        [
            [sx, 0.0, 0.0, ox],
            [0.0, sy, 0.0, oy],
            [0.0, 0.0, sz, oz],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def save_synthetic_nifti(
    output_path: str | Path,
    voxel_spacing: tuple[float, float, float] = (0.25, 0.25, 0.50),
    origin: tuple[float, float, float] = (10.0, 20.0, 30.0),
) -> Path:
    """
    Create and save a synthetic T-shaped engineering specimen as NIfTI.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    volume = create_t_shape_volume()
    affine = create_affine(voxel_spacing, origin)

    image = nib.Nifti1Image(volume, affine)

    # Explicitly describe the physical coordinate system in the header.
    image.header.set_xyzt_units(xyz="mm")
    image.set_qform(affine, code=1)
    image.set_sform(affine, code=1)

    nib.save(image, output_path)

    return output_path
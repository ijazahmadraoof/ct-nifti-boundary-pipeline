"""Input/output utilities for NIfTI engineering image volumes."""

from pathlib import Path

import nibabel as nib
import numpy as np


def load_nifti(file_path: str | Path) -> nib.Nifti1Image:
    """
    Load a NIfTI image from disk.

    Parameters
    ----------
    file_path:
        Path to a .nii or .nii.gz file.

    Returns
    -------
    nib.Nifti1Image
        Loaded NIfTI image.

    Raises
    ------
    FileNotFoundError
        If the supplied path does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"NIfTI file not found: {path}")

    return nib.load(path)


def get_affine_source(image: nib.Nifti1Image) -> str:
    """
    Determine where the spatial affine information originates.

    NIfTI normally stores spatial transforms in the sform or qform.
    If neither is defined, NiBabel constructs a fallback affine from
    basic header information.
    """
    header = image.header

    _, sform_code = header.get_sform(coded=True)
    _, qform_code = header.get_qform(coded=True)

    if sform_code > 0:
        return "sform"

    if qform_code > 0:
        return "qform"

    return "fallback"


def inspect_nifti(file_path: str | Path) -> dict:
    """
    Inspect important geometric and intensity information in a NIfTI volume.

    The returned dictionary is intended for diagnostics and validation before
    geometry is passed into later processing or simulation steps.
    """
    image = load_nifti(file_path)
    header = image.header

    shape = image.shape
    spacing = tuple(float(value) for value in header.get_zooms()[:3])

    spatial_units, temporal_units = header.get_xyzt_units()

    # Load the voxel values for basic statistics.
    data = np.asarray(image.dataobj)

    physical_size = tuple(
        float(shape[i] * spacing[i])
        for i in range(min(3, len(shape)))
    )

    orientation = nib.aff2axcodes(image.affine)

    _, qform_code = header.get_qform(coded=True)
    _, sform_code = header.get_sform(coded=True)

    return {
        "shape": shape,
        "dtype": str(data.dtype),
        "voxel_spacing": spacing,
        "physical_size": physical_size,
        "spatial_units": spatial_units or "unknown",
        "temporal_units": temporal_units or "unknown",
        "intensity_min": float(np.min(data)),
        "intensity_max": float(np.max(data)),
        "intensity_mean": float(np.mean(data)),
        "qform_code": int(qform_code),
        "sform_code": int(sform_code),
        "affine_source": get_affine_source(image),
        "orientation": orientation,
        "affine": image.affine.copy(),
    }
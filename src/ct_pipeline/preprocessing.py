"""Preprocessing utilities for CT-derived NIfTI volumes."""

import nibabel as nib
import numpy as np


def crop_nifti(
    image: nib.Nifti1Image,
    x_range: tuple[int, int],
    y_range: tuple[int, int],
    z_range: tuple[int, int],
) -> nib.Nifti1Image:
    """
    Crop a 3D NIfTI volume while preserving physical coordinates.

    The affine matrix is updated so that voxel (0, 0, 0) in the cropped
    image has the same physical location as voxel (x_start, y_start, z_start)
    in the original image.

    Parameters
    ----------
    image:
        Input 3D NIfTI image.

    x_range, y_range, z_range:
        Half-open index ranges ``(start, stop)`` for each voxel axis.

    Returns
    -------
    nib.Nifti1Image
        Cropped image with an updated affine transform.
    """
    if len(image.shape) != 3:
        raise ValueError("crop_nifti currently supports only 3D volumes.")

    ranges = (x_range, y_range, z_range)

    for axis, (start, stop) in enumerate(ranges):
        if start < 0:
            raise ValueError(f"Crop start for axis {axis} cannot be negative.")

        if stop <= start:
            raise ValueError(
                f"Crop stop must be greater than crop start for axis {axis}."
            )

        if stop > image.shape[axis]:
            raise ValueError(
                f"Crop range {start}:{stop} exceeds axis {axis} "
                f"size {image.shape[axis]}."
            )

    x_start, x_stop = x_range
    y_start, y_stop = y_range
    z_start, z_stop = z_range

    data = np.asanyarray(image.dataobj)

    cropped_data = data[
        x_start:x_stop,
        y_start:y_stop,
        z_start:z_stop,
    ]

    # New voxel coordinates refer to positions in the original array:
    #
    # old_i = new_i + x_start
    # old_j = new_j + y_start
    # old_k = new_k + z_start
    #
    # Therefore:
    #
    # new_affine = old_affine @ translation(start_indices)
    index_translation = np.eye(4, dtype=float)
    index_translation[:3, 3] = [
        x_start,
        y_start,
        z_start,
    ]

    new_affine = image.affine @ index_translation

    header = image.header.copy()

    cropped_image = nib.Nifti1Image(
        cropped_data,
        new_affine,
        header=header,
    )

    # Preserve explicitly defined spatial transforms when available.
    _, qform_code = image.header.get_qform(coded=True)
    _, sform_code = image.header.get_sform(coded=True)

    if qform_code > 0:
        cropped_image.set_qform(new_affine, code=int(qform_code))

    if sform_code > 0:
        cropped_image.set_sform(new_affine, code=int(sform_code))

    return cropped_image


def reorient_to_canonical(
    image: nib.Nifti1Image,
) -> nib.Nifti1Image:
    """
    Reorient a NIfTI volume to the closest canonical RAS orientation.

    This performs axis permutations and/or flips while updating the affine
    transform so that the physical geometry remains consistent.

    It does not perform arbitrary-angle interpolation.
    """
    return nib.as_closest_canonical(image)
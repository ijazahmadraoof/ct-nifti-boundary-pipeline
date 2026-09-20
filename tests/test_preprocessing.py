import nibabel as nib
import numpy as np

from ct_pipeline.coordinates import (
    physical_bounds,
    voxel_to_physical,
)
from ct_pipeline.preprocessing import (
    crop_nifti,
    reorient_to_canonical,
)


AFFINE = np.array(
    [
        [0.25, 0.0, 0.0, 10.0],
        [0.0, 0.25, 0.0, 20.0],
        [0.0, 0.0, 0.50, 30.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)


def create_test_image() -> nib.Nifti1Image:
    data = np.zeros((96, 64, 128), dtype=np.float32)

    image = nib.Nifti1Image(data, AFFINE)

    image.set_qform(AFFINE, code=1)
    image.set_sform(AFFINE, code=1)
    image.header.set_xyzt_units(xyz="mm")

    return image


def test_crop_shape() -> None:
    image = create_test_image()

    cropped = crop_nifti(
        image,
        x_range=(10, 50),
        y_range=(5, 35),
        z_range=(20, 80),
    )

    assert cropped.shape == (40, 30, 60)


def test_crop_preserves_physical_location() -> None:
    image = create_test_image()

    crop_start = (10, 5, 20)

    cropped = crop_nifti(
        image,
        x_range=(10, 50),
        y_range=(5, 35),
        z_range=(20, 80),
    )

    original_physical = voxel_to_physical(
        crop_start,
        image.affine,
    )

    cropped_origin_physical = voxel_to_physical(
        (0, 0, 0),
        cropped.affine,
    )

    assert np.allclose(
        original_physical,
        cropped_origin_physical,
    )


def test_crop_preserves_spatial_units() -> None:
    image = create_test_image()

    cropped = crop_nifti(
        image,
        x_range=(10, 50),
        y_range=(5, 35),
        z_range=(20, 80),
    )

    spatial_units, _ = cropped.header.get_xyzt_units()

    assert spatial_units == "mm"


def test_reorientation_to_ras_preserves_bounds() -> None:
    data = np.zeros((20, 30, 40), dtype=np.float32)

    las_affine = np.array(
        [
            [-0.25, 0.0, 0.0, 10.0],
            [0.0, 0.25, 0.0, 20.0],
            [0.0, 0.0, 0.50, 30.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    image = nib.Nifti1Image(data, las_affine)

    assert nib.aff2axcodes(image.affine) == ("L", "A", "S")

    minimum_before, maximum_before = physical_bounds(
        image.shape,
        image.affine,
    )

    canonical = reorient_to_canonical(image)

    assert nib.aff2axcodes(canonical.affine) == ("R", "A", "S")

    minimum_after, maximum_after = physical_bounds(
        canonical.shape,
        canonical.affine,
    )

    assert np.allclose(minimum_before, minimum_after)
    assert np.allclose(maximum_before, maximum_after)
import numpy as np

from ct_pipeline.coordinates import (
    physical_bounds,
    physical_to_voxel,
    voxel_to_physical,
)


AFFINE = np.array(
    [
        [0.25, 0.0, 0.0, 10.0],
        [0.0, 0.25, 0.0, 20.0],
        [0.0, 0.0, 0.50, 30.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)


def test_voxel_origin_to_physical() -> None:
    physical = voxel_to_physical((0, 0, 0), AFFINE)

    expected = np.array([10.0, 20.0, 30.0])

    assert np.allclose(physical, expected)


def test_voxel_to_physical_known_point() -> None:
    physical = voxel_to_physical((10, 20, 30), AFFINE)

    expected = np.array(
        [
            12.5,
            25.0,
            45.0,
        ]
    )

    assert np.allclose(physical, expected)


def test_round_trip_coordinate_transform() -> None:
    voxel = np.array([12.5, 8.0, 40.25])

    physical = voxel_to_physical(voxel, AFFINE)
    recovered_voxel = physical_to_voxel(physical, AFFINE)

    assert np.allclose(recovered_voxel, voxel)


def test_volume_physical_bounds() -> None:
    minimum, maximum = physical_bounds(
        shape=(96, 64, 128),
        affine=AFFINE,
    )

    expected_minimum = np.array(
        [9.875, 19.875, 29.75]
    )

    expected_maximum = np.array(
        [33.875, 35.875, 93.75]
    )

    assert np.allclose(minimum, expected_minimum)
    assert np.allclose(maximum, expected_maximum)
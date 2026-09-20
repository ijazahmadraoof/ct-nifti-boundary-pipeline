import numpy as np

from ct_pipeline.boundary import (
    exposed_voxel_indices,
    find_exposed_voxels,
)


def test_single_voxel_is_exposed_in_all_directions() -> None:
    mask = np.zeros((3, 3, 3), dtype=bool)
    mask[1, 1, 1] = True

    for direction in (
        "+X",
        "-X",
        "+Y",
        "-Y",
        "+Z",
        "-Z",
    ):
        exposed = exposed_voxel_indices(mask, direction)

        assert exposed.shape == (1, 3)
        assert np.array_equal(
            exposed[0],
            np.array([1, 1, 1]),
        )


def test_adjacent_voxels_hide_internal_x_face() -> None:
    mask = np.zeros((4, 3, 3), dtype=bool)

    mask[1, 1, 1] = True
    mask[2, 1, 1] = True

    positive_x = exposed_voxel_indices(mask, "+X")
    negative_x = exposed_voxel_indices(mask, "-X")

    assert np.array_equal(
        positive_x,
        np.array([[2, 1, 1]]),
    )

    assert np.array_equal(
        negative_x,
        np.array([[1, 1, 1]]),
    )


def test_volume_edge_counts_as_exposed() -> None:
    mask = np.zeros((3, 3, 3), dtype=bool)

    mask[2, 1, 1] = True

    exposed = find_exposed_voxels(mask, "+X")

    assert exposed[2, 1, 1]


def test_internal_voxel_is_not_directionally_exposed() -> None:
    mask = np.ones((3, 3, 3), dtype=bool)

    positive_x = find_exposed_voxels(mask, "+X")

    assert not positive_x[1, 1, 1]
    assert positive_x[2, 1, 1]
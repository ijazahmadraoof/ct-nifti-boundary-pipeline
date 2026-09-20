import numpy as np

from ct_pipeline.selection import (
    apply_fractional_roi,
    filter_surface_band,
    keep_largest_component,
    select_boundary_patch,
)


def test_fractional_roi() -> None:
    mask = np.ones((10, 10, 10), dtype=bool)

    selected = apply_fractional_roi(
        mask,
        x_range=(0.2, 0.5),
    )

    assert selected.sum() == 300
    assert selected[2:5].all()
    assert not selected[:2].any()
    assert not selected[5:].any()


def test_positive_surface_band_keeps_extreme_layers() -> None:
    mask = np.zeros((5, 5, 6), dtype=bool)

    mask[1, 1, 1] = True
    mask[2, 2, 4] = True
    mask[3, 3, 5] = True

    selected = filter_surface_band(
        mask,
        direction="+Z",
        band_voxels=2,
    )

    assert not selected[1, 1, 1]
    assert selected[2, 2, 4]
    assert selected[3, 3, 5]


def test_largest_component_is_retained() -> None:
    mask = np.zeros((6, 6, 6), dtype=bool)

    mask[1, 1, 1] = True
    mask[2, 1, 1] = True
    mask[3, 1, 1] = True

    mask[5, 5, 5] = True

    selected = keep_largest_component(mask)

    assert selected.sum() == 3
    assert selected[1, 1, 1]
    assert selected[2, 1, 1]
    assert selected[3, 1, 1]
    assert not selected[5, 5, 5]


def test_surface_band_rejects_internal_void_surface() -> None:
    material = np.zeros((7, 7, 7), dtype=bool)

    # Solid specimen.
    material[1:6, 1:6, 1:6] = True

    # Internal void creates an additional +Z-facing material surface.
    material[3, 3, 4] = False

    selected = select_boundary_patch(
        material,
        direction="+Z",
        surface_band_voxels=1,
    )

    indices = np.argwhere(selected)

    assert len(indices) == 25
    assert np.all(indices[:, 2] == 5)


def test_roi_restricts_boundary_patch() -> None:
    material = np.zeros((6, 6, 6), dtype=bool)
    material[1:5, 1:5, 1:5] = True

    selected = select_boundary_patch(
        material,
        direction="+Z",
        x_range=(0.0, 0.5),
        surface_band_voxels=1,
    )

    indices = np.argwhere(selected)

    assert len(indices) == 8
    assert np.all(indices[:, 0] < 3)
    assert np.all(indices[:, 2] == 4)
import numpy as np

from ct_pipeline.segmentation import (
    estimate_otsu_threshold,
    threshold_material,
)


def test_threshold_material() -> None:
    data = np.array(
        [
            [[0.0, 0.4], [0.5, 1.0]],
            [[0.2, 0.7], [0.9, 0.1]],
        ],
        dtype=float,
    )

    material = threshold_material(
        data,
        threshold=0.5,
    )

    expected = np.array(
        [
            [[False, False], [True, True]],
            [[False, True], [True, False]],
        ]
    )

    assert np.array_equal(material, expected)

def test_otsu_threshold_separates_two_intensity_groups() -> None:
    background = np.linspace(
        0.0,
        0.2,
        1000,
    )

    material = np.linspace(
        0.8,
        1.0,
        1000,
    )

    data = np.concatenate(
        [background, material]
    ).reshape(20, 10, 10)

    threshold = estimate_otsu_threshold(
        data,
        bins=128,
    )

    assert 0.15 < threshold < 0.85
import numpy as np

from ct_pipeline.segmentation import threshold_material


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
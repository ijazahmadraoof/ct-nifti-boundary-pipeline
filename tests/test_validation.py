import numpy as np

from ct_pipeline.surface import (
    voxel_faces_to_triangles,
)
from ct_pipeline.validation import (
    validate_boundary_surface,
)


AFFINE = np.eye(4)


def test_valid_boundary_surface() -> None:
    voxel_indices = np.array(
        [
            [1, 1, 1],
            [2, 1, 1],
        ]
    )

    triangles = voxel_faces_to_triangles(
        voxel_indices,
        "+Z",
        AFFINE,
    )

    report = validate_boundary_surface(
        triangles,
        selected_voxel_count=2,
        direction="+Z",
        affine=AFFINE,
    )

    assert report["valid"]
    assert report["triangle_count"] == 4
    assert report["triangle_count_matches"]
    assert report["normals_consistent"]


def test_wrong_triangle_count_is_detected() -> None:
    voxel_indices = np.array(
        [[1, 1, 1]]
    )

    triangles = voxel_faces_to_triangles(
        voxel_indices,
        "+Z",
        AFFINE,
    )

    report = validate_boundary_surface(
        triangles,
        selected_voxel_count=2,
        direction="+Z",
        affine=AFFINE,
    )

    assert not report["valid"]
    assert not report[
        "triangle_count_matches"
    ]


def test_inverted_normal_is_detected() -> None:
    voxel_indices = np.array(
        [[1, 1, 1]]
    )

    triangles = voxel_faces_to_triangles(
        voxel_indices,
        "+Z",
        AFFINE,
    )

    inverted = triangles.copy()

    inverted[0] = (
        inverted[0][[0, 2, 1]]
    )

    report = validate_boundary_surface(
        inverted,
        selected_voxel_count=1,
        direction="+Z",
        affine=AFFINE,
    )

    assert not report["valid"]
    assert not report[
        "normals_consistent"
    ]
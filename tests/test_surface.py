import numpy as np

from ct_pipeline.surface import (
    physical_face_normal,
    voxel_faces_to_triangles,
)


IDENTITY = np.eye(4)


def normalized_normal(triangle: np.ndarray) -> np.ndarray:
    normal = np.cross(
        triangle[1] - triangle[0],
        triangle[2] - triangle[0],
    )

    return normal / np.linalg.norm(normal)


def test_all_face_directions_have_correct_normals() -> None:
    voxel = np.array([[1, 1, 1]])

    for direction in (
        "+X",
        "-X",
        "+Y",
        "-Y",
        "+Z",
        "-Z",
    ):
        triangles = voxel_faces_to_triangles(
            voxel,
            direction,
            IDENTITY,
        )

        assert triangles.shape == (2, 3, 3)

        expected_normal = physical_face_normal(
            direction,
            IDENTITY,
        )

        for triangle in triangles:
            actual_normal = normalized_normal(triangle)

            assert np.allclose(
                actual_normal,
                expected_normal,
            )


def test_positive_z_face_uses_voxel_cell_corners() -> None:
    triangles = voxel_faces_to_triangles(
        np.array([[2, 3, 4]]),
        "+Z",
        IDENTITY,
    )

    vertices = np.unique(
        triangles.reshape(-1, 3),
        axis=0,
    )

    expected = np.array(
        [
            [1.5, 2.5, 4.5],
            [1.5, 3.5, 4.5],
            [2.5, 2.5, 4.5],
            [2.5, 3.5, 4.5],
        ]
    )

    assert np.allclose(
        vertices,
        expected,
    )


def test_reflected_affine_preserves_outward_normal() -> None:
    affine = np.array(
        [
            [-0.25, 0.0, 0.0, 10.0],
            [0.0, 0.50, 0.0, 20.0],
            [0.0, 0.0, 0.75, 30.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    triangles = voxel_faces_to_triangles(
        np.array([[1, 1, 1]]),
        "+X",
        affine,
    )

    expected_normal = physical_face_normal(
        "+X",
        affine,
    )

    for triangle in triangles:
        assert np.allclose(
            normalized_normal(triangle),
            expected_normal,
        )


def test_multiple_faces_produce_two_triangles_each() -> None:
    voxels = np.array(
        [
            [1, 1, 1],
            [2, 1, 1],
            [3, 1, 1],
        ]
    )

    triangles = voxel_faces_to_triangles(
        voxels,
        "+Z",
        IDENTITY,
    )

    assert triangles.shape == (6, 3, 3)
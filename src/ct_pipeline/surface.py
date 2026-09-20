"""Conversion of exposed voxel faces into physical-space surface triangles."""

import numpy as np

from ct_pipeline.boundary import BoundaryDirection
from ct_pipeline.coordinates import voxel_to_physical


_FACE_OFFSETS: dict[str, np.ndarray] = {
    "+X": np.array(
        [
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
        ]
    ),
    "-X": np.array(
        [
            [-0.5, -0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [-0.5, 0.5, -0.5],
        ]
    ),
    "+Y": np.array(
        [
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, 0.5, -0.5],
        ]
    ),
    "-Y": np.array(
        [
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, -0.5, 0.5],
            [-0.5, -0.5, 0.5],
        ]
    ),
    "+Z": np.array(
        [
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
        ]
    ),
    "-Z": np.array(
        [
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
        ]
    ),
}


_VOXEL_NORMALS: dict[str, np.ndarray] = {
    "+X": np.array([1.0, 0.0, 0.0]),
    "-X": np.array([-1.0, 0.0, 0.0]),
    "+Y": np.array([0.0, 1.0, 0.0]),
    "-Y": np.array([0.0, -1.0, 0.0]),
    "+Z": np.array([0.0, 0.0, 1.0]),
    "-Z": np.array([0.0, 0.0, -1.0]),
}


def physical_face_normal(
    direction: BoundaryDirection,
    affine: np.ndarray,
) -> np.ndarray:
    """
    Calculate the physical-space normal corresponding to a voxel face.

    Surface normals transform with the inverse transpose of the affine's
    linear component. This remains correct for axis flips, rotations,
    anisotropic spacing, and general invertible linear transforms.
    """
    if direction not in _VOXEL_NORMALS:
        raise ValueError(f"Unsupported direction: {direction}")

    affine = np.asarray(affine, dtype=float)

    if affine.shape != (4, 4):
        raise ValueError("Affine must have shape (4, 4).")

    linear = affine[:3, :3]

    if abs(np.linalg.det(linear)) < 1e-12:
        raise ValueError("Affine linear transform must be invertible.")

    normal = np.linalg.inv(linear).T @ _VOXEL_NORMALS[direction]

    return normal / np.linalg.norm(normal)


def voxel_faces_to_triangles(
    voxel_indices: np.ndarray,
    direction: BoundaryDirection,
    affine: np.ndarray,
) -> np.ndarray:
    """
    Convert exposed voxel faces into physical-space triangles.

    Each exposed square voxel face becomes two triangles.

    Parameters
    ----------
    voxel_indices:
        Array with shape ``(N, 3)`` containing exposed voxel centres.

    direction:
        Exposed face direction.

    affine:
        NIfTI voxel-to-physical transformation matrix.

    Returns
    -------
    numpy.ndarray
        Triangle array with shape ``(2*N, 3, 3)``.
    """
    indices = np.asarray(voxel_indices, dtype=float)

    if indices.size == 0:
        return np.empty((0, 3, 3), dtype=float)

    if indices.ndim != 2 or indices.shape[1] != 3:
        raise ValueError("voxel_indices must have shape (N, 3).")

    if direction not in _FACE_OFFSETS:
        raise ValueError(f"Unsupported direction: {direction}")

    face_corners_voxel = (
        indices[:, np.newaxis, :]
        + _FACE_OFFSETS[direction][np.newaxis, :, :]
    )

    face_corners_physical = voxel_to_physical(
        face_corners_voxel,
        affine,
    )

    first_triangles = face_corners_physical[:, [0, 1, 2], :]
    second_triangles = face_corners_physical[:, [0, 2, 3], :]

    triangles = np.stack(
        [first_triangles, second_triangles],
        axis=1,
    ).reshape(-1, 3, 3)

    target_normal = physical_face_normal(
        direction,
        affine,
    )

    triangle_normals = np.cross(
        triangles[:, 1] - triangles[:, 0],
        triangles[:, 2] - triangles[:, 0],
    )

    magnitudes = np.linalg.norm(
        triangle_normals,
        axis=1,
    )

    if np.any(magnitudes < 1e-12):
        raise ValueError("Degenerate triangle encountered.")

    # A reflection in the affine can reverse triangle winding.
    # Flip any triangle whose normal points inward.
    wrong_orientation = (
        triangle_normals @ target_normal
    ) < 0.0

    triangles[wrong_orientation] = (
        triangles[wrong_orientation][:, [0, 2, 1], :]
    )

    return triangles
"""Validation utilities for exported boundary-surface geometry."""

import numpy as np

from ct_pipeline.boundary import BoundaryDirection
from ct_pipeline.surface import physical_face_normal


def validate_boundary_surface(
    triangles: np.ndarray,
    selected_voxel_count: int,
    direction: BoundaryDirection,
    affine: np.ndarray,
) -> dict:
    """
    Validate geometric consistency of a directional boundary surface.

    Checks include:

    - surface is non-empty
    - triangle count equals two triangles per voxel face
    - all coordinates are finite
    - triangles are non-degenerate
    - triangle normals point in the requested physical direction
    """
    triangles = np.asarray(triangles, dtype=float)

    expected_triangle_count = 2 * selected_voxel_count

    shape_valid = (
        triangles.ndim == 3
        and triangles.shape[1:] == (3, 3)
    )

    if not shape_valid:
        return {
            "valid": False,
            "surface_non_empty": False,
            "triangle_shape_valid": False,
            "triangle_count_matches": False,
            "coordinates_finite": False,
            "triangles_non_degenerate": False,
            "normals_consistent": False,
            "selected_voxel_count": selected_voxel_count,
            "expected_triangle_count": expected_triangle_count,
            "triangle_count": 0,
        }

    triangle_count = len(triangles)

    surface_non_empty = (
        selected_voxel_count > 0
        and triangle_count > 0
    )

    triangle_count_matches = (
        triangle_count
        == expected_triangle_count
    )

    coordinates_finite = bool(
        np.all(np.isfinite(triangles))
    )

    edges_1 = (
        triangles[:, 1]
        - triangles[:, 0]
    )

    edges_2 = (
        triangles[:, 2]
        - triangles[:, 0]
    )

    normals = np.cross(
        edges_1,
        edges_2,
    )

    magnitudes = np.linalg.norm(
        normals,
        axis=1,
    )

    triangles_non_degenerate = bool(
        np.all(magnitudes > 1e-12)
    )

    normals_consistent = False

    if (
        triangle_count > 0
        and triangles_non_degenerate
    ):
        unit_normals = (
            normals
            / magnitudes[:, np.newaxis]
        )

        target_normal = physical_face_normal(
            direction,
            affine,
        )

        alignment = (
            unit_normals
            @ target_normal
        )

        normals_consistent = bool(
            np.all(alignment > 1.0 - 1e-8)
        )

    valid = all(
        (
            surface_non_empty,
            shape_valid,
            triangle_count_matches,
            coordinates_finite,
            triangles_non_degenerate,
            normals_consistent,
        )
    )

    report = {
        "valid": valid,
        "surface_non_empty": surface_non_empty,
        "triangle_shape_valid": shape_valid,
        "triangle_count_matches": triangle_count_matches,
        "coordinates_finite": coordinates_finite,
        "triangles_non_degenerate": triangles_non_degenerate,
        "normals_consistent": normals_consistent,
        "selected_voxel_count": selected_voxel_count,
        "expected_triangle_count": expected_triangle_count,
        "triangle_count": triangle_count,
    }

    if triangle_count > 0:
        report["bounds_minimum"] = (
            triangles.min(axis=(0, 1)).tolist()
        )
        report["bounds_maximum"] = (
            triangles.max(axis=(0, 1)).tolist()
        )

    return report


def require_valid_boundary(
    validation_report: dict,
) -> None:
    """
    Raise an error when a boundary validation report contains failures.
    """
    if validation_report["valid"]:
        return

    failed_checks = [
        key
        for key, value in validation_report.items()
        if isinstance(value, bool)
        and key != "valid"
        and not value
    ]

    raise ValueError(
        "Boundary-surface validation failed: "
        + ", ".join(failed_checks)
    )
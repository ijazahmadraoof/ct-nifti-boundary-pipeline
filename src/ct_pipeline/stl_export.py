"""STL export utilities for simulation boundary surfaces."""

from pathlib import Path

import numpy as np


def triangle_normal(
    triangle: np.ndarray,
) -> np.ndarray:
    """Return the unit normal of a triangle."""
    triangle = np.asarray(triangle, dtype=float)

    if triangle.shape != (3, 3):
        raise ValueError("Triangle must have shape (3, 3).")

    normal = np.cross(
        triangle[1] - triangle[0],
        triangle[2] - triangle[0],
    )

    magnitude = np.linalg.norm(normal)

    if magnitude < 1e-12:
        raise ValueError("Cannot calculate the normal of a degenerate triangle.")

    return normal / magnitude


def write_ascii_stl(
    triangles: np.ndarray,
    output_path: str | Path,
    solid_name: str = "boundary_surface",
) -> Path:
    """
    Write physical-space triangles to an ASCII STL file.
    """
    triangles = np.asarray(triangles, dtype=float)

    if (
        triangles.ndim != 3
        or triangles.shape[1:] != (3, 3)
    ):
        raise ValueError("Triangles must have shape (N, 3, 3).")

    if not np.all(np.isfinite(triangles)):
        raise ValueError("Triangle coordinates must be finite.")

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_name = "_".join(solid_name.split())

    if not safe_name:
        safe_name = "boundary_surface"

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as stl_file:
        stl_file.write(f"solid {safe_name}\n")

        for triangle in triangles:
            normal = triangle_normal(triangle)

            stl_file.write(
                "  facet normal "
                f"{normal[0]:.9e} "
                f"{normal[1]:.9e} "
                f"{normal[2]:.9e}\n"
            )
            stl_file.write("    outer loop\n")

            for vertex in triangle:
                stl_file.write(
                    "      vertex "
                    f"{vertex[0]:.9e} "
                    f"{vertex[1]:.9e} "
                    f"{vertex[2]:.9e}\n"
                )

            stl_file.write("    endloop\n")
            stl_file.write("  endfacet\n")

        stl_file.write(f"endsolid {safe_name}\n")

    return output_path
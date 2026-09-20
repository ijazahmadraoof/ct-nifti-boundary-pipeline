"""Metadata export for simulation boundary-condition surfaces."""

import json
from pathlib import Path

import numpy as np


def build_boundary_metadata(
    *,
    boundary_name: str,
    direction: str,
    threshold_method: str,
    threshold_value: float,
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    z_range: tuple[float, float],
    surface_band_voxels: int | None,
    largest_component: bool,
    connectivity: int,
    selected_voxel_count: int,
    triangles: np.ndarray,
    affine_source: str,
    spatial_units: str,
    orientation: tuple[str, str, str],
    stl_file: str,
) -> dict:
    """
    Build serializable metadata describing a boundary-condition export.
    """
    triangles = np.asarray(
        triangles,
        dtype=float,
    )

    geometry: dict = {
        "selected_voxels": int(
            selected_voxel_count
        ),
        "triangle_count": int(
            len(triangles)
        ),
    }

    if len(triangles) > 0:
        geometry["bounds"] = {
            "minimum": (
                triangles
                .min(axis=(0, 1))
                .tolist()
            ),
            "maximum": (
                triangles
                .max(axis=(0, 1))
                .tolist()
            ),
        }

    return {
        "boundary_name": boundary_name,
        "direction": direction,
        "stl_file": stl_file,
        "segmentation": {
            "method": threshold_method,
            "threshold": float(
                threshold_value
            ),
        },
        "selection": {
            "x_range": list(x_range),
            "y_range": list(y_range),
            "z_range": list(z_range),
            "surface_band_voxels": (
                surface_band_voxels
            ),
            "largest_component": bool(
                largest_component
            ),
            "connectivity": int(
                connectivity
            ),
        },
        "geometry": geometry,
        "spatial_metadata": {
            "affine_source": affine_source,
            "units": spatial_units,
            "orientation": list(
                orientation
            ),
        },
    }


def write_metadata_json(
    metadata: dict,
    output_path: str | Path,
) -> Path:
    """
    Write boundary-condition metadata as formatted JSON.
    """
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as json_file:
        json.dump(
            metadata,
            json_file,
            indent=2,
        )

        json_file.write("\n")

    return output_path
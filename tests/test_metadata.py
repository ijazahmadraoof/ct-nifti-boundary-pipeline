import json

import numpy as np

from ct_pipeline.metadata import (
    build_boundary_metadata,
    write_metadata_json,
)


def test_boundary_metadata_and_json_export(
    tmp_path,
) -> None:
    triangles = np.array(
        [
            [
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
            ],
            [
                [0.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 1.0],
            ],
        ]
    )

    metadata = build_boundary_metadata(
        boundary_name="top_load",
        direction="+Z",
        threshold_method="otsu",
        threshold_value=15.5,
        x_range=(0.25, 0.75),
        y_range=(0.25, 0.75),
        z_range=(0.75, 1.0),
        surface_band_voxels=1,
        largest_component=True,
        connectivity=1,
        selected_voxel_count=1,
        triangles=triangles,
        affine_source="sform",
        spatial_units="mm",
        orientation=("R", "A", "S"),
        stl_file="top_load.stl",
    )

    output_path = (
        tmp_path
        / "top_load.json"
    )

    write_metadata_json(
        metadata,
        output_path,
    )

    loaded = json.loads(
        output_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        loaded["boundary_name"]
        == "top_load"
    )

    assert (
        loaded["geometry"][
            "triangle_count"
        ]
        == 2
    )

    assert (
        loaded["spatial_metadata"][
            "units"
        ]
        == "mm"
    )

    assert loaded["geometry"]["bounds"][
        "maximum"
    ] == [1.0, 1.0, 1.0]
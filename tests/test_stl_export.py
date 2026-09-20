import numpy as np

from ct_pipeline.stl_export import write_ascii_stl


def test_write_ascii_stl(tmp_path) -> None:
    triangles = np.array(
        [
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
            ],
        ]
    )

    output_path = tmp_path / "surface.stl"

    write_ascii_stl(
        triangles,
        output_path,
        solid_name="test_surface",
    )

    text = output_path.read_text(
        encoding="utf-8"
    )

    assert text.startswith("solid test_surface")
    assert text.count("facet normal") == 2
    assert text.strip().endswith(
        "endsolid test_surface"
    )
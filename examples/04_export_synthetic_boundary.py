"""Extract and export a directional boundary from the synthetic specimen."""

from pathlib import Path

from ct_pipeline.boundary import exposed_voxel_indices
from ct_pipeline.segmentation import threshold_material
from ct_pipeline.stl_export import write_ascii_stl
from ct_pipeline.surface import voxel_faces_to_triangles
from ct_pipeline.synthetic import (
    create_affine,
    create_t_shape_volume,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = create_t_shape_volume()

    affine = create_affine(
        voxel_spacing=(0.25, 0.25, 0.50),
        origin=(10.0, 20.0, 30.0),
    )

    material_mask = threshold_material(
        data,
        threshold=0.5,
    )

    direction = "+Z"

    exposed_voxels = exposed_voxel_indices(
        material_mask,
        direction,
    )

    triangles = voxel_faces_to_triangles(
        exposed_voxels,
        direction,
        affine,
    )

    output_path = (
        PROJECT_ROOT
        / "results"
        / "synthetic_boundary"
        / "boundary_plus_z.stl"
    )

    write_ascii_stl(
        triangles,
        output_path,
        solid_name="synthetic_plus_z_boundary",
    )

    print("\nSynthetic boundary export")
    print("=" * 50)
    print(f"Direction:         {direction}")
    print(f"Exposed voxels:    {len(exposed_voxels)}")
    print(f"STL triangles:     {len(triangles)}")
    print(f"Expected triangles:{2 * len(exposed_voxels)}")

    if len(triangles) > 0:
        print("\nPhysical surface bounds")
        print(f"Minimum: {triangles.min(axis=(0, 1))}")
        print(f"Maximum: {triangles.max(axis=(0, 1))}")

    print(f"\nSTL written to:\n{output_path}")


if __name__ == "__main__":
    main()
"""Create and inspect a reproducible synthetic NIfTI specimen."""

from pathlib import Path

from ct_pipeline.io import inspect_nifti
from ct_pipeline.synthetic import save_synthetic_nifti


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    output_path = (
        PROJECT_ROOT
        / "results"
        / "synthetic_demo"
        / "synthetic_t_shape.nii.gz"
    )

    saved_path = save_synthetic_nifti(output_path)

    print(f"\nSynthetic specimen written to:\n{saved_path}")

    info = inspect_nifti(saved_path)

    print("\nSynthetic NIfTI Inspection")
    print("=" * 50)

    print(f"Shape:           {info['shape']}")
    print(f"Voxel spacing:   {info['voxel_spacing']}")
    print(f"Physical size:   {info['physical_size']}")
    print(f"Spatial units:   {info['spatial_units']}")
    print(f"Orientation:     {info['orientation']}")
    print(f"Affine source:   {info['affine_source']}")
    print(f"qform code:      {info['qform_code']}")
    print(f"sform code:      {info['sform_code']}")

    print("\nAffine matrix:")
    print(info["affine"])


if __name__ == "__main__":
    main()
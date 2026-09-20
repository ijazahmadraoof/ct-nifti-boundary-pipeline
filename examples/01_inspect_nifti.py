"""Inspect the metadata and voxel information of a NIfTI volume."""

from pathlib import Path

from ct_pipeline.io import inspect_nifti

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    nifti_path = PROJECT_ROOT / "local_data" / "cube_split_01.nii"

    info = inspect_nifti(nifti_path)

    print("\nCT-NIfTI Volume Inspection")
    print("=" * 50)

    print(f"File:            {nifti_path.name}")
    print(f"Shape:           {info['shape']}")
    print(f"Data type:       {info['dtype']}")
    print(f"Voxel spacing:   {info['voxel_spacing']}")
    print(f"Physical size:   {info['physical_size']}")
    print(f"Spatial units:   {info['spatial_units']}")
    print(f"Orientation:     {info['orientation']}")

    print("\nIntensity statistics")
    print("-" * 50)
    print(f"Minimum:         {info['intensity_min']:.6f}")
    print(f"Maximum:         {info['intensity_max']:.6f}")
    print(f"Mean:            {info['intensity_mean']:.6f}")

    print("\nSpatial transform")
    print("-" * 50)
    print(f"Affine source:   {info['affine_source']}")
    print(f"qform code:      {info['qform_code']}")
    print(f"sform code:      {info['sform_code']}")

    print("\nAffine matrix:")
    print(info["affine"])


if __name__ == "__main__":
    main()
# ILDM Reconstruction Datasets

This repository provides the data package used to study hard-constrained reconstruction of discontinuous compressible flow fields from low-fidelity observations.

## Included datasets

| Original file | Physical case | Stored format |
| --- | --- | --- |
| `near_wall_cavitation.mat` | Near-wall cavitation-bubble collapse | MATLAB v7.3/HDF5 |
| `riemann2d_1000.mat` | Two-dimensional Riemann problem | MATLAB MAT-file |
| `double_mach_revise.mat` | Double Mach reflection, 900 retained frames | MATLAB MAT-file |

The binary datasets are distributed as assets of the `v1.0.0` GitHub Release. Each MAT file is losslessly gzip-compressed and, when needed, split into ordered parts or smaller transfer segments. The exact original and compressed sizes, reconstruction order, and SHA-256 checksums are recorded in `dataset_manifest.json` and `SHA256SUMS`.

## Download and reconstruct

Download every release asset into one directory:

```bash
gh release download v1.0.0 \
  --repo liuqiang686/ILDM-Reconstruction-Datasets \
  --dir release_assets
```

Join the parts, decompress the streams, and verify the original MAT files:

```bash
python reassemble_dataset.py \
  --assets-dir release_assets \
  --output-dir datasets
```

Use `--force` only when an existing reconstructed file should be replaced. The script validates each downloaded part before joining it, verifies the complete gzip stream, and validates the decompressed output against the original-file SHA-256 checksum. It requires only the Python standard library.

## Integrity metadata

- `dataset_manifest.json`: original filenames, byte sizes, checksums, physical-case metadata, and ordered release assets.
- `SHA256SUMS`: checksums of all downloadable release assets.
- `reassemble_dataset.py`: cross-platform reconstruction and integrity-checking utility.

The source MAT files are not committed to Git history.

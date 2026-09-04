# ILDM Reconstruction Datasets v1.0.0

This release contains three MAT datasets for reconstructing discontinuous compressible flow fields from low-fidelity observations:

- near-wall cavitation-bubble collapse;
- a two-dimensional Riemann problem;
- double Mach reflection with 900 retained time frames.

The MAT files are losslessly gzip-compressed, with large streams provided as ordered `.part.###` assets. Download all assets and run `reassemble_dataset.py` from the repository to recover and verify the original MAT files. Exact SHA-256 checksums are provided in `dataset_manifest.json` and `SHA256SUMS`.

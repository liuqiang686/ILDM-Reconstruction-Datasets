#!/usr/bin/env python3
"""Reassemble and verify MAT datasets downloaded from the GitHub Release."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


BUFFER_SIZE = 16 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(BUFFER_SIZE):
            digest.update(block)
    return digest.hexdigest()


def verify(path: Path, expected_size: int, expected_sha256: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing release asset: {path}")
    actual_size = path.stat().st_size
    if actual_size != expected_size:
        raise ValueError(
            f"Size mismatch for {path.name}: expected {expected_size}, got {actual_size}"
        )
    actual_sha256 = sha256_file(path)
    if actual_sha256.lower() != expected_sha256.lower():
        raise ValueError(
            f"SHA-256 mismatch for {path.name}: expected {expected_sha256}, "
            f"got {actual_sha256}"
        )


def reconstruct_dataset(
    dataset: dict, assets_dir: Path, output_dir: Path, force: bool
) -> Path:
    parts = dataset["parts"]
    output_path = output_dir / dataset["original_name"]
    resolved_output = output_path.resolve()

    for part in parts:
        verify(
            assets_dir / part["name"],
            int(part["bytes"]),
            part["sha256"],
        )

    if output_path.exists() and not force:
        raise FileExistsError(
            f"Output already exists: {output_path}. Use --force to replace it."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    direct_asset = len(parts) == 1 and parts[0]["name"] == dataset["original_name"]
    direct_path = (assets_dir / parts[0]["name"]).resolve() if direct_asset else None

    if direct_asset and direct_path == resolved_output:
        result = output_path
    elif direct_asset:
        shutil.copyfile(direct_path, output_path)
        result = output_path
    else:
        temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
        if temporary_path.exists():
            temporary_path.unlink()
        try:
            with temporary_path.open("wb") as target:
                for part in parts:
                    with (assets_dir / part["name"]).open("rb") as source:
                        shutil.copyfileobj(source, target, length=BUFFER_SIZE)
            temporary_path.replace(output_path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise
        result = output_path

    verify(result, int(dataset["original_bytes"]), dataset["original_sha256"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reassemble and validate the ILDM Reconstruction Datasets release."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).with_name("dataset_manifest.json"),
    )
    parser.add_argument("--assets-dir", type=Path, default=Path("release_assets"))
    parser.add_argument("--output-dir", type=Path, default=Path("reconstructed"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    for dataset in manifest["datasets"]:
        result = reconstruct_dataset(
            dataset, args.assets_dir, args.output_dir, args.force
        )
        print(f"Verified: {result}")


if __name__ == "__main__":
    main()

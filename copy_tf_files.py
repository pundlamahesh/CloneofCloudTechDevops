#!/usr/bin/env python3
"""
Copy Terraform .tf files from one directory to another.

Usage:
    python copy_tf_files.py SOURCE_DIR DEST_DIR
    python copy_tf_files.py SOURCE_DIR DEST_DIR --recursive
    python copy_tf_files.py SOURCE_DIR DEST_DIR --recursive --overwrite
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_tf_files(source: Path, destination: Path, recursive: bool, overwrite: bool) -> int:
    if not source.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source}")

    destination.mkdir(parents=True, exist_ok=True)

    pattern = "**/*.tf" if recursive else "*.tf"
    copied_count = 0

    for tf_file in source.glob(pattern):
        if not tf_file.is_file():
            continue

        relative_path = tf_file.relative_to(source)
        target_file = destination / relative_path
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if target_file.exists() and not overwrite:
            print(f"Skipped existing file: {target_file}")
            continue

        shutil.copy2(tf_file, target_file)
        print(f"Copied: {tf_file} -> {target_file}")
        copied_count += 1

    return copied_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy .tf files between folders.")
    parser.add_argument("source", type=Path, help="Folder to copy .tf files from")
    parser.add_argument("destination", type=Path, help="Folder to copy .tf files into")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Copy .tf files from subfolders too",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Replace files that already exist in the destination",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    copied_count = copy_tf_files(
        source=args.source,
        destination=args.destination,
        recursive=args.recursive,
        overwrite=args.overwrite,
    )
    print(f"Done. Copied {copied_count} .tf file(s).")


if __name__ == "__main__":
    main()

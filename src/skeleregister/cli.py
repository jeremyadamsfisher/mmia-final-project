import argparse
from pathlib import Path

def cli() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("."))
    parser.add_argument("images", nargs="*", type=Path)
    return parser.parse_args().__dict__

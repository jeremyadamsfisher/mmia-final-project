import argparse
from pathlib import Path

def cli() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("."),
        help="Where to save the analysis"
    )
    parser.add_argument(
        "image_args",
        nargs="*",
        type=Path,
        help="Specify a single directory or multiple images"
    )
    opts = parser.parse_args().__dict__
    img_args = opts.pop("image_args")
    if (len(img_args) == 1
        and img_args[0].is_dir()):
        opts["radiograph_fps"] = list(img_args[0].glob("*.jpg"))
    else:  # list of images
        opts["radiograph_fps"] = img_args
    n_radiographs = len(opts["radiograph_fps"])
    if n_radiographs == 0:
        parser.error("No radiographs found!")
    return opts

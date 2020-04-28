import re
import json
import random
from tqdm import tqdm
import importlib.resources as ilr

import prototypical_appendages
from .register import register, load_and_preprocess_img
from .cli import cli
from .visualization import comparison, save_img


def register_radiographs(radiograph_fps, outdir):
    """register radiographs requested from the command line

    Arguments:
        {l,r}{h,f}_fp: file path of the radiograph to register against
        radiograph_fps: list of ragiographs to register
        outdir: where to output the per-radiograph analysis
    """
    visual_inspection_dir = outdir/"comparison"
    registration_result_dir = outdir/"registered"
    analysis_out_fp = outdir/"registration_results.json"
    for dir in [visual_inspection_dir, registration_result_dir]:
        dir.mkdir(exist_ok=True)
    visual_inspection_dir.mkdir(exist_ok=True)
    prototypical = {}
    for appendage, f_name in [("LF", "UAB007-LF.jpg"),
                              ("RF", "UAB006-RF.jpg"),
                              ("LH", "UAB012-LH.jpg"),
                              ("RH", "UAB013-RH.jpg")]:
        with ilr.path(prototypical_appendages, f_name) as template_fp:
            prototypical[appendage], *_ = load_and_preprocess_img(template_fp)
    results = []
    for radiograph_fp in tqdm(radiograph_fps, unit="radiographs"):
        match = re.search(r"-([L|R][H|F]).jpg$", radiograph_fp.name)
        try:
            appendage, = match.groups()
        except AttributeError:
            raise ValueError(f"filename `{radiograph_fp.name}` does not seem"
                             f"to be formatted correctly!")
        while True:
            try:
                radiograph_original, radiograph_registered, rotation, \
                    padding_left, padding_top, transform_quality \
                    = register(radiograph_fp, prototypical[appendage], n_registrations=1)
            except RuntimeError:
                pass  # fail-safe against mutual information bug
            else:
                break
        save_img(radiograph_registered, str(registration_result_dir/radiograph_fp.name))
        comparison(
            radiograph_original,
            radiograph_registered,
            title=f"{rotation:.2f} rads, {max((padding_left, padding_top))*2} pixels padding",
            outfp=visual_inspection_dir/(radiograph_fp.stem + "_comparison.png"),
        )
        results.append({
            "appendage": appendage,
            "fname": radiograph_fp.name,
            "rotation": rotation,
            "padding_top": padding_top,
            "padding_left": padding_left,
            "transform_quality": transform_quality,
        })

    with analysis_out_fp.open("wt") as f:
        json.dump(results, f)


def main():
    """cli ingress"""
    register_radiographs(**cli())
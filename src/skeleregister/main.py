import re
from tqdm import tqdm
import importlib.resources as ilr

import prototypical_appendages
from .register import register
from .cli import cli
from .image_processing import load_img
from .visualization import compare


def register_radiographs(radiograph_fps, outdir):
    """register radiographs requested from the command line

    Arguments:
        {l,r}{h,f}_fp: file path of the radiograph to register against
        radiograph_fps: list of ragiographs to register
        outdir: where to output the per-radiograph analysis
    """
    prototypical = {}
    for appendage, f_name in [("LF", "UAB007-LF.jpg"),
                              ("RF", "UAB006-RF.jpg"),
                              ("LH", "UAB012-LH.jpg"),
                              ("RH", "UAB013-RH.jpg")]:
        with ilr.path(templates, f_name) as template_fp:
            prototypical[appendage] = load_img(template_fp)

    for radiograph_fp in tqdm(radiograph_fps, unit="radiographs"):
        match = re.search(r"-([L|R][H|F]).jpg$", radiograph_fp.name)
        try:
            appendage, = match.groups()
        except AttributeError:
            raise ValueError(f"filename `{radiograph_fp.name}` does not seem to be formatted correctly!")
        radiograph_original = load_img(radiograph_fp)
        radiograph_registered = register(radiograph_original,
                                         prototypical[appendage],
                                         n_registrations=1)
        compare(prototypical[appendage],
                radiograph_original,
                radiograph_registered,
                outfp=outdir/(radiograph_fp.stem+"_registered.jpg"))


def main():
    """cli ingress"""
    register_radiographs(**cli())
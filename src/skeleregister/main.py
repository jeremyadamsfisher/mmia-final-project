import re
from tqdm import tqdm

from .register import register
from .cli import cli
from .image_processing import load_img
from .visualization import compare

def main(lf_fp, rf_fp, lh_fp, rh_fp, images, outdir):
    """register radiographs requested from the command line

    Arguments:
        {l,r}{h,f}_fp: file path of the radiograph to register against
        images: list of ragiographs to register
        outdir: where to output the per-radiograph analysis
    """
    prototypical = {"LF": load_img("UAB007-LF.jpg"),
                    "RF": load_img("UAB006-RF.jpg"),
                    "LH": load_img("UAB012-LH.jpg"),
                    "RH": load_img("UAB013-RH.jpg")}

    for radiograph_fp in tqdm(images, unit="radiographs"):
        appendage, = re.search(r"^.{3}\d{3}-([L|F][H|F]).jpg$", radiograph_fp).groups()
        assert appendage in {"LF", "RF", "LH", "RH"}
        prototype = prototypical[appendage]
        radiograph_original = load_img(radiograph_fp)
        radiograph_registered = register(radiograph_original, prototype, n_registrations=1)
        compare(prototype, radiograph_original,
                radiograph_registered,
                outfp=outdir/(radiograph_fp.stem+"_registered.jpg"))


if __name__ == "__main__":
    main(**cli())
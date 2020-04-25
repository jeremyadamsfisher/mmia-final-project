import typing as t
import SimpleITK as sitk
import matplotlib.pyplot as plt
from tqdm import tqdm
from skimage import io, color, util, transform
from pathlib import Path

# type aliases
Pathlike = t.Union[str, Path]

# constants
IM_SIZE = (1024, 1024)
IMG_DATA_DIR = Path("/Users/jeremyfisher/ra2challenge/data/raw/images")


def load_img(fp: Pathlike) -> sitk.Image:
    """load the radiograph into memory and resize to a square
    to be amenable to downstream registration and learning and stuff"""
    im = io.imread(fp)
    im = color.rgb2gray(im)
    width, height = im.shape
    if height < width:
        padding = (width - height) // 2
        im = util.pad(im, padding, mode="edge")
        im = im[padding:padding+width,:]
    im = transform.resize(im, IM_SIZE, anti_aliasing=True)
    return sitk.GetImageFromArray(im)


def threshold(radiograph: sitk.Image) -> sitk.Image:
    """threshold (adaptively) to seperate skeleton from flesh
    and background -- this improves registration""" 
    otsu_filter = sitk.OtsuThresholdImageFilter()
    otsu_filter.SetInsideValue(0)
    otsu_filter.SetOutsideValue(1)
    seg = otsu_filter.Execute(radiograph)
    seg = sitk.BinaryDilate(seg, 25)
    seg = sitk.BinaryErode(seg, 10)
    return seg


# define registration using SimpleITKs OOP interface
r = sitk.ImageRegistrationMethod()
r.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)        
r.SetMetricSamplingStrategy(r.RANDOM)
r.SetMetricSamplingPercentage(0.1)
r.SetInterpolator(sitk.sitkLinear)
r.SetOptimizerAsGradientDescent(learningRate=0.25, numberOfIterations=250) 
r.SetOptimizerScalesFromPhysicalShift() 
r.SetShrinkFactorsPerLevel(shrinkFactors=[4,2,1])
r.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
r.SmoothingSigmasAreSpecifiedInPhysicalUnitsOff()


def register(radiograph: sitk.Image,
             prototypical_radiograph: sitk.Image,
             n_registrations=3) -> sitk.Image:
    fixed_image = sitk.Cast(sitk.RescaleIntensity(threshold(prototypical_radiograph)), sitk.sitkFloat32)
    moving_image = sitk.Cast(sitk.RescaleIntensity(threshold(radiograph)), sitk.sitkFloat32)
    initial_transform = sitk.CenteredTransformInitializer(
        fixed_image, 
        moving_image, 
        sitk.Euler2DTransform(), 
        sitk.CenteredTransformInitializerFilter.GEOMETRY
    )
    r.SetInitialTransform(initial_transform, inPlace=False)
    registrations = []
    for _ in range(n_registrations):
        transform = r.Execute(fixed_image, moving_image)
        quality = r.GetMetricValue()
        registrations.append((transform, quality))
    final_transform, _ = min(registrations, key=lambda x: x[1])
    radiograph_registered = sitk.Resample(
        radiograph,
        prototypical_radiograph,
        transform,
        sitk.sitkLinear,
        0.0,
        radiograph.GetPixelID()
    )
    return radiograph_registered


def main():
    for appendage, prototype_fname in [("LF", "UAB007-LF.jpg"),
                                       ("RF", "UAB006-RF.jpg"),
                                       ("LH", "UAB012-LH.jpg"),
                                       ("RH", "UAB013-RH.jpg")]:
        prototype = load_img(IMG_DATA_DIR/prototype_fname)
        radiograph_fps = list(IMG_DATA_DIR.glob(f"*-{appendage}.jpg"))
        for radiograph_fp in tqdm(radiograph_fps, unit=appendage):
            radiograph_original = load_img(radiograph_fp)
            radiograph_registered = register(radiograph_original, prototype, n_registrations=1)
            fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15,5))
            ax1.imshow(sitk.GetArrayFromImage(radiograph_registered))
            ax2.imshow((0.5*sitk.GetArrayFromImage(prototype))+(0.5*sitk.GetArrayFromImage(radiograph_registered)))
            ax3.imshow(sitk.GetArrayFromImage(radiograph_original))
            fig.savefig(Path("./out")/(radiograph_fp.stem + "_registered.jpg"))
            plt.close()

if __name__ == "__main__":
    main()
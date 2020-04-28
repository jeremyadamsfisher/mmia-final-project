import typing as t
import SimpleITK as sitk
from skimage import io, color, util, transform


# define registration using SimpleITKs OOP interface
r = sitk.ImageRegistrationMethod()
r.SetMetricAsMattesMutualInformation(numberOfHistogramBins=150)
r.SetMetricSamplingStrategy(r.RANDOM)
r.SetMetricSamplingPercentage(0.125)
r.SetInterpolator(sitk.sitkLinear)
r.SetOptimizerAsGradientDescent(learningRate=0.25, numberOfIterations=250)
r.SetOptimizerScalesFromPhysicalShift()
r.SetShrinkFactorsPerLevel(shrinkFactors=[8,2,1])
r.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
r.SmoothingSigmasAreSpecifiedInPhysicalUnitsOff()


def load_and_preprocess_img(fp, im_size=(1024, 1024)) -> t.Tuple[sitk.Image, int, str]:
    """load the radiograph into memory and resize to a square
    to be amenable to downstream registration and learning and stuff"""
    im_orig = io.imread(fp)
    im = color.rgb2gray(im_orig)
    width, height = im.shape

    padding_left = padding_top = 0
    if width != height:
        padding = abs(width - height) // 2
        im = util.pad(im,  padding, mode="edge")  # pad in all directions...
        if width < height:
            padding_left = padding
            im = im[:, padding:height+padding]  # ...then crop
        else:
            padding_top = padding
            im = im[padding:width+padding, :]
    im = transform.resize(im, im_size, anti_aliasing=True)
    return sitk.GetImageFromArray(im), im_orig, padding_left, padding_top


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


def register(radiograph_fp,
             prototypical_radiograph: sitk.Image,
             n_registrations=3):

    radiograph, radiograph_orig, padding_left, padding_top = \
        load_and_preprocess_img(radiograph_fp)

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
        transforme_proposed = r.Execute(fixed_image, moving_image)
        quality = r.GetMetricValue()
        registrations.append((transforme_proposed, quality))
    transform_final, transform_quality = min(registrations, key=lambda x: x[1])
    rotation, *_ = transform_final.GetParameters()
    transform_final.SetParameters((rotation, 0, 0))  # discard translation
    radiograph_registered = sitk.Resample(
        radiograph,
        prototypical_radiograph,
        transform_final,
        sitk.sitkLinear,
        0.0,
        radiograph.GetPixelID()
    )
    return (radiograph_orig, radiograph_registered, rotation,
            padding_left, padding_top, transform_quality)

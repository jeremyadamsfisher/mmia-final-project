import SimpleITK as sitk

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
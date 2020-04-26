import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
from skimage import io

def save_img(radiograph, outfp):
    radiograph = sitk.Cast(sitk.RescaleIntensity(radiograph), sitk.sitkUInt8)
    io.imsave(outfp, sitk.GetArrayFromImage(radiograph))


def comparison(radiograph_original: np.ndarray,
               radiograph_registered: sitk.Image,
               outfp,
               title):
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 5))
    ax0.imshow(radiograph_original, cmap="Greys_r")
    ax0.set(title="Original")
    ax1.imshow(sitk.GetArrayFromImage(radiograph_registered), cmap="Greys_r")
    ax1.set(title=f"Registered/Resampled ({title})")
    plt.savefig(outfp)
    plt.close()
import SimpleITK as sitk
from skimage import io, color, util, transform


def load_img(fp, im_size=(1024, 1024)) -> sitk.Image:
    """load the radiograph into memory and resize to a square
    to be amenable to downstream registration and learning and stuff"""
    im = io.imread(fp)
    im = color.rgb2gray(im)
    width, height = im.shape
    if height < width:
        padding = (width - height) // 2
        im = util.pad(im, padding, mode="edge")
        im = im[padding:padding+width,:]
    im = transform.resize(im, im_size, anti_aliasing=True)
    return sitk.GetImageFromArray(im)


sitk2numpy = sitk.GetArrayFromImage
import matplotlib.pyplot as plt

from .image_processing import sitk2numpy

def compare(prototype, radiograph_original, radiograph_registered, outfp):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    ax1.imshow(sitk2numpy(radiograph_registered))
    ax2.imshow((0.5 * sitk2numpy(prototype)) + (0.5 * sitk2numpy(radiograph_registered)))
    ax3.imshow(sitk2numpy(radiograph_original))
    fig.savefig(outfp)
    plt.close()
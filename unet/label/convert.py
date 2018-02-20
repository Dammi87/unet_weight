"""Convert image to a weight image and save in folder.

The saved weight image will be normalized with a factor w0 + 1
This means, that a white pixel of value 255 is in reality a weight
of w0 + 1. So, if the converted image is to be converted to the orginal
weight value again, the following formula applies:

    weights = (w0 + 1) * loaded_img_array / 255

Parameters
----------
image_path : str
    Full path to mask image
output_folder : str
    Output folder location
w0=10.0: float, optional
    Maximum weight of the kernel
sigma=5.0 : float, optional
    Decay rate of the kernel
"""
import argparse
import numpy as np
import os
from PIL import Image


def load_da_image(path):
    if "gs://" in path:
        print("Hello")
        print(path)
        file_name = os.path.basename(path)
        os.system('gsutil cp %s .' % path)
        print(os.popen('ll').read())
        return Image.open(file_name)
    else:
        return Image.open(path)


def save_image(save_path, array):
    img = Image.fromarray(array)

    if "gs://" in save_path:
        file_name = os.path.basename(save_path)
        img.save(file_name)
        os.system('gsutil cp %s %s' % (file_name, save_path))
        print("Saved at %s" % save_path)
    else:
        img.save(save_path)

# from unet.label.common import get_weight_array


def mask_to_weight(mask_path, output_folder, w0=10.0, sigma=5.0):
    # Get weights
    weights = np.array(load_da_image(mask_path))

    # Theoretical maximum weight
    w_max = w0 + 1

    # Normalize to 255
    weights = np.divide(255 * weights, w_max).astype(np.uint8)
    file_name = os.path.basename(mask_path).split('.')[0]
    save_path = os.path.join(output_folder, "%s.png" % file_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    save_image(save_path, weights)

    return save_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--mask_path', help='Path to the mask to convert',
                        required=True)
    parser.add_argument('-o', '--output_folder', help='Folder to save image to',
                        required=True)
    parser.add_argument('--w0', help='Kernel weight', type=float,
                        default=10.0)
    parser.add_argument('--sigma', help='Kernel decay rate',
                        type=float, default=5.0)

    args = parser.parse_args()

    mask_to_weight(args.mask_path, args.output_folder, args.w0, args.sigma)

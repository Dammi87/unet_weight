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

from .common import get_weight_array


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--image_path', help='Path to the image to convert',
                        required=True)
    parser.add_argument('-o', '--output_folder', help='Folder to save image to',
                        required=True)
    parser.add_argument('--w0', help='Kernel weight', type=float,
                        default=10.0)
    parser.add_argument('--sigma', help='Kernel decay rate',
                        type=float, default=5.0)

    args = parser.parse_args()

    # Get weights
    weights = get_weight_array(args.image_path, w0=args.w0, sigma=args.sigma)

    # Theoretical maximum weight
    w_max = args.w0 + 1

    # Normalize to 255
    weights = np.divide(255 * weights, w_max).astype(np.uint8)
    file_name = os.path.basename(args.image_path).split('.')[0]
    save_path = os.path.join(args.output_folder, "%s.png" % file_name)

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    img = Image.fromarray(weights)
    img.save(save_path)

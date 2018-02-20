"""Convert folder of label images to a weight image and save output.

This script is run as a spark job.

The saved weight image will be normalized with a factor w0 + 1
This means, that a white pixel of value 255 is in reality a weight
of w0 + 1. So, if the converted image is to be converted to the orginal
weight value again, the following formula applies:

    weights = (w0 + 1) * loaded_img_array / 255

Parameters
----------
image_folder : str
    Full path to mask folder
output_folder : str
    Output folder location
w0=10.0: float, optional
    Maximum weight of the kernel
sigma=5.0 : float, optional
    Decay rate of the kernel
"""
import os
import pyspark
import argparse
from subprocess import call

from unet.common import listdir
from unet.label.convert import mask_to_weight

# Wrap the function into a function that accepts one input
def mask_to_weight_spark(input_image):
    return mask_to_weight(input_image, output_folder, w0, sigma)


if __name__ == "__main__":
    # [START pyspark]
    image_folder = 'gs://datasets-simone/labels'
    output_folder = 'gs://datasets-simone/weights'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    w0 = 10
    sigma = 100

    sc = pyspark.SparkContext()
    image_paths = sc.parallelize(listdir(image_folder))
    image_paths = image_paths.map(mask_to_weight_spark)
    image_path_done = image_paths.collect()
    # [END pyspark]

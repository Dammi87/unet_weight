from io import BytesIO
from PIL import Image
import numpy as np
import pyspark

def load_image_as_array(binary_file):
    im = np.array(Image.open(BytesIO(binary_file[1])))
    return im


if __name__ == "__main__":
    # [START pyspark]
    sc = pyspark.SparkContext()
    binary_files = sc.binaryFiles("gs://datasets-simone/labels")
    image_array = binary_files.map(load_image_as_array)
    image_array.saveAsPickleFile("gs://datasets-simone/label_pickles")
    # [END pyspark]

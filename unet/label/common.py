import numpy as np
import scipy.ndimage as ndimage
import cv2


def get_weight_array(image_path, w0=10.0, sigma=8.0):
    """Given a path to an bw cell image, create the weighted image for said image.

    The method is the same as described in this paper for the weighted image:
    https://arxiv.org/pdf/1505.04597.pdf

    Parameters
    ----------
    image_path : str
        Path to the black and white image
    w0 : float, optional
        The maximum weight to give the kernel, this means the theoretical maximum
        weight for a pixel will become w0 + 1
    sigma : float, optional
        The decay rate of the kernel

    Returns
    -------
    array
        (W, H) array, with maximum peak at w0 + 1
    """

    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

    # Calculate the contours
    img_empty = 255 * np.ones(img.shape, dtype=np.uint8)
    _, contours, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw them onto the rgb image
    all_contours_together = cv2.drawContours(img_empty.copy(), contours, -1, (0, 0), -1)

    # Create an empty container to fill in
    distance_map = np.zeros(list(img.shape) + [len(contours)])

    # Loop through all contours
    for i, i_contour in enumerate(contours):
        this_contour = cv2.drawContours(img_empty.copy(), [i_contour], -1, (0, 0), -1)
        edt = ndimage.distance_transform_edt(this_contour == 255)
        distance_map[:, :, i] = edt

    # distance_map = np.stack(collected_edt, -1)
    largest_distance = distance_map.max() + 1

    # Anywhere where there is zero, we set to the largest number
    distance_map[distance_map == 0] = largest_distance

    # Calculate closest and next closest cell to all pixels
    col_idx, row_idx = [
        val.transpose() for val in np.meshgrid(*[np.arange(dim) for dim in img.shape])
    ]

    cell_idx = np.argmin(distance_map, -1)
    d1_val = distance_map[col_idx, row_idx, cell_idx]
    distance_map[col_idx, row_idx, cell_idx] = largest_distance + 1
    d2_val = np.min(distance_map, -1)

    # Class weights
    n_total_pixels = img.shape[0] * img.shape[1]
    n_background_pixels = np.sum(all_contours_together != 0)
    n_cell_pixels = n_total_pixels - n_background_pixels
    bg_ratio = 1 - float(n_cell_pixels) / n_total_pixels
    cell_ratio = 1 - bg_ratio

    # Make sure the ratios down "explode" if there are only few cells in image
    ratios = np.array([bg_ratio / cell_ratio, 1.0])
    ratios = np.divide(ratios, ratios.max())

    class_weights = np.ones(img.shape, dtype=np.float32)
    class_weights[all_contours_together == 0] = ratios[0]
    class_weights[all_contours_together == 255] = ratios[1]

    # Exponential distance weights
    weights = w0 * np.exp(-np.divide(np.power(d1_val + d2_val, 2), 2 * sigma**2))

    # Make sure insides of cells are still 0
    weights[all_contours_together == 0] = 0

    return weights + class_weights

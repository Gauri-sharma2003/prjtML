# -*- coding: utf-8 -*-
"""cellcountingedited.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qaZUGAnm4oCEYQHmPibCTw82JD2b2hY2
"""

from google.colab.patches import cv2_imshow
import cv2
import numpy as np

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising using Non-Local Means Denoising
    denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(denoised)

    return equalized

def adaptive_threshold_image(image, block_size=11, C=2):
    # Adaptive thresholding with Gaussian Mean
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
    return thresh

def post_process_image(image):
    # Connected component analysis (connected components labeling)
    num_labels, labeled_image = cv2.connectedComponents(image)

    # Keep only the connected components (regions) larger than a threshold area (e.g., 100 pixels)
    min_area_threshold = 100
    cleaned_image = np.zeros_like(image)
    for label in range(1, num_labels):  # Skip background label (0)
        region_mask = (labeled_image == label).astype(np.uint8)
        region_area = np.sum(region_mask)
        if region_area >= min_area_threshold:
            cleaned_image += region_mask * label

    # Apply binary thresholding to get final binary image
    _, final_image = cv2.threshold(cleaned_image, 0, 255, cv2.THRESH_BINARY)

    return final_image

def count_cells(image):
    # Find contours in the binary image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image (for visualization)
    result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert grayscale image to color for drawing contours
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

    # Count the number of contours (cells)
    num_cells = len(contours)

    # Display the result
    cv2.putText(result_image, f'Cells: {num_cells}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2_imshow(result_image)

    return num_cells

# Example usage
image_path = 'cell.jpg'

# Preprocess the image
preprocessed_image = preprocess_image(image_path)

# Adaptive threshold the preprocessed image
adaptive_thresholded_image = adaptive_threshold_image(preprocessed_image)

# Post-process the thresholded image
post_processed_image = post_process_image(adaptive_thresholded_image)

# Count cells in the post-processed image
num_cells = count_cells(post_processed_image)
print(f'Number of cells: {num_cells}')

from google.colab.patches import cv2_imshow
import cv2
import numpy as np

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising using Non-Local Means Denoising
    denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Smoothing using Gaussian Blur
    smoothed = cv2.GaussianBlur(denoised, (11, 11), 0)

    # Histogram Equalization
    equalized = cv2.equalizeHist(smoothed)

    return equalized

def threshold_image(image, block_size=11, C=2):
    # Adaptive thresholding with Gaussian Mean
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
    return thresh

def count_cells_inner(image):
    # Find contours in the binary image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image (for visualization)
    result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert grayscale image to color for drawing contours
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

    # Count the number of contours (cells)
    num_cells = len(contours)

    # Display the result
    cv2.putText(result_image, f'Cells: {num_cells}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2_imshow(result_image)

    return num_cells

# Example usage
image_path = 'cell.jpg'

# Preprocess the image
preprocessed_image = preprocess_image(image_path)

# Threshold the preprocessed image
thresholded_image = threshold_image(preprocessed_image)

# Count cells in the thresholded image
num_cells_inner = count_cells_inner(thresholded_image)
print(f'Number of cells: {num_cells_inner}')

num_cells = count_cells(post_processed_image)
num_cells_inner = count_cells_inner(thresholded_image)
print("number of cells present in the imgage is : ",num_cells+num_cells_inner)
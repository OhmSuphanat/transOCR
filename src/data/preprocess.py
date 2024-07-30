from PIL import Image
import cv2
import numpy as np

def cv2_to_pil(image):
    return Image.fromarray(image)

def pil_to_cv2(image):
    numpy_image = np.array(image)
    cv2_image = cv2.cvtColor(numpy_image, cv2.IMREAD_GRAYSCALE)
    return cv2_image

def denoise(image):
    cv2_image = pil_to_cv2(image)
    iso_image = cv2.fastNlMeansDenoising(cv2_image, None, h=10, 
                                         templateWindowSize=3, searchWindowSize=21)
    return cv2_to_pil(iso_image)

def add_white_space(image, width_percent: float):
    # Calculate the new width for the white space
    white_space_width = int(image.width * width_percent)

    # Create a new image with white background
    new_width = image.width + white_space_width
    new_img = Image.new("RGB", (new_width, image.height), "white")

    # Paste the original image on the new image, offset by the white space width
    new_img.paste(image, (white_space_width, 0))
    return new_img

def pipeline(image):
    processed = denoise(image=image)
    return processed





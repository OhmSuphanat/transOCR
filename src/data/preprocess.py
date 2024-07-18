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

def delete_line(image):
    cv2_image = pil_to_cv2(image)
    longest_side = max(cv2_image.shape)
    minLineLength = int(longest_side * 0.25)  
    maxLineGap = int(longest_side * 0.01)    
    edges = cv2.Canny(cv2_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=minLineLength, maxLineGap=maxLineGap)
    mask = np.ones_like(image) * 255
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(mask, (x1, y1), (x2, y2), (0, 0, 0), thickness=3)  # Adjust thickness if needed
    mask_inv = cv2.bitwise_not(mask)
    result = cv2.bitwise_or(cv2_image, mask_inv)
    return cv2_to_pil(result)

def pipeline(image):
    processed = denoise(image=image)
    return processed

def preprocess(image_dict):
    for k, v in image_dict.items():
        image_dict[k] = pipeline(v)
    return image_dict


from ultralytics import YOLO
import pytesseract
from pathlib import Path
from src.data.preprocess import *
import os

os.environ["TESSDATA_PREFIX"] = "data/model/tesseract/tessdata"

yolo = YOLO(Path("data/model/yolo/best-section-model.pt"))
tesseract_path = Path("data/model/tesseract/tesseract")
tesseract_config = r"--oem 3 --psm 6"
pytesseract.pytesseract.tesseract_cmd = tesseract_path



def get_OCR(image):
  return pytesseract.image_to_string(image=image, lang='thnd', config=tesseract_config)


def OCR(image_dict: dict):
  ocr_dict = {}
  for k, v in image_dict.items():
    ocr_dict[k] = get_OCR(v)
  return ocr_dict
  

def detect_section(image):
  cv2_image = pil_to_cv2(image)
  coords = yolo(image, conf=0.8)

  section_dict = {}
  boxes = [box for data in coords for box in data.boxes.data]
  for idx, box in enumerate(boxes):
    x, y, h, w, _, _ = box
    x, y, h, w = int(x), int(y), int(w), int(h)
    croped_img = cv2_image[y:h, x:w]
    section_dict[idx] = cv2_to_pil(croped_img)
  return section_dict






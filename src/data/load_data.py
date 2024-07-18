
from PIL import Image

def read_image(path):
    return Image.open(path).convert("L")
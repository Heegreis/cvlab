import numpy as np
import cv2
import math


def contrast_and_brightness(img, value):
    """
    docstring
    """
    # brightness = 0
    # contrast = +200
    brightness = value['brightness']
    contrast = value['contrast']
    cmt = value['contrast_mid_threshold']
    
    B = brightness / 255.0
    c = contrast / 255.0 
    k = math.tan((45 + 44 * c) / 180 * math.pi)

    img = (img - cmt * (1 - B)) * k + cmt * (1 + B)
    # img = (img - 127 * (1 - B)) * k + 127 * (1 + B)
      
    # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
    img = np.clip(img, 0, 255).astype(np.uint8)

    return img
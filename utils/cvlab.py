import cv2
from os import path


class Cvlab():
    """
    docstring
    """
    def __init__(self):
        self.imshow_order = []
        self.imshow_imgs = {}
        
    def imshow(self, img_name, img, save=False, save_dir=''):
        """
        cvlab.imshow('gray_img') = img
        待辦：子階層
        """
        if img_name not in self.imshow_order:
            self.imshow_order.append(img_name)
        self.imshow_imgs[img_name] = img

        imshow_num = self.imshow_order.index(img_name)
        imshow_img = self.imshow_imgs[img_name]

        imshow_name = f'{imshow_num}_{img_name}'

        cv2.namedWindow(imshow_name, cv2.WINDOW_NORMAL)
        cv2.imshow(imshow_name, imshow_img)

        if save:
            save_path = path.join(save_dir, imshow_name+'.jpg')
            cv2.imwrite(save_path, imshow_img)
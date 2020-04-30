import cv2


def gray(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def Negative(img):
    pass

def Powerlaw(img):
    pass

def BinaryThresholding(img):
    pass

def HistogramEqualization(img):
    pass

def MedianFilter(img):
    pass

def Kmeans(img):
    pass

def Sobel(img):
    pass

def Erosion(img):
    pass

def Dilation(img):
    pass

def Opening(img):
    pass

def Closing(img):
    pass

def imgProcess(img, algorithm):
    algorithms = {
        'gray': gray,
        'Negative': Negative,
        'Powerlaw': Powerlaw,
        'BinaryThresholding': BinaryThresholding,
        'HistogramEqualization': HistogramEqualization,
        'MedianFilter': MedianFilter,
        'Kmeans': Kmeans,
        'Sobel': Sobel,
        'Erosion': Erosion,
        'Dilation': Dilation,
        'Opening': Opening,
        'Closing': Closing
    }
    for algo in algorithm:
        img = algorithms[algo](img)
    return img
import cv2


def gray(img, args):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def negative(img, args):
    rows = img.shape[0]
    cols = img.shape[1] 
    for r in range(rows):
        for c in range(cols):
            img[r, c, 0] = 255-img[r, c, 0]
            img[r, c, 1] = 255-img[r, c, 1]
            img[r, c, 2] = 255-img[r, c, 2]
    return img

def powerlaw(img):
    pass

def binaryThresholding(img):
    pass

def histogramEqualization(img):
    pass

def medianFilter(img):
    pass

def kmeans(img):
    pass

def sobel(img):
    pass

def erosion(img):
    pass

def dilation(img):
    pass

def opening(img):
    pass

def closing(img):
    pass

def test(img, args):
    arg1 = args['test-arg1']
    print(arg1)
    return img

def imgProcess(img, algorithms, args):
    algorithmDict = {
        'gray': gray,
        'negative': negative,
        'powerlaw': powerlaw,
        'binaryThresholding': binaryThresholding,
        'histogramEqualization': histogramEqualization,
        'medianFilter': medianFilter,
        'kmeans': kmeans,
        'sobel': sobel,
        'erosion': erosion,
        'dilation': dilation,
        'opening': opening,
        'closing': closing,
        'test': test
    }
    for algo in algorithms:
        img = algorithmDict[algo](img, args)
    return img
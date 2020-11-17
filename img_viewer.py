import cv2
from utils.cvlab import Cvlab


if __name__ == "__main__":
    path = '/win/專案資料/玻璃纖維/實驗圖片收集/整體實驗/20201116/line5-5附著-Feather__2020082503415405_Original-整體實驗/3_增加最後向外消除的範圍/6_canny_show_img.jpg'
    cvlab = Cvlab()
    img = cv2.imread(path)
    cvlab.imshow('viewer', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
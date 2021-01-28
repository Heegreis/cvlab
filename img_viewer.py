import numpy as np
import cv2
import os
import sys
from utils.cvlab import Cvlab
import argparse
import time

def parse_args(in_args=None):
    parser = argparse.ArgumentParser(description="Image viewer")
    parser.add_argument(
        "--path",
        nargs="+",
        required=True,
        help="A list of images",
    )
    parser.add_argument("--compare", action="store_true", help="show two windows for compare with same file name")
    parser.add_argument("--photoshop", action="store_true", help="open photoshop window")
    return parser.parse_args(in_args)

def nothing(x):
    pass

def doSome():
    time.sleep(1)
    return "done"



if __name__ == "__main__":
    args = parse_args()

    if args.compare:    # path 須輸入兩個以上資料夾
        input_paths = []
        input_paths_len = []
        for dir in args.path:
            input_paths_tmp = [os.path.join(dir, fname) for fname in os.listdir(dir)]
            input_paths_tmp.sort()
            input_paths.append(input_paths_tmp)
            input_paths_len.append(len(input_paths_tmp))
        
        set_of_len = len(set(input_paths_len))
        if set_of_len > 1:
            print("檔案數量不一")
            sys.exit()

        cvlab = Cvlab()

        i = 0
        while(i >=0 and i < len(input_paths[0])):
            names = []
            for input_paths_tmp in input_paths:
                names.append(os.path.basename(input_paths_tmp[i]))
            set_of_name = len(set(names))
            if set_of_name > 1:
                print("檔案對應錯誤")
                print(names)
                sys.exit()

            for dir_num, input_paths_tmp in enumerate(input_paths):
                path = input_paths_tmp[i]
                print(path)
                # img = cv2.imread(path)
                img=cv2.imdecode(np.fromfile(path,dtype=np.uint8),-1)
                cvlab.imshow(f'img_{dir_num+1}', img)

            print(names[0], f'{i+1}/{len(input_paths[0])}')
            key = cv2.waitKey(0) & 0xFF
            if key == ord('d'):
                i += 1
                if i >= len(input_paths[0]):
                    i = len(input_paths[0]) - 1
                continue
            if key == ord('a'):
                i -= 1
                if i < 0:
                    i = 0
                continue
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

    else:   # path 為一串圖片路徑 或 一個資料夾
        if os.path.isdir(args.path[0]):
            args.path = [os.path.join(args.path[0], fname) for fname in os.listdir(args.path[0])]
        elif len(args.path) == 1:
            args.path = glob.glob(os.path.expanduser(args.path[0]))
            assert args.path, "The input path(s) was not found"
        input_paths = args.path
        input_paths.sort()

        i = 0
        if args.photoshop:
            value = {}
            tmp_value = {}
        while(i >=0 and i < len(input_paths[0])):
            path = input_paths[i]

            cvlab = Cvlab()
            # img = cv2.imread(path)
            img=cv2.imdecode(np.fromfile(path,dtype=np.uint8),-1)
            cvlab.imshow('viewer', img)

            name = os.path.basename(path)

            print(name, f'{i+1}/{len(input_paths)}')

            if args.photoshop:
                cv2.namedWindow("control panel")
                cv2.createTrackbar("R", "control panel", 0, 255, nothing)
                cv2.createTrackbar("G", "control panel", 0, 255, nothing)
                cv2.createTrackbar("B", "control panel", 0, 255, nothing)
                while(1):
                    # cv2.namedWindow("control panel")
                    # cv2.createTrackbar("R", "control panel", 0, 255, nothing)
                    # cv2.createTrackbar("G", "control panel", 0, 255, nothing)
                    # cv2.createTrackbar("B", "control panel", 0, 255, nothing)
                    

                    value['r'] = cv2.getTrackbarPos('R','control panel')
                    value['g'] = cv2.getTrackbarPos('G','control panel')
                    value['b'] = cv2.getTrackbarPos('B','control panel')

                    if value != tmp_value:
                        tmp_value = value
                        print("start")
                        # 執行ps
                        d = doSome()
                        print(d)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('d'):
                        i += 1
                        if i >= len(input_paths[0]):
                            i = len(input_paths[0]) - 1
                        ps_status = 'd'
                        break
                    if key == ord('a'):
                        i -= 1
                        if i < 0:
                            i = 0
                        ps_status = 'a'
                        break
                    if key == ord('q'):
                        ps_status = 'q'
                        break
                if ps_status == 'd' or ps_status == 'a':
                    continue
                if ps_status == 'q':
                    break


            key = cv2.waitKey(0) & 0xFF
            if key == ord('d'):
                i += 1
                if i >= len(input_paths[0]):
                    i = len(input_paths[0]) - 1
                continue
            if key == ord('a'):
                i -= 1
                if i < 0:
                    i = 0
                continue
            if key == ord('q'):
                break
        cv2.destroyAllWindows()
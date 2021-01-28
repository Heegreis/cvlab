import numpy as np
import cv2
import os
import sys
from utils.cvlab import Cvlab
import argparse

def parse_args(in_args=None):
    parser = argparse.ArgumentParser(description="Image viewer")
    parser.add_argument(
        "--path",
        nargs="+",
        required=True,
        help="A list of images",
    )
    parser.add_argument("--compare", action="store_true", help="show two windows for compare with same file name")
    return parser.parse_args(in_args)

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

    else:   # path 為一串圖片路徑 或 一個資料夾
        if os.path.isdir(args.input[0]):
            args.input = [os.path.join(args.input[0], fname) for fname in os.listdir(args.input[0])]
        elif len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"

        for path in args.input:
            cvlab = Cvlab()
            img = cv2.imread(path)
            cvlab.imshow('viewer', img)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
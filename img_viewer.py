import numpy as np
import cv2
import os
import sys

from numpy.lib.function_base import percentile
from utils.cvlab import Cvlab
from utils.img_process import *
import argparse
import time
import glob
import json

def parse_args(in_args=None):
    parser = argparse.ArgumentParser(description='Image viewer')
    parser.add_argument(
        '--path',
        nargs='+',
        required=True,
        help='A list of images',
    )
    parser.add_argument('--compare', action='store_true', help='show two windows for compare with same file name')
    parser.add_argument('--photoshop', action='store_true', help='open photoshop window')
    parser.add_argument('--enhanpath', help='enhancemment log json')
    parser.add_argument('--savepath', help='img save path')
    return parser.parse_args(in_args)

def nothing(x):
    pass

def doSome(img, value):
    
    time.sleep(1)
    return img



if __name__ == '__main__':
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
            print('檔案數量不一')
            sys.exit()

        cvlab = Cvlab()

        i = 0
        while(i >=0 and i < len(input_paths[0])):
            names = []
            for input_paths_tmp in input_paths:
                names.append(os.path.basename(input_paths_tmp[i]))
            set_of_name = len(set(names))
            if set_of_name > 1:
                print('檔案對應錯誤')
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
            assert args.path, 'The input path(s) was not found'
        input_paths = args.path
        input_paths.sort()

        i = 0
        if args.photoshop:
            value = {}
            tmp_value = {}
            ps_path = ''
            tmp_ps_path = ''
        while(i >=0 and i < len(input_paths[0])):
            path = input_paths[i]
            if args.enhanpath:
                with open(args.enhanpath, 'r') as load_f:
                    load_dict = json.load(load_f)

            cvlab = Cvlab()
            # img = cv2.imread(path)
            img=cv2.imdecode(np.fromfile(path,dtype=np.uint8),-1)
            cvlab.imshow('viewer', img)

            name = os.path.basename(path)

            print(name, f'{i+1}/{len(input_paths)}')

            if args.photoshop:
                cv2.namedWindow('control panel')
                blank_image = np.zeros((200,500,3), np.uint8)
                cv2.createTrackbar('brightness', 'control panel', 0, 510, nothing)
                cv2.createTrackbar('contrast', 'control panel', 0, 510, nothing)
                cv2.createTrackbar('contrast_mid_threshold', 'control panel', 0, 255, nothing)
                cv2.createTrackbar('gap', 'control panel', 1, 10, nothing)
                if args.enhanpath:
                    if not name in load_dict:
                        load_dict[name] = {}
                        load_dict[name]['brightness'] = 0
                        load_dict[name]['contrast'] = 0
                        load_dict[name]['contrast_mid_threshold'] = 128
                        load_dict[name]['gap'] = 1
                    cv2.setTrackbarPos('brightness', 'control panel', load_dict[name]['brightness'] + 255)
                    cv2.setTrackbarPos('contrast', 'control panel', load_dict[name]['contrast'] + 255)
                    cv2.setTrackbarPos('contrast_mid_threshold', 'control panel', load_dict[name]['contrast_mid_threshold'])
                    cv2.setTrackbarPos('gap', 'control panel', load_dict[name]['gap'])
                        

                while(1):
                    value['brightness'] = cv2.getTrackbarPos('brightness','control panel') - 255
                    value['contrast'] = cv2.getTrackbarPos('contrast','control panel') - 255
                    value['contrast_mid_threshold'] = cv2.getTrackbarPos('contrast_mid_threshold','control panel')
                    value['gap'] = cv2.getTrackbarPos('gap','control panel')
                    control_panel_image = blank_image.copy()
                    cv2.putText(control_panel_image, f"brightness: {value['brightness']}", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(control_panel_image, f"contrast: {value['contrast']}", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(control_panel_image, f"contrast_mid_threshold: {value['contrast_mid_threshold']}", (0, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(control_panel_image, f"gap: {value['gap']}", (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.imshow('control panel', control_panel_image)
                    ps_path = path

                    if value != tmp_value or ps_path != tmp_ps_path:
                        tmp_value = value.copy()
                        img_edit = img.copy()
                        tmp_ps_path = ps_path
                        # print('start')
                        # 執行ps
                        img_edit = adjustPixelGap(img_edit, value)
                        img_edit = contrast_and_brightness(img_edit, value)

                        # print('ebd')
                        cv2.namedWindow('edit', cv2.WINDOW_NORMAL)
                        cv2.imshow('edit', img_edit)

                    key = cv2.waitKey(5) & 0xFF
                    if key == ord('r'):
                        cv2.setTrackbarPos('brightness', 'control panel', 255)
                        cv2.setTrackbarPos('contrast', 'control panel', 255)
                        cv2.setTrackbarPos('contrast_mid_threshold', 'control panel', 128)
                        cv2.setTrackbarPos('gap', 'control panel', 1)
                        continue
                    if key == ord('s'):
                        if args.enhanpath:
                            load_dict[name] = value
                            with open(args.enhanpath, 'w') as f:
                                json.dump(load_dict, f)
                            if args.savepath:
                                if os.path.isdir(args.savepath):
                                    save_path = os.path.join(args.savepath, name)
                                    cv2.imwrite(save_path, img_edit)
                            print('saved')
                            continue
                    if key == ord('d'):
                        i += 1
                        if i >= len(input_paths):
                            i = len(input_paths) - 1
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
                if i >= len(input_paths):
                    i = len(input_paths) - 1
                continue
            if key == ord('a'):
                i -= 1
                if i < 0:
                    i = 0
                continue
            if key == ord('q'):
                break
        cv2.destroyAllWindows()
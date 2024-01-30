import os
import argparse
from Augmentation import img_contrast, img_brightness, img_flip, img_rotate, img_blur
import cv2 as cv
from plantcv import plantcv as pcv

def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the directory to analyze
    """

    parser = argparse.ArgumentParser(
                    prog='Distribution',
                    description="Distribution of files in a directory",
                    epilog='----')
    parser.add_argument('folder')
    args = parser.parse_args()
    return args.folder

def main():
    augmentedFunctions = {"contrast": img_contrast, "brightness": img_brightness, "flip": img_flip, "rotate": img_rotate, "blur": img_blur}

    folder = parse_argument()
    for root, dir, files in os.walk(folder):
        for file in files:
            for label, func in augmentedFunctions.items():
                img = pcv.readimage(os.path.join(root, file))
                ret = func(img, )



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
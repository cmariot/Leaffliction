import os
import cv2


if __name__ == "__main__":

    """
    Convert all images in a directory from BGR to RGB
    """

    DIR = "cmariot"

    for root, dirs, files in os.walk(DIR):

        for file in files:

            img = cv2.imread(f"{root}/{file}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            cv2.imwrite(f"{root}/{file}", img)

            print(f"{root}/{file} has been converted from BGR to RGB.")

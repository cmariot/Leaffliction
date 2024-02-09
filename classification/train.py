import argparse
import sys
import os
sys.path.insert(1, '/mnt/nfs/homes/xsaulnie/leaf3/augmentation')
sys.path.insert(1, '/mnt/nfs/homes/xsaulnie/leaf3/transformation')
from Balancing import augmentation_on_directory
from Transformation import transform_directory
import numpy as np

# Args

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Train a classification model"
    )

    parser.add_argument(
        "dir",
        type=str,
    )

    return parser.parse_args().dir


# Augmentation
# Transformation
# Model
# Training
# Evaluation
# Save model

def main():
    dir = parse_arguments()
    print("augmentation on : ", dir)
    augmentation_on_directory(dir, "minifitaug", False)
    transform_directory("minifitaug", "minifitrans", np.array(["Mask"]))




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
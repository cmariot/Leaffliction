import argparse


# Args

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Train a classification model"
    )

    parser.add_argument(
        "dir",
        type=str,
    )

    return parser.parse_args()


# Augmentation
# Transformation
# Model
# Training
# Evaluation
# Save model

def main():
    dir = parse_arguments()
    print(dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
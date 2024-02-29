from mlpackage.parsers.Balancing import parse_argument
from mlpackage.balance.augmentation_on_dir import augmentation_on_directory


if __name__ == "__main__":
    try:
        old_directory = parse_argument()
        augmentation_on_directory(old_directory)
    except Exception as e:
        print(e)
        exit(1)

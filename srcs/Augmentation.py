from mlpackage.parsers.Augmentation import parse_argument
from mlpackage.image_augmentation.ImageAugmentation import ImageAugmentation
from mlpackage.image_augmentation.save_images import save_images
from mlpackage.image_augmentation.plot_images import plot_images
from mlpackage.colors_variable import GREEN, RED, RESET


def intro() -> None:
    print(
        f"""{GREEN}
    _                                    _        _   _
   / \\  _   _  __ _ _ __ ___   ___ _ __ | |_ __ _| |_(_) ___  _ __
  / _ \\| | | |/ _` | '_ ` _ \\ / _ \\ '_ \\| __/ _` | __| |/ _ \\| '_ \\
 / ___ \\ |_| | (_| | | | | | |  __/ | | | || (_| | |_| | (_) | | | |
/_/   \\_\\__,_|\\__, |_| |_| |_|\\___|_| |_|\\__\\__,_|\\__|_|\\___/|_| |_|
              |___/
{RESET}\n""" +
        "This program displays the original image and the augmented images.\n"
        "The augmented images are saved in the same directory as the",
        "original image.\n"
    )


def main():

    intro()

    # Filename is the path of the image to augment
    filename = parse_argument()

    # Read the image
    image = ImageAugmentation.read_image(filename)

    # Dictionary with the label of the image as key and the augmented image as
    # value
    images = {
        "Original": image,
        "Contrast": ImageAugmentation.contrast(image),
        "Brightness": ImageAugmentation.brightness(image),
        "Zoomed": ImageAugmentation.zoom(image),
        "Flipped": ImageAugmentation.flip(image),
        "Rotated": ImageAugmentation.rotate(image),
        "Blurred": ImageAugmentation.blur(image),
        "Distortion": ImageAugmentation.distortion(image)
    }

    save_images(images, filename)
    plot_images(images, filename)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(RED + "Error:", RESET, error)

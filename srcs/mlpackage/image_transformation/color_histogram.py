import matplotlib.pyplot as plt
from plantcv import plantcv as pcv


def plot_stat_hist(label, sc=1):

    """
    Retrieve the histogram x and y values and plot them
    """

    y = pcv.outputs.observations['default_1'][label]['value']
    x = [
        i * sc
        for i in pcv.outputs.observations['default_1'][label]['label']
    ]
    if label == "hue_frequencies":
        x = x[:int(255 / 2)]
        y = y[:int(255 / 2)]
    if (
        label == "blue-yellow_frequencies" or
        label == "green-magenta_frequencies"
    ):
        x = [x + 128 for x in x]
    plt.plot(x, y, label=label)


def plot_histogram(image, kept_mask):

    """
    Plot the histogram of the image
    """

    dict_label = {
        "blue_frequencies": 1,
        "green_frequencies": 1,
        "green-magenta_frequencies": 1,
        "lightness_frequencies": 2.55,
        "red_frequencies": 1,
        "blue-yellow_frequencies": 1,
        "hue_frequencies": 1,
        "saturation_frequencies": 2.55,
        "value_frequencies": 2.55
    }

    labels, _ = pcv.create_labels(mask=kept_mask)
    pcv.analyze.color(
        rgb_img=image,
        colorspaces="all",
        labeled_mask=labels,
        label="default"
    )

    plt.subplots(figsize=(16, 9))
    for key, val in dict_label.items():
        plot_stat_hist(key, val)

    plt.legend()

    plt.title("Color Histogram")
    plt.xlabel("Pixel intensity")
    plt.ylabel("Proportion of pixels (%)")
    plt.grid(
        visible=True,
        which='major',
        axis='both',
        linestyle='--',
    )
    plt.show()
    plt.close()

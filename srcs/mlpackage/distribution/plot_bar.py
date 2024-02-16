import matplotlib.pyplot as plt


def plot_bar(data: dict, path: str):

    """
    Plot a bar chart representing the distribution of files in a directory
    """

    plt.figure(2, figsize=(16, 9))
    plt.title(f"Bar chart representing the distribution of files in {path}")
    plt.bar(
        x=data.keys(),
        height=data.values(),
    )
    for index, value in enumerate(data.values()):
        plt.text(
            x=index,
            y=value,
            s=str(value),
            horizontalalignment="center",
            verticalalignment="bottom",
        )
    plt.xticks(rotation=45)
    plt.ylabel("Number of files")
    plt.xlabel("Name of the subdirectory")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()

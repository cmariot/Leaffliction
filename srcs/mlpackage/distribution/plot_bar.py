import matplotlib.pyplot as plt


def plot_bar(data: dict, path: str):

    """
    Plot a bar chart representing the distribution of files in a directory
    """

    # Create the figure
    plt.figure(figsize=(16, 9))

    # Title
    plt.suptitle(
        f"Bar chart representing the distribution of files in {path}",
        fontweight="bold",
    )

    # Plot the bar chart
    plt.bar(
        x=data.keys(),
        height=data.values(),
    )

    # Add the number of files on top of each bar
    for index, value in enumerate(data.values()):
        plt.text(
            x=index,
            y=value,
            s=str(value),
            horizontalalignment="center",
            verticalalignment="bottom",
        )

    # Add labels and grid
    plt.xticks(rotation=45)
    plt.ylabel("Number of files")
    plt.xlabel("Name of the subdirectory")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)

    # Tight layout to avoid overlapping (not necessary but looks better)
    plt.tight_layout()

    # Show the plot
    plt.show()

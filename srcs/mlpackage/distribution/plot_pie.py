import matplotlib.pyplot as plt


def plot_pie(data: dict, path: str):

    """
    Plot a pie chart representing the distribution of files in a directory
    """

    # Create the figure
    plt.figure(figsize=(16, 9))

    # Title
    plt.title(
        f"Pie chart representing the distribution of files in {path}",
        fontweight="bold",
        y=0.001
    )

    # Plot the pie chart
    plt.pie(
        x=data.values(),
        labels=data.keys(),
        autopct="%.2f%%",
        pctdistance=.8,
        labeldistance=1.1
    )

    # Tight layout to avoid overlapping (not necessary but looks better)
    plt.tight_layout()

    # Show the plot
    plt.show()

import matplotlib.pyplot as plt


def plot_pie(data: dict, path: str):

    """
    Plot a pie chart representing the distribution of files in a directory
    """

    plt.figure(1, figsize=(16, 9))
    plt.title(f"Pie chart representing the distribution of files in {path}")
    plt.pie(
        x=data.values(),
        labels=data.keys(),
        autopct="%.2f%%",
        pctdistance=.8,
        labeldistance=1.1
    )
    plt.show()

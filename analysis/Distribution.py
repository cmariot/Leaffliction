import os
import argparse
import matplotlib.pyplot as plt


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the directory to analyze
    """

    parser = argparse.ArgumentParser(
                    prog='Distribution',
                    description="Distribution of files in a directory",
                    epilog='----')
    parser.add_argument('path')
    args = parser.parse_args()
    return args.path


def path_to_name(path: str) -> str:

    """
    Return the name of the directory without the path,
    if the path is a file return the name of the file
    """

    car = path.rfind("/")
    if (car == -1):
        return path
    else:
        return path[car + 1:]


def count_files(path: str) -> dict:

    """
    Return a dictionary with the name of the directory as key
    and the number of files in the directory as value
    """

    data = {}
    for root, dir, files in os.walk(path):
        number_of_files = len(files)
        if number_of_files != 0:
            data[path_to_name(root)] = number_of_files

        # ⚠️ A gerer, le cas ou un le nom d'un dossier apparait plusieurs fois ?

    # elems = []
    # for key, value in data.items():
    #     if value == 0:
    #         elems.append(key)
    # for key in elems:
    #     data.pop(key)

    return data


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


def plot_bar(data: dict, path: str):

    """
    Plot a bar chart representing the distribution of files in a directory
    """

    plt.figure(2, figsize=(16, 9))
    plt.title(f"Bar chart representing the distribution of files in {path}")
    plt.bar(
        x=data.keys(),
        height=data.values()
    )


def main():

    # The path of the directory to analyze
    path = parse_argument()

    # Dictionary with the name of the directory as key and the number of files
    # in the directory as value
    data = count_files(path)

    # Bar chart
    plot_bar(data, path)

    # Pie chart
    plot_pie(data, path)

    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)

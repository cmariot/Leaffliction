from mlpackage.parsers.Distribution import parse_argument
from mlpackage.distribution.print_directory_structure \
    import print_directory_structure
from mlpackage.distribution.count_files import count_files
from mlpackage.distribution.plot_bar import plot_bar
from mlpackage.distribution.plot_pie import plot_pie
from mlpackage.colors_variable import GREEN, RED, RESET
from pyfiglet import Figlet


def intro():
    print(
        f"{GREEN}{Figlet(font='big').renderText('Distribution')}{RESET}\n""" +
        "This program takes a directory as argument and display a bar chart" +
        "\nand a pie chart representing the distribution of files in the\n" +
        "directory.\n"
    )


def main():

    # Print the intro
    intro()

    # The path of the directory to analyze
    path = parse_argument()

    # Print the structure of the directory
    print_directory_structure(path)

    # Dictionary with the name of the directory as key and the number of files
    # in the directory as value
    data = count_files(path)

    # Bar chart
    plot_bar(data, path)

    # Pie chart
    plot_pie(data, path)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"{RED}Error: {RESET}{error}")

from mlpackage.parsers.Distribution import parse_argument
from mlpackage.distribution.print_directory_structure \
    import print_directory_structure
from mlpackage.distribution.count_files import count_files
from mlpackage.distribution.plot_bar import plot_bar
from mlpackage.distribution.plot_pie import plot_pie
from mlpackage.colors_variable import GREEN, RED, RESET


def intro():
    print(
        f"""{GREEN} ____  _     _        _ _           _   _
|  _ \\(_)___| |_ _ __(_) |__  _   _| |_(_) ___  _ __
| | | | / __| __| '__| | '_ \\| | | | __| |/ _ \\| '_ \\
| |_| | \\__ \\ |_| |  | | |_) | |_| | |_| | (_) | | | |
|____/|_|___/\\__|_|  |_|_.__/ \\__,_|\\__|_|\\___/|_| |_|

{RESET}""" +
        "This program takes a directory as argument and display a bar chart\n" +
        "and a pie chart representing the distribution of files in the\n" +
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

def intro():
    GREEN = "\033[92m"
    RESET = "\033[0m"
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

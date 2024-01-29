import os
import argparse
import matplotlib.pyplot as plt


def parse_argument():

    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('path')
    args = parser.parse_args()
    return args.path


def path_to_name(path):
    car = path.rfind("/")
    if (car == -1):
        return path
    else:
        return path[car + 1:]


def main():

    path = parse_argument()

    data = {}

    for root, dir, files in os.walk(path):
        data[path_to_name(root)] = len(files)

    elems = []

    for key, value in data.items():
        if value == 0:
            elems.append(key)

    for key in elems:
        data.pop(key)

    plt.figure(1)
    plt.pie(data.values(), labels=data.keys(), autopct="%.2f%%")
    plt.figure(2)
    plt.bar(data.keys(), data.values())
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)

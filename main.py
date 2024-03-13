import re

from sys import argv


FOLDER_NAME_FROM_LINK_PATTERN = r"/(\d+)(\.html)?(#.*)?/?$"


def main():
    # Get params from user input in console
    if len(argv) < 3:
        print("Usage: python3.11 main.py <host_type> <url1> <url2> ...")
        return

    links_and_folder_names = {}

    for link in argv[2:]:
        match = re.search(FOLDER_NAME_FROM_LINK_PATTERN, link)
        if match:
            links_and_folder_names[link] = match.group(1)
        else:
            print(f"Incorrect link: {link}")

    for k, v in links_and_folder_names.items():
        print(k + " : " + v)


if __name__ == "__main__":
    main()

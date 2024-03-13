import re
import time

from sys import argv

FOLDER_NAME_FROM_LINK_PATTERN = r"/(\d+)(\.html)?(#.*)?/?$"


def main():
    # Get params from user input in console
    if len(argv) < 3:
        print("Usage: python3.11 main.py <host_type> <url1> <url2> ...")
        return

    host_type = argv[1]

    # Check host from user is correct
    if host_type != "2ch" and host_type != "archivach":
        print('Incorrent host. Correct: "2ch" or "archivach"')
        return

    links_and_folder_names = {}

    for link in argv[2:]:
        match = re.search(FOLDER_NAME_FROM_LINK_PATTERN, link)
        if match:
            links_and_folder_names[link] = match.group(1)
        else:
            print(f"Incorrect link: {link}")

    for k, v in links_and_folder_names.items():
        downloader(host_type, k, v)


def downloader(host_type, url, output_directory):
    print(host_type)
    print(url)
    print(output_directory)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time} seconds")

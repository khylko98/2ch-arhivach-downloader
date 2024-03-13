import re
import time
import requests

from sys import argv
from bs4 import BeautifulSoup

FOLDER_NAME_FROM_LINK_PATTERN = r"/(\d+)(\.html)?(#.*)?/?$"


def main():
    # Get params from user input in console
    if len(argv) < 4:
        print("Usage: python3.11 main.py <output_path> <host_type> <url1> <url2> ...")
        return

    output_path = argv[1]
    host_type = argv[2]

    # Check host from user is correct
    if host_type != "2ch" and host_type != "archivach":
        print('Incorrent host. Correct: "2ch" or "archivach"')
        return

    links_and_folder_names = {}

    for link in argv[3:]:
        match = re.search(FOLDER_NAME_FROM_LINK_PATTERN, link)
        if match:
            links_and_folder_names[link] = match.group(1)
        else:
            print(f"Incorrect link: {link}")

    for k, v in links_and_folder_names.items():
        downloader(output_path, host_type, k, v)


def downloader(output_path, host_type, url, folder_name):
    print(output_path)
    print(host_type)
    print(url)
    print(folder_name, end="\n\n")
    
    try:
        # Get response by url
        response = requests.get(url)

        # Check response content
        print(response.content)

        if response.status_code == 200:
            # Parse response content
            soup = BeautifulSoup(response.content, "html.parser")

            # Check parsing result
            print(soup)
        else:
            print(f"Failed to download from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time} seconds")

import os
import re
import requests
import time

from sys import argv
from bs4 import BeautifulSoup

# Regular expression pattern to extract folder names from links
FOLDER_NAME_FROM_LINK_PATTERN = r"/(\d+)(\.html)?(#.*)?/?$"

# Constants for host URLs
DVACH = "https://2ch.hk"
ARCHIVACH = "https://arhivach.top"

# Constants for media extensions
IMAGE_EXT = [".jpg", ".png", ".gif"]
VIDEO_EXT = [".mp4", ".webm"]


def main():
    # Check if enough arguments are provided
    if len(argv) < 3:
        print("Usage: python3.11 main.py <output_path> <url1> <url2> ...")
        return

    output_path = argv[1]  # Output directory path

    links_and_folder_names = {}

    # Extract links and folder names
    for link in argv[2:]:
        match = re.search(FOLDER_NAME_FROM_LINK_PATTERN, link)
        if match:
            links_and_folder_names[link] = match.group(1)
        else:
            print(f"Incorrect link: {link}")

    # Download content from each link
    for k, v in links_and_folder_names.items():
        if "2ch" in k:
            downloader(output_path + v, "2ch", k)
        elif "arhivach" in k:
            downloader(output_path + v, "arhivach", k)


def downloader(output_path, host_type, url):
    try:
        # Get response from the URL
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find links to download
            links = soup.find_all(
                "a",
                href=lambda href: href
                and (
                    href.endswith(".jpg")
                    or href.endswith(".png")
                    or href.endswith(".gif")
                    or href.endswith(".mp4")
                    or href.endswith(".webm")
                ),
            )

            # Create directory if it does not exist
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Download each file
            for link in links:
                link_href = link["href"]

                # Construct full URL based on host type
                if host_type == "2ch":
                    path = DVACH + link_href
                elif host_type == "arhivach":
                    if any(extension in link_href for extension in IMAGE_EXT):
                        path = ARCHIVACH + link_href
                    elif any(extension in link_href for extension in VIDEO_EXT):
                        path = link_href

                # Extract filename from URL
                filename = os.path.join(output_path, path.split("/")[-1])

                # Download and save file
                with open(filename, "wb") as file:
                    file.write(requests.get(path).content)

                print(f"Downloaded {filename} successfully!")
        else:
            print(f"Failed to download from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

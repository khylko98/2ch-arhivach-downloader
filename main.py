import os
import re
import time
import requests

from sys import argv
from bs4 import BeautifulSoup

FOLDER_NAME_FROM_LINK_PATTERN = r"/(\d+)(\.html)?(#.*)?/?$"
DVACH = "https://2ch.hk"
ARCHIVACH = "https://arhivach.top"


def main():
    # Get params from user input in console
    if len(argv) < 3:
        print("Usage: python3.11 main.py <output_path> <url1> <url2> ...")
        return

    output_path = argv[1]

    links_and_folder_names = {}

    for link in argv[2:]:
        match = re.search(FOLDER_NAME_FROM_LINK_PATTERN, link)
        if match:
            links_and_folder_names[link] = match.group(1)
        else:
            print(f"Incorrect link: {link}")

    for k, v in links_and_folder_names.items():
        if "2ch" in k:
            downloader(output_path, "2ch", k, v)
        elif "arhivach" in k:
            downloader(output_path, "arhivach", k, v)


def downloader(output_path, host_type, url, folder_name):
    try:
        # Get response by url
        response = requests.get(url)

        if response.status_code == 200:
            # Parse response content
            soup = BeautifulSoup(response.content, "html.parser")

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

            if not os.path.exists(f"{output_path}{folder_name}"):
                os.makedirs(f"{output_path}{folder_name}")

            for link in links:
                link_href = link["href"]

                if host_type == "2ch":
                    path = DVACH + link_href
                elif host_type == "arhivach":
                    if any(
                        extension in link_href for extension in [".jpg", ".png", ".gif"]
                    ):
                        path = ARCHIVACH + link_href
                    elif any(extension in link_href for extension in [".mp4", ".webm"]):
                        path = link_href

                filename = os.path.join(
                    f"{output_path}{folder_name}", path.split("/")[-1]
                )

                with open(filename, "wb") as file:
                    file.write(requests.get(path).content)

                print(f"Downloaded {filename} successfully!")
        else:
            print(f"Failed to download from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time} seconds")

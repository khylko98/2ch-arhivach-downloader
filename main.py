import os
import re
import requests

from sys import argv
from bs4 import BeautifulSoup

# Regular expression pattern to extract folder names from links
FOLDER_NAME_FROM_LINK_PATTERN = r"/(\d+)(\.html)?(#.*)?/?$"

# Constants for host URLs
DVACH = "https://2ch.hk"
ARHIVACH_DOMAINS = ["https://arhivach.top", "https://arhivach.xyz", "https://arhivach.hk"]

# Constants for media extensions
IMAGE_EXT = [".jpg", ".png", ".gif"]
VIDEO_EXT = [".mp4", ".webm"]


def main():
    if len(argv) < 3:
        print("Usage: python main.py <output_path> <url1> <url2> ...")
        return

    output_path = argv[1]
    links_and_folder_names = {}

    # Extract links and folder names
    for link in argv[2:]:
        match = re.search(FOLDER_NAME_FROM_LINK_PATTERN, link)
        if match:
            links_and_folder_names[link] = match.group(1)
        else:
            print(f"Incorrect link: {link}")

    # Download content from each link
    for link, folder_name in links_and_folder_names.items():
        if "2ch" in link:
            downloader(output_path + folder_name, "2ch", link)
        elif "arhivach" in link:
            downloader(output_path + folder_name, "arhivach", link)


def downloader(output_path, host_type, url):
    if host_type == "2ch":
        try_download(output_path, DVACH, url)
    elif host_type == "arhivach":
        # Try both domains
        for domain in ARHIVACH_DOMAINS:
            success = try_download(output_path, domain, url)
            if success:
                print(f"Successfully downloaded from {domain}")
                break
        else:
            print(f"Failed to download from both {ARHIVACH_DOMAINS[0]} "
                  f"and {ARHIVACH_DOMAINS[1]}")


def try_download(output_path, base_url, url):
    """Attempt to download content from a given base URL."""
    try:
        # Modify the URL to use the given base URL
        adjusted_url = re.sub(r"https://arhivach\.\w+", base_url, url)
        response = requests.get(adjusted_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find media links
            links = soup.find_all(
                "a",
                href=lambda href: isinstance(href, str) and
                any(href.endswith(ext) for ext in IMAGE_EXT + VIDEO_EXT),
            )

            # Create directory if it does not exist
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Download each file
            for link in links:
                link_href = link["href"]
                if not link_href.startswith("http"):
                    link_href = base_url + link_href

                filename = os.path.join(output_path, link_href.split("/")[-1])

                # Download and save the file
                with open(filename, "wb") as file:
                    file.write(requests.get(link_href).content)

                print(f"Downloaded {filename} successfully!")

            return True
        else:
            print(f"Failed to download from {adjusted_url}. "
                  f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while trying {base_url}: {str(e)}")
        return False


if __name__ == "__main__":
    main()

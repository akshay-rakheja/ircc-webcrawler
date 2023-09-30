import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()


def crawl_website(url, depth=0, max_depth=2):
    if depth > max_depth:
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            visited.add(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Save content to a file
            save_content_to_file(url, soup.get_text())

            links = soup.find_all('a')
            for link in links:
                absolute_link = urljoin(url, link.get('href'))
                base_url = urlparse(url).scheme + "://" + \
                    urlparse(url).hostname

                # Check if "immigration" is in the URL
                if "immigration" in absolute_link:
                    if base_url in absolute_link and absolute_link not in visited:
                        print(f"Crawling: {absolute_link}")
                        crawl_website(absolute_link, depth + 1, max_depth)

        else:
            print(
                f"Failed to retrieve the website. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


def save_content_to_file(url, content):
    # Create a directory named "data" if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # Replace all non-alphanumeric characters with underscores
    filename = "".join(c if c.isalnum() else "_" for c in url)

    # Write the content to a file in the "data" directory
    with open(f"data/{filename}.txt", "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    crawl_website(
        "https://www.canada.ca/en/immigration-refugees-citizenship.html")

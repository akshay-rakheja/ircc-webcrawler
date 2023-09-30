import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Set to store visited URLs
visited = set()


def crawl_website(url, depth=0, max_depth=2):
    if depth > max_depth:
        return

    try:
        # Sending a GET request to the URL
        response = requests.get(url)

        # Checking if the GET request was successful
        if response.status_code == 200:

            # Mark the URL as visited
            visited.add(url)

            # Parsing the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Capture text data (example: capturing text within paragraph tags)
            paragraphs = soup.find_all('p')
            for i, p in enumerate(paragraphs):
                print(f"Paragraph {i+1}: {p.get_text()}")

            # Find all the links on the web page
            links = soup.find_all('a')

            for link in links:
                # Create an absolute URL
                absolute_link = urljoin(url, link.get('href'))

                # Extract the base URL to stick to the same domain
                base_url = urlparse(url).scheme + "://" + \
                    urlparse(url).hostname

                # Continue crawling if it's an unvisited link within the same domain
                if base_url in absolute_link and absolute_link not in visited:
                    print(f"Crawling: {absolute_link}")
                    crawl_website(absolute_link, depth + 1, max_depth)

        else:
            print(
                f"Failed to retrieve the website. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    url_to_crawl = 'https://www.canada.ca/en/immigration-refugees-citizenship.html'
    crawl_website(url_to_crawl)

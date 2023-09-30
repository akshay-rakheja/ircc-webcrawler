import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

visited = set()


def is_related_to_immigration(text):
    # Use the first 1000 characters
    prompt = f"What is this text about: {text[:1000]}"
    response = openai.ChatCompletion.create(
        engine="gpt-4", messages=[{"role": "user", "content": "Hello world"}])

    # If the response contains "immigration" or "Canada", return True
    return "immigration" in response.choices[0].text.lower() or "canada" in response.choices[0].text.lower()


def crawl_website(url, depth=0, max_depth=2):
    if depth > max_depth:
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            visited.add(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()

            # Check if the page is related to immigration
            if is_related_to_immigration(page_text):
                save_content_to_file(url, page_text)

            links = soup.find_all('a')
            for link in links:
                absolute_link = urljoin(url, link.get('href'))
                base_url = urlparse(url).scheme + "://" + \
                    urlparse(url).hostname

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

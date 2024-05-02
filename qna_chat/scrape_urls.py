"""scrape_urls: """

__author__ = "Rajesh Pethe"
__date__ = "09/01/2024 18:16:58"
__credits__ = ["Rajesh Pethe"]

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse
import requests
from celery import shared_task


def get_drf_urls() -> list:
    base_url = "https://www.django-rest-framework.org/"
    base_response = requests.get(
        base_url,
        headers={
            "Accept": "application/xml; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
        },
        timeout=5,
    )
    base_html = base_response.content.decode("utf-8")
    soup = BeautifulSoup(base_html, "html.parser")

    # Parse the root URL to extract components
    base_url_parts = urlparse(base_url)

    # URLs from sidebar nav
    links = [
        i
        for i in soup.find(
            "ul", {"class": "nav nav-list side-nav well sidebar-nav-fixed"}
        ).find_all("a", href=True)
    ]

    for i in soup.find_all("ul", {"class": "dropdown-menu"}):
        links.extend(i.find_all("a", href=True))

    print(f"Number of links: {len(links)}")

    result = set()
    for link in links:
        path = link.get("href")
        if path.endswith("announcement/") or path.startswith("#"):
            # Avoid version announcements
            continue

        # if "tutorial" not in path:
        #     continue

        if not path.startswith("#"):
            path = urlparse(path).path

        url = f"{base_url_parts.scheme}://{base_url_parts.netloc}/{path}"

        if not url.endswith("/"):
            url += "/"
        result.add(url)
    return list(result)

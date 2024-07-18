from temporalio import activity

import logging
log = logging.getLogger(__name__)

def _remove_url_params(url):
    from urllib.parse import urlparse, urlunparse
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query="", fragment=""))


@activity.defn()
def extract_links_from_url(url, class_):
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    from ..database import db_get_html

    html = db_get_html(url)
    assert html is not None, 'no html for this page/'

    soup = BeautifulSoup(html, 'html.parser')
    urls = set()

    a_tags = soup.find_all('a', class_=class_, href=True) if class_ else soup.find_all('a', href=True)
    for a_tag in a_tags:
        href = a_tag['href']
        full_url = urljoin(url, href)
        full_url = _remove_url_params(full_url)
        urls.add(full_url)
        log.info("adding new url to visit: %s", full_url)

    return urls
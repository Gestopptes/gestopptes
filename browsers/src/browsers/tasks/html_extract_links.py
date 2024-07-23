from temporalio import activity

import logging
log = logging.getLogger(__name__)

def _remove_url_params(url):
    from urllib.parse import urlparse, urlunparse
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query="", fragment=""))


def accept_url_link(next_url, scrape_options):
    from urllib.parse import urlparse
    
    orig_domain = urlparse(scrape_options['url']).netloc
    new_domain = urlparse(next_url).netloc
    if scrape_options['same_domain']:
        if orig_domain != new_domain:
            return False
    if scrape_options['allow_domain_list']:
        if new_domain not in scrape_options['allow_domain_list']:
            return False
    if scrape_options['reject_domain_list']:
        if new_domain in scrape_options['reject_domain_list']:
            return False
    if scrape_options['url_filter_regex']:
        import re
        if re.match(scrape_options['url_filter_regex'], new_domain) is None:
            return False
    return True


@activity.defn()
def extract_links_from_url(url, scrape_options):
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    from ...database import db_get_html
    class_ = scrape_options['link_class']

    html = db_get_html(url)
    assert html is not None, 'no html for this page/'

    soup = BeautifulSoup(html, 'html.parser')
    urls = set()

    a_tags = soup.find_all('a', class_=class_, href=True) if class_ else soup.find_all('a', href=True)
    activity.logger.info("found %s link tags", len(a_tags))
    for a_tag in a_tags:
        href = a_tag['href']
        full_url = urljoin(url, href)
        full_url = _remove_url_params(full_url)
        if accept_url_link(full_url, scrape_options):
            urls.add(full_url)
            log.info("extracted link: %s", full_url)
    return urls
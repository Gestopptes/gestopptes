from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time

print("hello sirs")
DBNAME = 'cache-html-pages'

def make_driver():
    print("start make driver...")
    options = ChromeOptions()
    options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')
    driver = webdriver.Remote(options=options, command_executor="http://localhost:4444")
    # driver.get("https://selenium.dev")
    print("done get driver.")
    return driver


def make_mongo_client():
    import pymongo
    return pymongo.MongoClient("localhost", 27017,username="root", password="example")

def init_mongo(client):
    dblist = client.list_database_names()
    db = client[DBNAME]
    db["screenshot-png"].create_index("url", unique=True)
    db["html"].create_index("url", unique=True)
    print("mongo dblist: ", str(dblist))


def db_get_html(url):
    client = make_mongo_client()
    db = client[DBNAME]
    html_col = db["html"]
    x = html_col.find_one({"url": url})
    if x:
        return x['html']

def db_save_html(url, html):
    client = make_mongo_client()
    db = client[DBNAME]
    html_col = db["html"]
    html_col.insert_one({"url": url, "html": html})

def db_get_screenshot(url):
    client = make_mongo_client()
    db = client[DBNAME]
    ccol = db["screenshot-png"]
    x = ccol.find_one({"url": url})
    if x:
        return ['png']

def db_get_all_screenshot():
    client = make_mongo_client()
    db = client[DBNAME]
    ccol = db["screenshot-png"]
    return ccol.find()


def db_set_screenshot(url, png):
    client = make_mongo_client()
    db = client[DBNAME]
    ccol = db["screenshot-png"]
    ccol.insert_one({"url": url, "png": png})


def render_page_to_html(driver, url):
    if html:= db_get_html(url):
        print("page found in cache, skip:", url)
        return html
    print("rendering url: ", url)
    driver.get(url)
    html = driver.find_element(By.TAG_NAME, "html").get_attribute('innerHTML')

    print("got html len: {}", len(html))
    db_save_html(url, html)
    db_set_screenshot(url, driver.get_screenshot_as_png())
    return html


def remove_url_params(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query="", fragment=""))


def get_children_urls(driver, base_url, filter_func=None, class_=None, max_depth=3, delay=0.3):
    visited = set()

    def fetch_urls(url, depth):
        if depth > max_depth or url in visited:
            return set()
        
        url = remove_url_params(url)
        visited.add(url)
        
        time.sleep(delay)
        
        try:
            html = render_page_to_html(driver, url)
        except Exception as e:
            print(f"An error occurred while fetching {url}: {e}")
            raise
            return set()

        soup = BeautifulSoup(html, 'html.parser')
        urls = set()

        a_tags = soup.find_all('a', class_=class_, href=True) if class_ else soup.find_all('a', href=True)
        for a_tag in a_tags:
            href = a_tag['href']
            full_url = urljoin(url, href)
            full_url = remove_url_params(full_url)
            if filter_func is None or filter_func(full_url):
                urls.add(full_url)
                print("adding new url to visit: ", full_url)
                urls.update(fetch_urls(full_url, depth + 1))

        return urls

    result = sorted(set(fetch_urls(base_url, 0)))
    return result

# Example filter function
def example_filter(url):
    return "langchain.com/v0.2" in url

def example_alex_scrape_ceva(driver):
    # Example usage
    base_url = 'https://github.com/langchain-ai/langchain/tree/langchain%3D%3D0.2.6/templates/csv-agent'
    children_urls = get_children_urls(driver, base_url, filter_func=None, max_depth=3, class_='Link--primary')
    for url in children_urls:
        if url.endswith('.py') or url.endswith('.md'):
            print(url)


if __name__ == "__main__":
    monclient = make_mongo_client()
    init_mongo(monclient)
    
    driver = make_driver()
    try:
        example_alex_scrape_ceva(driver)
    finally:
        driver.quit()

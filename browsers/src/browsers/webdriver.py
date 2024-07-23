from ..config import SELENIUM_PAGE_LOAD_TIMEOUT, SELENIUM_IP
import logging
import os
log = logging.getLogger(__name__)

def make_chrome_options():
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    options = ChromeOptions()
    options.set_capability('se:name', 'GESTOPT CHROME DRIVER')
    options.headless = True
    options.add_argument('--headless=new')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
        
    CHROME_EXTENSION_FOLDER = os.path.join(os.path.dirname(__file__), "extensions", "chrome")
    for filename in os.listdir(CHROME_EXTENSION_FOLDER):
        if filename.endswith(".crx"):
            filepath = os.path.join(CHROME_EXTENSION_FOLDER, filename)
            log.info("chrome options add extension: %s", filename)
            options.add_extension(filepath)
    return options


def make_driver():
    from selenium import webdriver

    log.info("start make driver...")
    options = make_chrome_options()
    # options.add_argument("--no-sandbox")
    driver = webdriver.Remote(options=options, command_executor=f'http://{SELENIUM_IP}:4444')
    driver.set_page_load_timeout(SELENIUM_PAGE_LOAD_TIMEOUT)
    driver.set_script_timeout(SELENIUM_PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(SELENIUM_PAGE_LOAD_TIMEOUT)

    # driver.get("https://selenium.dev")
    log.info("done get driver.")
    return driver

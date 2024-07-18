from .config import PAGE_LOAD_TIMEOUT, SELENIUM_ADDRESS
import logging
log = logging.getLogger(__name__)

def make_driver():
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium import webdriver

    log.info("start make driver...")
    options = ChromeOptions()
    options.set_capability('se:name', 'DRIVER')
    options.headless = True
    options.add_argument('--headless=new')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--no-sandbox")
    driver = webdriver.Remote(options=options, command_executor=SELENIUM_ADDRESS)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.set_script_timeout(PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(PAGE_LOAD_TIMEOUT)
    # driver.get("https://selenium.dev")
    log.info("done get driver.")
    return driver

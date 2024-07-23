from temporalio import activity
import time
import logging
log = logging.getLogger(__name__)


@activity.defn()
def selenium_render_page_to_html(url):
    from selenium.webdriver.common.by import By
    from ...database import db_save_html_and_pic, db_get_html
    from ..webdriver import make_driver

    # check before getting browser
    if html := db_get_html(url):
        log.info("page found in db (1), skip: %s", url)
        return
    
    log.info("fetching driver...")
    driver = make_driver()
    log.info("driver ok.")
    try:
        # check after getting browser
        if html := db_get_html(url):
            log.info("page found in db (2), skip: %s", url)
            return
        
        log.info("rendering url: %s", url)
        driver.get(url)
        time.sleep(0.1)
        html = driver.find_element(By.TAG_NAME, "html").get_attribute('innerHTML')
        picture = driver.get_screenshot_as_png()
    finally:
        log.info("close driver...")
        driver.close()

    log.info("got html len: %s.", len(html))
    db_save_html_and_pic(url, html, picture)
    log.info("saved html and pic.")
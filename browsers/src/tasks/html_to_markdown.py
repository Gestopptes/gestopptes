
from temporalio import activity
import re

import logging
log = logging.getLogger(__name__)

def markdown_strip_spaces(page_markdown):
    COUNT = 99999

    def clean_init(page_markdown):
        page_markdown = page_markdown.strip()
        page_markdown = "\n".join(p.strip() for p in page_markdown.splitlines())
        return page_markdown

    def clean_one(page_markdown):
        page_markdown = re.sub(' +', ' ', page_markdown, count=COUNT)
        page_markdown = re.sub('\n \n', '\n\n', page_markdown, count=COUNT)
        page_markdown = re.sub('\n\n\n+', '\n\n', page_markdown, count=COUNT)
        return page_markdown
    
    init_page = clean_init(page_markdown)
    new_page = clean_one(init_page)
    for _ in range(COUNT):
        init_page = new_page
        new_page = clean_one(init_page)
        if new_page == init_page:
            break

    return new_page


@activity.defn()
def extract_markdown_from_html(url):
    from markdownify import markdownify
    from ..database import db_get_html, db_set_markdown

    html = db_get_html(url)
    assert html is not None, "no htmlm in db WTF??"
    page_markdown = markdownify(html)
    log.info("markdown convert OK")
    pre_len = len(page_markdown)
    page_markdown = markdown_strip_spaces(page_markdown)
    post_len = len(page_markdown)
    log.info("markdown strip whitespace: %s ---> %s", pre_len, post_len)
    db_set_markdown(url, page_markdown)

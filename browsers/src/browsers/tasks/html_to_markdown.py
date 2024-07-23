
from temporalio import activity
import re

def markdown_strip_spaces(markdown):
    COUNT = 99999

    def clean_init(markdown):
        markdown = markdown.strip()
        markdown = "\n".join(p.strip() for p in markdown.splitlines())
        markdown = re.sub(r"[(.+)](.+)", r"\1", markdown)
        return markdown

    def clean_one(markdown):
        markdown = re.sub(' +', ' ', markdown, count=COUNT)
        markdown = re.sub('\n \n', '\n\n', markdown, count=COUNT)
        markdown = re.sub('\n\n\n+', '\n\n', markdown, count=COUNT)
        return markdown
    
    init_page = clean_init(markdown)
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
    from ...database import db_get_html, db_set_markdown

    html = db_get_html(url)
    assert html is not None, "no htmlm in db WTF??"
    page_markdown = markdownify(html)
    activity.logger.info("markdown convert OK")
    pre_len = len(page_markdown)
    page_markdown = markdown_strip_spaces(page_markdown)
    post_len = len(page_markdown)
    activity.logger.info("markdown strip whitespace: %s ---> %s", pre_len, post_len)
    db_set_markdown(url, page_markdown)

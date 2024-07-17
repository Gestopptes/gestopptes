from scrape import *


def example_alex_scrape_ceva():
    for obj in db_get_all_url():
        url = obj['url']
        html = db_get_html(url)
        assert html is not None, "no htmlm in db WTF??"
        print("before convert markdown: ", len(html), html[:100])
        page_markdown = html2markdown.convert(html)
        print("after convert markdown: ", len(page_markdown), page_markdown[:100])
        db_set_markdown(url, page_markdown)


        
if __name__ == "__main__":
    example_alex_scrape_ceva()

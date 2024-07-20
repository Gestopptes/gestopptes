from ..router import hd,router

import logging
log = logging.getLogger(__name__)
import json
from urllib.parse import urlparse

@router.route("/new-scrape")
def new_scrape_page():

    with hd.form() as form:
        hd.h3("scrape this url:")
        url =     form.text_input('url').value
        with hd.hbox(gap=3,):
            with hd.box(width="50%", height="100%", gap=1,):
                # hd.text(str(url))

                hd.h3("follow links only in same domain?")
                same_domain = form.checkbox("follow same domain").value
                # hd.text(str(same_domain))

                hd.h3("follow only link urls matching regex")
                url_filter_regex = form.text_input("regex").value
                # hd.text(str(url_filter_regex))
                
                hd.h3("follow links matching this css selector")
                link_class = form.text_input("css selector").value or None

                hd.h3("follow only links with these domains")
                allow_domain_list = form.text_input("filter domains  (comma spearated").value
                # hd.text(str(allow_domain_list))

                # hd.text(str(reject_domain_list))

            with hd.box(width="50%", height="100%", gap=1,):
                hd.h3("reject links with these domains")
                reject_domain_list = form.text_input("reject domains  (comma spearated").value
                hd.h3("max depth")
                with hd.hbox(gap=2):
                    max_depth = int(form.slider(
                        'max depth',
                        min_value=1,
                        max_value=5,
                        step=1,
                        value=1,
                    ).value)
                    hd.text(str(max_depth))

                hd.h3("scrape options json")
                scrape_options = dict(
                    url=url,
                    same_domain=same_domain,
                    allow_domain_list=[x.strip() for x in allow_domain_list.split(",") if x.strip()],
                    reject_domain_list=[x.strip() for x in reject_domain_list.split(",") if x.strip()],
                    url_filter_regex=url_filter_regex or None,
                    max_depth=max_depth or 1,
                    link_class=link_class or None,
                )

                hd.code(f"""\n{json.dumps(scrape_options,indent=2)}\n""",language="json")

    task = hd.task()
    
    validated = False
    try:
        validate_scrape_options(scrape_options)
        validated = True
    except Exception as e:
        hd.h3("Validation error")
        hd.markdown(f"```\n{str(e)}\n```")
        return

    hd.h3("Submit")
    if hd.button("Start", disabled=not validated).clicked:
        from src.workflows.scrape import execute_scrape
        task.rerun(execute_scrape, url, scrape_options)
    
    if task.running:
        hd.h3("Running...")
        hd.spinner()
    elif task.done:
        hd.h3("Result")
        hd.text("result: " +str(task.result))


def validate_scrape_options(options):
    import validators
    _url_parsed = urlparse(options['url'])
    if _url_parsed.scheme != "https":
        raise ValueError("need url starting with https")
    if not validators.domain(_url_parsed.netloc):
        raise ValueError(f"invalid url domain: '{_url_parsed.netloc}'")
    for domtype in ['allow_domain_list', 'reject_domain_list']:
        for d in options[domtype]:
            if not validators.domain(d):
                raise ValueError(f"invalid domain listed in {domtype}: {d}")
    if options['url_filter_regex']:
        import re
        re.compile(options['url_filter_regex'])
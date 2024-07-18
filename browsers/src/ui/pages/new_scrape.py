from ..router import hd,router

import logging
log = logging.getLogger(__name__)

@router.route("/new-scrape")
def new_scrape_page():

    with hd.form() as form:
        with hd.hbox():
            with hd.box(width="50%", height="100%"):
                hd.h3("url:")
                url =     form.text_input('url').value
                hd.text(str(url))

                hd.h3("filter only same domain?")
                same_domain = form.checkbox("filter same domain").value
                hd.text(str(same_domain))

                hd.h3("Accepted domamins (ccomma spearated):")
                accepted_domain_list = form.text_input("accept domains ").value
                hd.text(str(accepted_domain_list))

                hd.h3("Url Regex")
                endpoint_regex = form.text_input("regex").value
                hd.text(str(endpoint_regex))
            with hd.box(width="50%", height="100%"):
                hd.h3("max depth")
                max_depth = int(form.slider(
                    'max depth',
                    min_value=1,
                    max_value=5,
                    step=1,
                    value=3,
                ).value)
                hd.text(str(max_depth))

                hd.h3("css link selector")
                link_class = form.text_input("css selectors").value or None
                hd.text(str(link_class))

                hd.markdown(f"""``` 
url = "{url}"
same_domain = "{same_domain}"
accepted_domain_list = "{accepted_domain_list}"
endpoint_regex = "{endpoint_regex}"
max_depth = "{max_depth}"
link_class = "{link_class}"
                        ```""")

    task = hd.task()
    if hd.button("Start").clicked:
        from src.workflows.scrape import execute_scrape
        task.rerun(execute_scrape, url, max_depth, link_class)
    
    if task.running:
        hd.spinner()
    elif task.done:
        hd.text("result:; "+str(task.result))
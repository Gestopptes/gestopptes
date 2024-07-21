from ..router import hd,router
from ...database import db_get_markdown, db_get_all_urls
@router.route("/new_datasource")
def new_datasource():    
    all_urls = db_get_all_urls()
    hd.h3("new data from url:")
    with hd.select(placeholder="Choose URl") as select:
        for i, a in enumerate(all_urls):
            with hd.scope(i):
                hd.option(a)
    url = select.value
    with hd.form() as form:
        # url =     form.text_input('url').value

        with hd.hbox(gap=3,):
            with hd.box(width="50%", height="100%", gap=1,):
                hd.h3("follow links only in same domain?")
                model = form.text_input("model").value

    validated = False
    try:
        md = db_get_markdown(url)
        options = {
            "url": url,
            "model": model,

        }
        assert md, "no markdown for url!"
        validated = True
    except Exception as e:
        hd.text(str(e))
    
    task = hd.task()
    hd.h3("Submit")
    if hd.button("Start", disabled=not validated).clicked:
        
        from src.workflows.lama_index import execute_lama
        task.rerun(execute_lama, url, options)

    
    if task.running:
        hd.h3("Running...")
        hd.spinner()
    elif task.done:
        hd.h3("Result")
        hd.text("result: " +str(task.result))

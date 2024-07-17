import hyperdiv as hd


def main():
    from scrape import db_get_all_url
    screenshots = db_get_all_url()

    template = hd.template(title="Image Editor", sidebar=False)
    with template.body:
        for i, data in enumerate(screenshots):
            with hd.scope(i):
                # Render the side by side images
                with hd.hbox():
                    with hd.box(width="50%", gap=1):
                        hd.h1("Link")
                        hd.link(data['url'], href= data['url'])


                        hd.h1("HTMML")
                        hd.code(data.get("html",'html') ,language="markdown")

                        hd.h1("Markdown")
                        hd.code(data.get("markdown",'') ,language="markdown")
                    with hd.box(width="50%", gap=1):
                        hd.image(data['png'])

hd.run(main)
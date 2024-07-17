import hyperdiv as hd


def main():
    from scrape import db_get_all_screenshot
    screenshots = db_get_all_screenshot()

    template = hd.template(title="Image Editor", sidebar=False)
    with template.body:
        for i, data in enumerate(screenshots):
            with hd.scope(i):
                # Render the side by side images
                with hd.hbox():
                    with hd.box(width="50%", gap=1):
                        hd.h1(data['url'])
                        hd.link(data['url'], href= data['url'])
                    with hd.box(width="50%", gap=1):
                        hd.image(data['png'])

hd.run(main)
import hyperdiv as hd
from ..router import router

from ..comp import pre, overflow_box


@router.route("/original-demo")
def orig_demo():
    from src.database import db_get_all_blogpost_data
    screenshots = db_get_all_blogpost_data()

    for i, data in enumerate(screenshots):
        with hd.scope(i):
            # Render the side by side images
            with hd.hbox(border="3px solid #000" ):
                with hd.box(width="50%", gap=1, height="768px"):
                    with hd.box(
                        width="90%",
                        height="90%",
                        border="1px solid yellow",
                        background_color="yellow-50",
                        border_radius=1,
                        # align="center",
                        # justify="center",
                    ):
                        hd.h1(f"Link {i}")
                        hd.link(data['url'], href=data['url'])

                        # hd.h1("HTMML")
                        # hd.code(data.get("html",'html') ,language="markdown")

                        hd.h2("Markdown")
                        with overflow_box(height="80%",  width="100%", overflow="scroll", padding="10px", margin="10px"):
                            with pre(background_color="#eee"):
                                with hd.box(gap=1):
                                    hd.text(data.get("markdown",''))
                            
                        # with hd.box(height="50%",  width="100%"):
                            # hd.code(data.get("markdown",'') ,language="markdown")
                with hd.box(
                        width="50%", gap=1, height="768px",
                        align="center",
                        justify="center",):
                    hd.image(data['png'], width="100%")
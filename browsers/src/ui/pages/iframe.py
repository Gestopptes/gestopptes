import os
from ...config import IFRAME_IP
from ..router import hd,router

class iframe(hd.Component, hd.Styled):
    _tag = "iframe"
    src = hd.Prop(hd.PureString)
    width = hd.Prop(
        hd.CSSField(
            "width",
            hd.Optional(hd.PureString)
        ),
        None
    )
    height = hd.Prop(
        hd.CSSField(
            "height",
            hd.Optional(hd.PureString)
        ),
        None
    )

IFRAME_PORTS = [8080, 8081, 4444]


for portno in IFRAME_PORTS:
    link = f"/iframe/{portno}"
    src = f"http://{IFRAME_IP}:{portno}"
    @router.route(link)
    def iframe_page(src=src):
        iframe(src=src, width="100%", height="100%")

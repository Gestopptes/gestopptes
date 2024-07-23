import os
from ...config import IFRAME_IP, LAMAINDEX_HOST
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

IFRAME_PORTS = [8080, 8081, 4444, 11434, 8082, 3000, 8083]


for portno in IFRAME_PORTS:
    link = f"/iframe/{portno}"
    ip = IFRAME_IP if portno != 11434 else LAMAINDEX_HOST
    src = f"http://{ip}:{portno}"
    if portno == 3000:
        src += r'/d/loki-containers-dashboard/logs-container?orgId=1'
    elif portno == 11434:
        src += r'/api/tags'
    @router.route(link)
    def iframe_page(src=src):
        hd.link("Original page: " + src, href=src)
        iframe(src=src, width="100%", height="100%")

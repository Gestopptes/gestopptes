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

IFRAME_PORTS = [8080, 8081, 4444, 11434, 8082, 3000]


for portno in IFRAME_PORTS:
    link = f"/iframe/{portno}"
    ip = IFRAME_IP if portno != 11434 else LAMAINDEX_HOST
    src = f"http://{ip}:{portno}"
    if portno == 3000:
        src += r'/explore?schemaVersion=1&panes={"5oy"%3A{"datasource"%3A"P8E80F9AEF21F6940"%2C"queries"%3A[{"refId"%3A"A"%2C"expr"%3A""%2C"queryType"%3A"range"%2C"datasource"%3A{"type"%3A"loki"%2C"uid"%3A"P8E80F9AEF21F6940"}}]%2C"range"%3A{"from"%3A"now-1h"%2C"to"%3A"now"}}}&orgId=1'
    @router.route(link)
    def iframe_page(src=src):
        hd.link("Original page: " + src, href=src)
        iframe(src=src, width="100%", height="100%")

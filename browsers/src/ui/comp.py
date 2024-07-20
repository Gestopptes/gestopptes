import hyperdiv as hd


class overflow_box(hd.box):
    overflow = hd.Prop(
        hd.CSSField(
            "overflow",
            hd.Optional(hd.String)
        ),
        None
    )
    

class pre(hd.Component, hd.Styled):
    _tag = "pre"
    
    background_color = hd.Prop(
        hd.CSSField(
            "background-color",
            hd.Optional(hd.String)
        ),
        None
    )
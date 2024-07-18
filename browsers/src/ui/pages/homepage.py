from ..router import hd,router

@router.route("/")
def homepage():
    hd.text("homepage")
from ..router import hd,router

@router.route("/view-scrapes")
def view_scrapes():
    hd.text("view scrapes")
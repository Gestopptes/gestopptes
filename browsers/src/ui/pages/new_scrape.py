from ..router import hd,router

@router.route("/new-scrape")
def new_scrape_page():
    hd.text("new scrape")
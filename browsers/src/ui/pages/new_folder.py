from ..router import hd,router
from ...database import MONGO_CLIENT
import pymongo

MONGO_DB = MONGO_CLIENT["GESTOPPTES_FOLDERS"]
MONGO_COL = MONGO_DB["FOLDERS1"]


MONGO_COL.create_index([("folder_name", pymongo.ASCENDING)],unique=True)

@router.route("/new-folder")
def new_folder():
    hd.text("create new falder")
    input = hd.text_input(placeholder="Enter Some Text") 
    x = input.value
    if len(x)<3:
        hd.text(",,,")
    elif MONGO_COL.find_one({"folder_name":x}):
        hd.text("ALREADY IN DB")
    elif hd.button(f"Create Folder:{x}").clicked:
        MONGO_COL.insert_one({"folder_name":x})
        input.value = ""
    for (i,folder) in enumerate(MONGO_COL.find()):
        with hd.scope(i):
            display_folder(folder)

def display_folder(folder):
    loc = hd.location()
    name = folder["folder_name"]
    hd.h3(name)
    hd.text(str(folder))
    with hd.hbox(gap=1):
        if hd.button("delete").clicked:
            MONGO_COL.delete_one({"folder_name":name})
        # hd.button("edit")
        if hd.button("view").clicked:
            loc.go(f"/folder/{name}")

import pymongo
from pymongo.errors import DuplicateKeyError
import logging
log = logging.getLogger(__name__)

from .config import MONGO_HOSTNAME

MONGO_CLIENT = pymongo.MongoClient(MONGO_HOSTNAME, 27017,username="root", password="example")
MONGO_DB = MONGO_CLIENT['GESTTOPTEZ']
MONGO_COL_BLOG_POST = MONGO_DB["blog_post"]

MONGO_COL_BLOG_POST_EMBEDDINGS = MONGO_DB["blog_post_EMBEDDINGS"]


def init_mongo():
    dblist = MONGO_CLIENT.list_database_names()
    MONGO_COL_BLOG_POST.create_index("url", unique=True)
    print("mongo dblist: ", str(dblist))


def db_get_html(url):
    x = MONGO_COL_BLOG_POST.find_one({"url": url})
    if x:
        return x['html']


def db_save_html_and_pic(url, html, png):
    try:
        MONGO_COL_BLOG_POST.insert_one({"url": url, "html": html, "png": png})
    except DuplicateKeyError:
        log.warn("tried to insert duplicate key: %s", url)


def db_get_markdown(url):
    x = MONGO_COL_BLOG_POST.find_one({"url": url, "markdown": {"$exists":True}})
    if x:
        return x.get('markdown')


def db_set_markdown(url, markdown):
    MONGO_COL_BLOG_POST.update_one({"url": url}, {"$set": {"markdown":markdown}})


def db_get_screenshot(url):
    x = MONGO_COL_BLOG_POST.find_one({"url": url})
    if x:
        return x['png']


def db_get_all_url():
    return MONGO_COL_BLOG_POST.find()

from ..router import hd,router
from ..comp import pre
import pymongo
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.route("/llm-proxy-scan")
def llm_proxy_scan():
    MONGO_HOSTNAME = "100.66.129.30"
    import json
    MONGO_CLIENT = pymongo.MongoClient(MONGO_HOSTNAME, 27017,username="root", password="example")
    MONGO_DB = MONGO_CLIENT['LLM_HTTP_CACHE']
    MONGO_COL = MONGO_DB["LLM_HTTP_CACHE"]

    for i, x in enumerate(MONGO_COL.find()):
        hd.scope(i)
        llm_cache_row_display(x)


def llm_cache_row_display(x):
    with pre():
        hd.h3(x['key'])
        hd.text(pretty_print(x.get('args_str', '')))

def pretty_print(x):
    import json
    return json.dumps(x, indent=2)    

def pretty_print_dict(x):
    if isinstance(x, dict):
        return {
            pretty_print_dict(k):pretty_print_dict(v)
            for k, v in x.items()
        }
    if isinstance(x, list):
        return [
            pretty_print_dict(i)
            for i in x
        ]
    if isinstance(x, str):
        return x
    return str(x)
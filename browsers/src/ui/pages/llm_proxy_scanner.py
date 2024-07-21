from ..router import hd,router
from ..comp import pre
import pymongo
import logging
import pickle
import json
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
        with hd.scope(i):
            with hd.box(width="100%"):
                llm_cache_row_display(x)


def llm_cache_row_display(x):
    with pre():
        hd.h3("key: " + x['key'])
        hd.text(x.get('args_str', ''))
        if x.get("args_pickle"):
            hd.h5("args:")
            args = pickle.loads(x.get("args_pickle"))
            args, content = pretty_print(args)
            hd.text(args)
            with hd.box(width="80%", border="3px solid green"):
                hd.markdown(content)
        if x.get("key_args_pickle"):
            hd.h5("key args:")
            args = pickle.loads(x.get("key_args_pickle"))
            args,content = pretty_print(args)
            hd.text(args)
            with hd.box(width="80%", border="3px solid green"):
                hd.markdown(content)

def pretty_print(x):
    try:
        x['data'] = json.loads( x['data'])
        content = x['data']['messages'][0]['content']
    except:
        content = ''
    return (json.dumps(pretty_print_dict(x), indent=2) , content)

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
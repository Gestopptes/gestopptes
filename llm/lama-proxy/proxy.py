import os

import pymongo
from pymongo.errors import DuplicateKeyError
import logging
import pickle
import hashlib
#
from flask import request, Response
import requests  # pip package requests

MONGO_HOSTNAME = "100.66.129.30"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
import json

MONGO_CLIENT = pymongo.MongoClient(MONGO_HOSTNAME, 27017,username="root", password="example")
MONGO_DB = MONGO_CLIENT['LLM_HTTP_CACHE']
MONGO_COL = MONGO_DB["LLM_HTTP_CACHE"]


def init_mongo():
    dblist = MONGO_CLIENT.list_database_names()
    MONGO_COL.create_index("url", unique=True)
    print("mongo dblist: ", str(dblist))


def db_get(key):
    return MONGO_COL.find_one({"key": key})


def db_set(key, val, args_str):
    try:
        MONGO_COL.insert_one({"key": key, "val": val, "args_str": args_str})
    except DuplicateKeyError:
        pass


API_HOST = "http://"+MONGO_HOSTNAME+":11436"

from flask import Flask

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=["GET", "POST"])  # ref. https://medium.com/@zwork101/making-a-flask-proxy-server-online-in-10-lines-of-code-44b8721bca6
@app.route('/<path:path>', methods=["GET", "POST"])  # NOTE: better to specify which methods to be accepted. Otherwise, only GET will be accepted. Ref: https://flask.palletsprojects.com/en/3.0.x/quickstart/#http-methods
def redirect_to_API_HOST(path):  #NOTE var :path will be unused as all path we need will be read from :request ie from flask import request

    args = dict(  # ref. https://stackoverflow.com/a/36601467/248616
        method          = request.method,
        url             = request.url.replace(request.host_url, f'{API_HOST}/'),
        headers         = {k:v for k,v in request.headers if k.lower() != 'host'}, # exclude 'host' header
        data            = request.get_data(),
        cookies         = request.cookies,
        allow_redirects = False,
    )
    args_txt = repr(args)
    log.info("got request: %s", args_txt)
    args_for_key = dict(args)
    del args_for_key['headers']
    del args_for_key['cookies']
    args_key = hashlib.md5(pickle.dumps(args_for_key)).hexdigest()
    if cached:= db_get(args_key):
        log.warning("CACHE HIT")
        val = cached['val']
        (content, status_code, headers) = pickle.loads(val)
        response = Response(content, status_code, headers)
        return response

    log.warning("CACHE MISS")
    res = requests.request(**args)

    #region exlcude some keys in :res response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']  #NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
    headers          = [
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]
    #endregion exlcude some keys in :res response

    to_cache = (res.content, res.status_code, headers)
    to_cache = pickle.dumps(to_cache)
    
    log.warning("CACHE SET")
    db_set(args_key, to_cache, args_txt)
    response = Response(res.content, res.status_code, headers)
    
    return response
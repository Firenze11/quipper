# Elasticsearch API docs: https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/index-data/

import os
import sys
# for debugging
if __name__ == "__main__":
    PACKAGE_PARENT = ".."
    SCRIPT_DIR = os.path.dirname(__file__)
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import boto3
import glob
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth
from ..parse_subtitles import parse_file


host = "search-quipper-6ee3qc46mosso4nnnkokssftsa.us-west-1.es.amazonaws.com"  # without "https://"
region = "us-west-1"
subtiltes_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../data"))
subtilte_suffix = "srt"


def init_es_service():
    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token,
    )

    es = Elasticsearch(
        hosts=[{"host": host, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    return es


def gen_actions(movie_id, subtitle_path, es_index="subtitles"):
    title = get_movie_title(movie_id)

    for subtitle in parse_file(subtitle_path, parse_time=False):
        _id = str(movie_id) + "_" + str(subtitle.ind)
        res = {
            "_index": es_index,
            "_id": _id,
            "_op_type": "index",
            "title": title,
            "start_time": subtitle.time_range[0],
            "end_time": subtitle.time_range[1],
            "text": subtitle.sentence,
        }
        yield res


def get_movie_title(movie_id):
    return "Into the Spider-Verse"


def ingest(directory=None):
    es = init_es_service()

    for filepath in glob.iglob(f"{directory}/**/*.{subtilte_suffix}", recursive=True):
        # todo: assign a movie_id to each movie
        movie_id = 1
        bulk(client=es, actions=gen_actions(movie_id, filepath, es_index="subtitles"))

    print(es.search(q="spider I mean"))


if __name__ == "__main__":
    ingest(subtiltes_dir)

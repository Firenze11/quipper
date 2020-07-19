import functools
import subprocess

from flask import Blueprint, request, session, url_for, send_from_directory

# from backend.db import get_db

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/health")
def health():
    return "OK"


@bp.route("/subtitles/")
def get_subtiles():
    movie_id = request.args.get("movie_id", "")
    print(movie_id)
    return "Hello World!"


@bp.route("/")
def hello():
    return "Hello Noah aaa"

@bp.route('/api/cut')
def cut():
    try:
        start = request.args['start']
        end = request.args['end']
    except KeyError:
        return '400'
    if invalid_timestamp(start) or invalid_timestamp(end):
        return '400'

    subprocess.run(["/run.sh", start, end])
    return send_from_directory("/data", "cut.gif")
    # return 200 with output url

@bp.route('/cut_links')
def cut_links():
    timestamps = [
        ['00:01:19.193', '00:01:23.463', 'my name is peter parker'],
        ['00:02:28.162', '00:02:33.798', "there's only one spider-man"],
        ['00:06:16.724', '00:06:23.828', 'i love you, dad']
    ]
    links = []
    for ts in timestamps:
        links.append('<div><a href="/api/cut?start={}&end={}">{}</a></div>'.format(*ts))
    return '<body>\n' + '\n'.join(links) + '</body>'

def invalid_timestamp(ts):
    return False
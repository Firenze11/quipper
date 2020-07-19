import functools
import subprocess
import re
from datetime import timedelta
from os import path

from flask import Blueprint, request, session, url_for, send_from_directory

from .parse_subtitles import start_subs_at

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

    movie_filepath = '/data/Spider-Man.Into.The.Spider-Verse.mp4'
    orig_subs_filepath = '/data/Spider-Man.Into.The.Spider-Verse.srt'
    trunc_subs_filepath = '/data/Spider-Man.Into.The.Spider-Verse-{}.srt'.format(make_path_friendly(start))
    out_path = '/data/out/spider-verse.{}.{}.gif'.format(make_path_friendly(start), make_path_friendly(end))

    start_subs_at(orig_subs_filepath, trunc_subs_filepath, parse_timestamp(start))

    subprocess.Popen(["/backend/cut.sh", movie_filepath, trunc_subs_filepath, start, end, out_path])
    return 'http://0.0.0.0:5000/out/' + path.basename(out_path)

@bp.route('/out/<filename>')
def out(filename):
    if path.exists(path.join('/data/out', filename)):
        return send_from_directory('/data/out', filename)
    else:
        return 'processing...'

RE_TIMESTAMP = "^(\d{2}):(\d{2}):(\d{2}).(\d{3})$"
def parse_timestamp(time_str):
    match = re.match(RE_TIMESTAMP, time_str)
    return timedelta(
        hours=int(match.group(1)),
        minutes=int(match.group(2)),
        seconds=int(match.group(3)),
        milliseconds=int(match.group(4))
    )


def format_timestamp_for_filepath(td):
    return make_path_friendly(str(td)[0:-3])

def make_path_friendly(s):
    return s.replace(':', '-').replace('.', '-')

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
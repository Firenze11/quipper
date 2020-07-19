import functools
from flask import Blueprint, request, session, url_for, jsonify
from .parse_subtitles import parse_file

import pathlib

# from backend.db import get_db

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/health")
def health():
    return "OK"


@bp.route("/subtitles/")
def get_subtiles():
    print(pathlib.Path(__file__).parent.absolute())

    print(pathlib.Path().absolute())
    print('aaaaaaaaa')

    movie_id = request.args.get("movie_id", "")
    # subtitles = parse_file(filepath)
    filepath = "/Users/lezhili/work/quipper/data/Spider-Man.Into.the.Spider-Verse.2018.720p.BluRay.x264-SPARKS.srt"
    return jsonify([list(st_record) for st_record in parse_file(filepath)])


@bp.route("/")
def hello():
    return "Hello Noah"


@bp.route("/api/cut")
def cut():
    return "ok i will cut next time"


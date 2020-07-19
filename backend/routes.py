import functools
from flask import Blueprint, request, session, url_for, jsonify
from .parse_subtitles import parse_file, format_time

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

    movie_id = request.args.get("movie_id", "")
    # subtitles = parse_file(filepath)
    filepath = "/data/Spider-Man.Into.the.Spider-Verse.2018.720p.BluRay.x264-SPARKS.srt"

    return jsonify(
        [
            [[format_time(timerange[0]), format_time(timerange[1])], sentence]
            for (ind, timerange, sentence) in parse_file(filepath)
        ]
    )


@bp.route("/")
def hello():
    return "Hello Noah"


@bp.route("/api/cut")
def cut():
    return "ok i will cut next time"

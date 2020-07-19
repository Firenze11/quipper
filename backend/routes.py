import functools

from flask import Blueprint, request, session, url_for

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


@bp.route("/api/cut")
def cut():
    return "ok i will cut next time"


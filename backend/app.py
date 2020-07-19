from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/health')
def health():
    return 'OK'


@app.route("/subtitles/")
def get_subtiles():
    movie_id = request.args.get("movie_id", "")
    print(searchword)
    return "Hello World!"


@app.route("/")
def hello():
    return 'Hello Noah'

@app.route('/api/cut')
def cut():
    return 'ok i will cut next time'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

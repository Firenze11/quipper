import subprocess
import os
from flask import Flask, send_from_directory, request

app = Flask(__name__)


@app.route('/health')
def health():
    return 'OK'


@app.route('/')
def hello():
    return 'Hello Noah'

@app.route('/api/cut')
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

@app.route('/cut_links')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import json
import os
from flask import (
    render_template, Blueprint, request, redirect, url_for
)
from graphy.graph import build_graph

bp = Blueprint('hello', __name__, url_prefix='/hello')


@bp.route('/', methods=['GET', 'POST'])
def render_hello():
    data_dir = os.path.join('graphy', 'static', 'data')
    build_graph_to_json()
    with open(os.path.join(data_dir, 'graph.json')) as f:
        graph_data = json.load(f)

    return render_template('hello/hello.html', json_data=graph_data)


def build_graph_to_json():
    print("building new graph")
    graph = build_graph()
    graph.write_json()

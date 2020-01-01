import json
import os
from flask import (
    render_template, Blueprint
)

bp = Blueprint('hello', __name__, url_prefix='/hello')


@bp.route('/')
def render_hello():
    data_dir = os.path.join('graphy', 'static', 'data')
    with open(os.path.join(data_dir, 'sample_data.json')) as f:
        graph_data = json.load(f)

    return render_template('hello/hello.html', json_data=graph_data)

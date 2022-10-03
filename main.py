import flask
import json
app = flask.Flask(__name__)


EASY_GRID = {
    'width': 3,
    'height': 3,
    'grid': [
        [{'down': 0, 'draw': True, 'right': 2},
         {'down': 0, 'draw': True, 'right': 0},
         {'down': None, 'draw': True, 'right': 3}],
        [{'down': 0, 'draw': True, 'right': 0},
         {'down': 0, 'draw': True, 'right': None},
         {'down': None, 'draw': True, 'right': 0}],
        [{'down': 1, 'draw': True, 'right': None},
         {'down': 0, 'draw': True, 'right': None},
         {'down': None, 'draw': True, 'right': None}]
    ]
}

HARD_GRID = {
    'width': 4,
    'height': 3,
    'grid': [
        [{'right': 1, 'down': 0, 'draw': True},
         {'right': 1, 'down': 0, 'draw': True},
         {'right': 0, 'down': None, 'draw': True}],
        [{'right': 2, 'down': 0, 'draw': True},
         {'right': None, 'down': 0, 'draw': True},
         {'right': 2, 'down': None, 'draw': True}], 
        [{'right': 2, 'down': None, 'draw': True},
         {'right': None, 'down': None, 'draw': None},
         {'right': 2, 'down': None, 'draw': True}],
        [{'right': None, 'down': 2, 'draw': True},
         {'right': None, 'down': 0, 'draw': True},
         {'right': None, 'down': None, 'draw': True}]
    ]
}

def make_response(dct: dict, status: int):
    result = flask.jsonify(dct)
    result.status = status
    return result


@app.route('/v1/demo_grid', methods=['POST'])
def create_grid():
    data = flask.request.json
    if 'difficulty' not in data:
        return make_response({'error': 'no_difficulty', 'result': None}, 400)
    try:
        difficulty = float(data['difficulty'])
    except ValueError:
        return make_response({'error': 'wrong_difficulty', 'result': None}, 400)
    if difficulty > 0.5:
        return {'error': None, 'result': 2}
    else:
        return {'error': None, 'result': 1}


@app.route('/v1/demo_grid/<grid_id>')
def get_grid(grid_id):
    try:
        grid_id = int(grid_id)
    except ValueError:
        return make_response({'error': 'wrong_id', 'result': None}, 400)
    if grid_id == 1:
        return {'error': None, 'result': EASY_GRID}
    elif grid_id == 2:
        return {'error': None, 'result': HARD_GRID}
    else:
        return make_response({'error': 'not_found', 'result': None}, 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9896)

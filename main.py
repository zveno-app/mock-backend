import copy
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

EASY_TASK = copy.deepcopy(EASY_GRID)
EASY_TASK['grid'][1][1]['down'] = -1
EASY_ANS = 0.75

HARD_TASK = copy.deepcopy(HARD_GRID)
HARD_TASK['grid'][2][0]['right'] = -1
HARD_ANS = 8


def make_response(dct: dict, status: int):
    result = flask.jsonify(dct)
    result.status = status
    return result


@app.route('/v1/<endpoint>', methods=['POST'])
def create_grid(endpoint: str):
    if endpoint not in ['demo_grid', 'task']:
        return make_response('route not found', 404)
    data = flask.request.json
    if 'difficulty' not in data:
        return make_response({'error': 'no_difficulty', 'result': None}, 400)
    try:
        difficulty = float(data['difficulty'])
        if not 0 <= difficulty <= 1:
            raise ValueError
    except ValueError:
        return make_response({'error': 'wrong_difficulty', 'result': None}, 400)
    if difficulty > 0.5:
        return {'error': None, 'result': 2}
    else:
        return {'error': None, 'result': 1}


@app.route('/v1/<endpoint>/<grid_id>')
def get_grid(endpoint, grid_id):
    if endpoint not in ['demo_grid', 'task']:
        return make_response('route not found', 404)
    try:
        grid_id = int(grid_id)
    except ValueError:
        return make_response({'error': 'wrong_id', 'result': None}, 400)
    if grid_id == 1:
        return {'error': None, 'result': EASY_GRID if endpoint == 'demo_grid' else EASY_TASK}
    elif grid_id == 2:
        return {'error': None, 'result': HARD_GRID if endpoint == 'demo_grid' else HARD_TASK}
    else:
        return make_response({'error': 'not_found', 'result': None}, 404)


@app.route('/v1/task/<grid_id>/check')
def check_task(grid_id):
    try:
        grid_id = int(grid_id)
    except ValueError:
        return make_response({'error': 'wrong_id', 'result': None}, 400)
    try:
        ans = float(flask.request.args['answer'])
    except KeyError:
        return make_response({'error': 'no_answer', 'result': None}, 400)
    except ValueError:
        return make_response({'error': 'wrong_answer', 'result': None}, 400)
    if 1 <= grid_id <= 2:
        return {'error': None, 'result': (EASY_ANS if grid_id == 1 else HARD_ANS) == ans}
    else:
        return make_response({'error': 'not_found', 'result': None}, 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9896)

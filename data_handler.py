import json
import pathlib


def load_data():
    if not pathlib.Path('data.json').exists():
        with open('data.json', 'w') as f:
            json.dump({'sets': {}, 'data': []}, f)

    with open('data.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {'sets': {}, 'data': []}

    return data


def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

import json
import pickle
import pathlib


def load_data():
    if not pathlib.Path('data.pickle').exists():
        with open('data.pickle', 'wb') as f:
            data = {'sets': {}, 'data': []}
            pickle.dump(data, f)
    else:
        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)

    return data


def save_data(data):
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)

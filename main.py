from gui import create_gui
from data_handler import load_data


def main():
    data = load_data()
    create_gui(data)


if __name__ == '__main__':
    main()

    # pathlib.Path('data.json').unlink()

from .parameters import DATA_PATH


def delete_data():
    for file_ in DATA_PATH.rglob("*"):
        if file_.is_dir():
            continue
        file_.unlink()

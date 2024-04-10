import os


def get_r_file_path(fpath: str) -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        fpath,
    )

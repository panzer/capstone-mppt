import os.path

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(ROOT_PATH, "output")


def get_output_path(filename: str):
    return os.path.join(OUTPUT_PATH, filename)

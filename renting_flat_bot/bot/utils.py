import httpx
import os
from pathlib import Path


def write_data(data, file_name="result", extension="html", folder_name="data"):
    _BASE_DIR = Path(__file__).parent
    data_folder_exists = os.path.exists(str(_BASE_DIR) + "/data")
    full_file_name = f"{file_name}.{extension}"
    file_path = f"{_BASE_DIR}/{folder_name}"

    if not data_folder_exists:
        os.mkdir(file_path)

    with open(f"{file_path}/{full_file_name}", "w") as fle:
        fle.write(data)


def get_data(url, generate_html_file=False):
    response = httpx.get(url)

    if not response.status_code == 200:
        return None

    to_html = str(response.content, encoding="utf8")

    if generate_html_file:
        write_data(to_html)

        # with open("./data/result.html", "at") as fle:
        # fle.write(to_html)

    return to_html

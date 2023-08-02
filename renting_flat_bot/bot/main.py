import os
import subprocess
import time
import re

import httpx

from pathlib import Path

from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    URL = "https://www.ouestfrance-immo.com/immobilier/location/appartement/rennes-35-35238/"
    HTML_PARSER = "html.parser"

    html = get_data(URL, generate_html_file=False)
    soup = BeautifulSoup(html, HTML_PARSER)

    announce_div = soup.find("div", id="listAnnonces")
    announces = announce_div.find_all(
        "div", id=lambda value: value and value.startswith("annonce_")
    )
    announces_str = ""
    price_list = []

    for announce in announces:
        imgs = announce.find_all("img")
        prices = announce.find_all("span", class_="annPrix")

        for price in prices:
            cleared_prices = re.sub("[^0-9]", "", price.getText(strip=True))
            price_list.append(int(cleared_prices))

        # for img in imgs:
        #     subprocess.run(["explorer.exe", str(img.get("data-original"))])
        #     time.sleep(1)
        # print(img.get("data-original"))
        # annonces_str += str(annonce)

    price_list.sort()

import os
import subprocess
import time
import json
import re

import httpx

from pathlib import Path

from bs4 import BeautifulSoup

URL = (
    "https://www.ouestfrance-immo.com/immobilier/location/appartement/rennes-35-35238/"
)
HTML_PARSER = "html.parser"


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


def bot():
    html = get_data(URL, generate_html_file=False)
    soup = BeautifulSoup(html, HTML_PARSER)

    announce_div = soup.find("div", id="listAnnonces")
    announces = announce_div.find_all(
        "div", id=lambda value: value and value.startswith("annonce_")
    )

    criterias_str = ""
    price_list = []

    # data
    announce_data = {
        "price": 0,
        "href": "",
        "surface": "",
        "rooms": "",
        "bathrooms": "",
    }
    data = {"announces": []}

    for index, announce in enumerate(announces):
        prices = announce.find_all("span", class_="annPrix")
        criterias = announce.find_all("span", class_="annCriteres")

        for criteria in criterias:
            unit_span_sp = criteria.find_all(
                "span", class_=lambda value: value and value.startswith("unit")
            )
            criterias_str += str(criteria.prettify())
            values = criteria.find_all("div")

            # print(criteria.find_all("span", class_="unit"))

            # for unit_sp in unit_span_sp:
            #     print(unit_sp.parent)

            # print(values)

        for price in prices:
            cleared_price = int(re.sub("[^0-9]", "", price.getText(strip=True)))
            price_list.append(int(cleared_price))

    for price in price_list:
        announce_data["price"] = price
        data["announces"].append({**announce_data})
        # not working, I don't know why
        # data["announces"].append(announce_data)


if __name__ == "__main__":
    bot()

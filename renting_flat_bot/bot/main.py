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
URL_WITH_FILTERS = "https://www.ouestfrance-immo.com/louer/appartement/rennes-35-35000/?tri=PRIX_CROISSANT&surface=30_0&colocation=0"
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
    html = get_data(URL_WITH_FILTERS, generate_html_file=False)
    soup = BeautifulSoup(html, HTML_PARSER)

    announce_div = soup.find("div", id="listAnnonces")
    announces = announce_div.find_all(
        "div", id=lambda value: value and value.startswith("annonce_")
    )

    announces_str = ""
    announce_parent_str = ""
    prices_str = ""

    # data
    announce_data = {
        "price": 0,
        "href": "",
        "surface": 0,
        "rooms": 0,
        "bathrooms": 0,
    }
    data = {"announces": []}

    for announce in announces:
        announce_parent_str += str(announce.parent)
        announces_str += str(announce)
        cleared_price = 0
        sq_meter = 0
        room = 0
        bathroom = 0

        prices_sp = announce.find_all("span", class_="annPrix")
        criterias_sp = announce.find_all("span", class_="annCriteres")

        # setting prices
        for price_sp in prices_sp:
            cleared_price = int(re.sub("[^0-9]", "", price_sp.getText(strip=True)))
            prices_str += str(cleared_price) + " €\n"

        # adding square meters, number of rooms, number of bathrooms
        for criteria_sp in criterias_sp:
            criteria_sp.find_all(
                "span", class_=lambda value: value and value.startswith("unit")
            )
            values = criteria_sp.find_all("div")

            for value in values:
                unit_span_sp = value.find("span", class_="unit")

                if unit_span_sp.text == "m²":
                    sq_meter = int(unit_span_sp.parent.next)

                if unit_span_sp.text == "chb" and unit_span_sp.parent.next:
                    room = int(unit_span_sp.parent.next)

                if unit_span_sp.text == "sdb" and unit_span_sp.parent.next:
                    bathroom = int(unit_span_sp.parent.next)

        # finally, modeling data
        announce_data["surface"] = sq_meter
        announce_data["price"] = cleared_price
        announce_data["rooms"] = room
        announce_data["bathrooms"] = bathroom
        data["announces"].append({**announce_data})

    # uncomment these lines, easy to debug
    write_data(json.dumps(data), file_name="data", extension="json")
    # write_data(prices_str, file_name="prices")


if __name__ == "__main__":
    bot()

import os
import subprocess

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

    # """Annonce sample. So, we have to extract those divs first."""
    # annonce_17133746 = soup.find_all(id="annonce_17133746")
    # for annonce in annonce_17133746:
    #     write_data(str(annonce), file_name="annonce_17133746")
    #     print(annonce)

    annonce_div = str(soup.find_all("div", id="listAnnonces")[0])
    annonce_div_soup = BeautifulSoup(annonce_div, HTML_PARSER)
    annonce_div_links = annonce_div_soup.find_all("a")
    links = ""

    for link in annonce_div_links:
        links += str(link)

    links_soup = BeautifulSoup(links, HTML_PARSER)
    # write_data(str(links_soup), file_name="links_soup")
    annonce_links = links_soup.find_all("a", class_="annLink")
    annonces = ""

    for annonce_link in annonce_links:
        annonces += str(
            annonce_link.find(
                "div", id=lambda value: value and value.startswith("annonce_")
            )
        )

    # write_data(annonces, file_name="annonces")

    annonces_soup = BeautifulSoup(annonces, HTML_PARSER)
    imgs = annonces_soup.find_all("img")

    # print(imgs[0]["data-original"])
    img_1_hrf = imgs[0]["data-original"]

    exit_code = subprocess.run(["explorer.exe", f"{img_1_hrf}"])
    print(exit_code)

    # subprocess.run("explorer.exe")

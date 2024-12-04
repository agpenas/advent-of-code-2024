import os
import re
from bs4 import BeautifulSoup as Soup
from urllib import request
import requests


def get_input_if_not_exists(year: int, dirname: str, level: int):
    day = get_current_day(dirname)
    if day == 0:
        return
    url = f"https://adventofcode.com/{year}/day/{day}/input"

    # Download the file from `url` and save it locally under `file_name`:
    file_name = url.split("/")[-1] + str(level) + ".txt"
    if os.path.exists(os.path.join(dirname, file_name)):
        print(f"{os.path.join(dirname, file_name)} already exists!")
        return

    r = request.Request(url)

    session = os.getenv("ADVENTOFCODE_SESSION")
    r.add_header("Cookie", f"session={session}")
    with request.urlopen(r) as response, open(
        os.path.join(dirname, file_name), "wb"
    ) as out_file:
        data = response.read()
        out_file.write(data)


def read_input_lines(filename: str):
    if not (os.path.exists(filename)):
        print("Input file not found when trying to read input lines!")
    with open(filename, "r") as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    return lines


def get_current_day(dirname: str):
    pattern = re.compile(r"day(\d+)")
    match = pattern.findall(dirname)
    if len(match) == 0:
        return 0
    return int(match[0])

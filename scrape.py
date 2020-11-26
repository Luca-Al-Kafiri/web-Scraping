import os
import sys
import datetime
from requests_html import HTML
import requests
import pandas as pd


BASE_DIR = os.path.dirname(__file__)

url = "https://www.boxofficemojo.com/year/world"


def save_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        with open("movies.html", "w") as f:
            f.write(r.text)
    return r.text


def data(url, name="2020"):
    html_text = save_data(url)
    if html_text == None:
        return False
    r_html = HTML(html=html_text)
    r_table = r_html.find("#table")
    table_data = []
    table_header = []
    if len(r_table) == 0:
        return False
    parsed_table = r_table[0]
    rows = parsed_table.find("tr")
    header_row = rows[0]
    header_cols = header_row.find("th")
    header_names = [x.text for x in header_cols]
    for row in rows:
        cols = row.find("td")
        row_data = []
        for i, col in enumerate(cols):
            row_data.append(col.text)
        table_data.append(row_data)
    df = pd.DataFrame(table_data, columns=header_names)
    path = os.path.join(BASE_DIR, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join('data', f"{name}.csv")
    df.to_csv(filepath, index=False)
    return True


def run(start, end):
    if start == None:
        now = datetime.datetime.now()
        start = now.year
    assert isinstance(start, int)
    assert isinstance(end, int)
    assert len(f"{start}") == 4
    for i in range(0, end):
        url = f"https://www.boxofficemojo.com/year/world/{start}/"
        finished = data(url, name=start)
        if finished:
            print(f"{start} finished")
        else:
            print(f"{start} not finished")
        start -= 1


if __name__ == "__main__":
    try:
        start1 = int(sys.argv[1])
    except:
        start = None
    try:
        end1 = int(sys.argv[2])
    except:
        end1 = 1
    run(start=start1, end=end1)

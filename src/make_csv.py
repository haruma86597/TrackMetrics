from bs4 import BeautifulSoup
import pandas as pd
import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class athlete_data:
    name: str
    grade: str
    athlete_number: str


def parse_name_tb(name_tb: str) -> athlete_data:
    # 全角空白を半角に置換して正規化します
    name_tb = name_tb.replace('\u3000', ' ')
    data = athlete_data(name="", grade="", athlete_number="")
    # 正規表現パターンの解説：
    # (.+)     -> 1文字以上の任意の文字
    # \((\d+)\) -> カッコの中に1文字以上の数字
    # :        -> コロン
    # (\d+)    -> 1文字以上の数字
    pattern = r"(.+)\((\d+)\):(\d+)"

    match = re.search(pattern, name_tb)
    data.name = match.group(1)
    data.grade = match.group(2)
    data.athlete_number = match.group(3)
    return data


def parse_date(date_text, year) -> datetime:
    cleaned_str = date_text.replace("[", "").replace("]", "")
    full_date_str = f"{year}/{cleaned_str}"

    dt = datetime.strptime(full_date_str, "%Y/%m/%d %H:%M")
    return dt


def converte_time(time_tb: str):
    total_seconds: float
    if ":" in time_tb:
        minutes_str, seconds_str = time_tb.split(":")
        total_seconds = int(minutes_str) * 60 + float(seconds_str)
    else:
        total_seconds = float(time_tb)
    return total_seconds


def parse_resultdata(soup: BeautifulSoup, year: int):
    date_span = soup.select_one('#round1 span[style*="font-size:14px"]')
    date_text = date_span.get_text(strip=True)
    date = parse_date(date_text, year)
    table_rows = soup.select('tr[id*="id_result_"]')
    datalist: list[dict] = []

    for row in table_rows:
        table_datas = row.find_all("td")
        rank: str = table_datas[0].get_text(strip=True)
        name_tb: str = table_datas[2].get_text(strip=True)
        time_tb: str = table_datas[4].get_text(strip=True)

        if time_tb == "DNS" or time_tb == "DNF":
            continue

        parsed_name_tb = parse_name_tb(name_tb)
        time: float = converte_time(time_tb)

        datalist.append({
            "year": year,
            "date": date,
            "rank": int(rank),
            "name": parsed_name_tb.name,
            "grade": int(parsed_name_tb.grade),
            "athlete_number": int(parsed_name_tb.athlete_number),
            "time": time
        })

    return datalist


def make_csv(datalist: list[dict]):
    df = pd.DataFrame(datalist)
    df.to_csv("result.csv", index=False, encoding="utf-8-sig")

import re
from datetime import datetime
from bs4 import BeautifulSoup
from datamodel.athlete import AthleteData

def parse_name_tb(name_tb: str) -> AthleteData:
    # 全角空白を半角に置換して正規化します
    name_tb = name_tb.replace('\u3000', ' ')
    data = AthleteData(name="", grade="", athlete_number="")
    # 正規表現パターンの解説：
    # (.+)     -> 1文字以上の任意の文字
    # \((\d+)\) -> カッコの中に1文字以上の数字
    # :        -> コロン
    # (\d+)    -> 1文字以上の数字
    pattern = r"(.+)\((\d+)\):(\d+)"

    match = re.search(pattern, name_tb)
    if match:
        data.name = match.group(1)
        data.grade = match.group(2)
        data.athlete_number = match.group(3)
    return data

def parse_date(date_text: str, year: int) -> datetime:
    cleaned_str = date_text.replace("[", "").replace("]", "")
    full_date_str = f"{year}/{cleaned_str}"
    dt = datetime.strptime(full_date_str, "%Y/%m/%d %H:%M")
    return dt

def convert_time(time_tb: str) -> float:
    if ":" in time_tb:
        minutes_str, seconds_str = time_tb.split(":")
        return int(minutes_str) * 60 + float(seconds_str)
    return float(time_tb)

def parse_resultdata(soup: BeautifulSoup, year: int) -> list[dict]:
    date_span = soup.select_one('#round1 span[style*="font-size:14px"]')
    date_text = date_span.get_text(strip=True) if date_span else ""
    date = parse_date(date_text, year) if date_text else None
    
    table_rows = soup.select('tr[id*="id_result_"]')
    datalist: list[dict] = []

    for row in table_rows:
        table_datas = row.find_all("td")
        if len(table_datas) < 5:
            continue
            
        rank_str = table_datas[0].get_text(strip=True)
        name_tb = table_datas[2].get_text(strip=True)
        time_tb = table_datas[4].get_text(strip=True)

        if time_tb in ("DNS", "DNF", "DQ", "NM"):
            continue

        try:
            rank = int(rank_str)
        except ValueError:
            continue

        parsed_name_tb = parse_name_tb(name_tb)
        time = convert_time(time_tb)

        datalist.append({
            "year": year,
            "date": date,
            "rank": rank,
            "name": parsed_name_tb.name,
            "grade": int(parsed_name_tb.grade) if parsed_name_tb.grade else 0,
            "athlete_number": int(parsed_name_tb.athlete_number) if parsed_name_tb.athlete_number else 0,
            "time": time
        })

    return datalist

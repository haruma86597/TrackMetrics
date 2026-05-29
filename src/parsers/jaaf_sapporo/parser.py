import json
from datetime import datetime
from datamodel.athlete import AthleteData


def parse_athlete_data(text: str, num_text: str) -> AthleteData:
    text = text.replace('\u3000', ' ')
    name_grade = text.split("<br/>")[1]
    name = name_grade.split("（")[0]
    grade = name_grade.split("（")[1].replace("）", "")
    num = num_text
    result = AthleteData(name, grade, num)
    return result


def convert_time(time_text: str) -> float:
    if ":" in time_text:
        minutes_str, seconds_str = time_text.split(":")
        return int(minutes_str) * 60 + float(seconds_str)
    return float(time_text)


def parse_date(date_text: str, call_time: str) -> datetime:
    date_text = date_text.split("（")[1].replace("）", "")
    call_time = call_time[-5:]

    combined_str = f"{date_text} {call_time}"
    dt = datetime.strptime(combined_str, "%Y/%m/%d %H:%M")
    return dt


def parse_data(result_data: dict):
    result_list: list[dict] = []

    date_text = result_data['Title']

    for group_data in result_data['ResultInfo']['2']:
        call_time = group_data['ShoshuJikan']
        for result in group_data['ResultList']:
            if result['Comment'] in ("DNS", "DNF", "DQ", "NM"):
                continue

            name_text = result['KyogishaMei']
            num_text = result['No']
            athlete_data = parse_athlete_data(name_text, num_text)
            time_text = result['Kiroku']
            time = convert_time(time_text)
            date = parse_date(date_text, call_time)
            year = date.year
            rank: int | None = None

            result_list.append({
                "year": year,
                "date": date,
                "rank": rank,
                "name": athlete_data.name,
                "grade": int(athlete_data.grade),
                "athlete_number": int(athlete_data.athlete_number),
                "time": time
            })

    result_list.sort(key=lambda x: x["time"])

    current_rank = 1  # 順位を保持する変数
    for i in range(len(result_list)):
        # 最初の要素(i=0)以外で、直前のタイムと違う場合のみ順位を更新
        if i > 0 and result_list[i]["time"] != result_list[i-1]["time"]:
            current_rank = i + 1

        # 現在の順位を辞書に書き込む
        result_list[i]["rank"] = current_rank

    return result_list

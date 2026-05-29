from pages.athlete_ranking.racedata_page import RaceDataPage
from pages.athlete_ranking.resultdata_page import ResultDataPage
from pages.athlete_ranking.gamelist_page import GameListPage
from pages.athlete_ranking.timetable_page import TimetablePage
from parsers.athlete_ranking.parser import parse_resultdata
from pages.jaaf_sapporo.gamelist_page import GameListPage as GameListPage_sapporo
from pages.jaaf_sapporo.timetable_page import TimetablePage as TimetablePage_sapporo
from pages.jaaf_sapporo.result_page import ResultPage as ResultPage_sapporo
from parsers.jaaf_sapporo.parser import parse_data as parse_data_sapporo
from parsers.openmeteo.parser import parse_weather_data
from csv_exporter import export_to_csv
from openmeteo import call_api
from datamodel.gender import Gender
from datetime import datetime


def main():
    csv_data = []

    # athletranking
    game_ids = GameListPage(1, "高体連新人").get_game_ids()
    for game_id in game_ids:
        event_id = RaceDataPage(game_id, Gender.MALE, "5000m").get_event_id()
        if not event_id:
            continue

        result_soup = ResultDataPage(game_id, event_id).get_soup()
        year = TimetablePage(game_id).get_year()

        datalist = parse_resultdata(result_soup, year)
        for data in datalist:
            csv_data.append(data)

    # jaaf_sapporo
    game_urls = GameListPage_sapporo("札幌支部高等学校新人陸上競技大会").get_game_urls()
    for game_url in game_urls:
        timetablepage = TimetablePage_sapporo(game_url, Gender.MALE, "5000m")
        target_event_list = timetablepage.get_event_list()
        event_data = timetablepage.get_event_data(target_event_list)
        if not event_data:
            continue
        resultpage = ResultPage_sapporo(event_data)
        result_json = resultpage.get_json()
        result_data = parse_data_sapporo(result_json)
        for data in result_data:
            csv_data.append(data)

    csv_data.sort(key=lambda x: x["year"], reverse=True)

    latest_year = None
    date_list: list[datetime] = []
    for data in csv_data:
        if latest_year != data["year"]:
            latest_year = data["year"]
            date_list.append(data["date"])

    weather_df = call_api(date_list)
    csv_data = parse_weather_data(weather_df, csv_data)

    export_to_csv(csv_data, "result.csv")
    print("csv生成成功しました。")


if __name__ == "__main__":
    main()

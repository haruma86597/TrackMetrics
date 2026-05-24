from pages.athlete_ranking.racedata_page import RaceDataPage
from pages.athlete_ranking.resultdata_page import ResultDataPage
from pages.athlete_ranking.gamelist_page import GameListPage
from pages.athlete_ranking.timetable_page import TimetablePage
from parser import parse_resultdata
from csv_exporter import export_to_csv
from datamodel.gender import Gender

def main():
    game_ids = GameListPage(1, "高体連新人").get_game_ids()
    csv_data = []
    for game_id in game_ids:
        event_id = RaceDataPage(game_id, Gender.MALE, "5000m").get_event_id()
        if not event_id:
            continue
            
        result_soup = ResultDataPage(game_id, event_id).get_soup()
        year = TimetablePage(game_id).get_year()
        
        datalist = parse_resultdata(result_soup, year)
        for data in datalist:
            csv_data.append(data)

    export_to_csv(csv_data, "result.csv")
    print("csv生成成功しました。")

if __name__ == "__main__":
    main()

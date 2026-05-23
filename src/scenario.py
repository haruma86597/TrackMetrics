from pages.racedata_page import racedata_page
from pages.resultdata_page import resultdata_page
from pages.gamelist_page import gamelist_page
from pages.timetable_page import timetable_page
from make_csv import parse_resultdata, make_csv
from datamodel.gender import Gender

game_ids = gamelist_page(1, "高体連新人").get_game_ids()
csv_data = []
for game_id in game_ids:
    event_id = racedata_page(game_id, Gender.MALE, "5000m").get_event_id()
    result_soup = resultdata_page(game_id, event_id).get_soup()
    year = timetable_page(game_id).get_year()
    datalist = parse_resultdata(result_soup, year)
    for data in datalist:
        csv_data.append(data)


make_csv(csv_data)
print(csv_data)

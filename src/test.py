from pages.jaaf_sapporo.timetable_page import TimetablePage
from pages.jaaf_sapporo.result_page import ResultPage
from pages.jaaf_sapporo.gamelist_page import GameListPage
from datamodel.gender import Gender
from parsers.jaaf_sapporo.parser import parse_data
from csv_exporter import export_to_csv


page = TimetablePage(
    "20230819-kokoshibushinjin/nans21v/shtml/", Gender.MALE, "5000m")


page2 = ResultPage(page.get_event_data(page.get_event_list()))


export_to_csv(parse_data(page2.get_json()))

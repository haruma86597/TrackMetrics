from pages.jaaf_sapporo.timetable_page import TimetablePage
from pages.jaaf_sapporo.result_page import ResultPage
from pages.jaaf_sapporo.gamelist_page import GameListPage
from datamodel.gender import Gender
from parsers.jaaf_sapporo.parser import parse_data
from csv_exporter import export_to_csv
import datetime
from openmeteo import call_api

date_list = [datetime.datetime(2025, 8, 23, 16, 25), datetime.datetime(2024, 8, 17, 16, 5), datetime.datetime(2023, 8, 19, 15, 15), datetime.datetime(2022, 8, 20, 14, 55), datetime.datetime(2021, 8, 26, 14, 50), datetime.datetime(2020, 8, 30, 11, 50), datetime.datetime(2019, 8, 17, 16, 10), datetime.datetime(
    2018, 8, 18, 15, 20), datetime.datetime(2017, 8, 19, 15, 30), datetime.datetime(2016, 8, 20, 16, 0), datetime.datetime(2015, 8, 23, 16, 10), datetime.datetime(2014, 8, 23, 16, 0), datetime.datetime(2013, 8, 31, 16, 0), datetime.datetime(2012, 9, 1, 15, 30), datetime.datetime(2011, 8, 13, 16, 5)]

call_api(date_list)

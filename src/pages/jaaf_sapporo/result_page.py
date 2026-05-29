import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta, time
from datamodel.gender import Gender
from datamodel.event import EventData, Round


class ResultPage:
    def __init__(self, event_data: EventData):
        self.base_url = "https://result.jaaf-sapporo.jp/"
        self.event_data = event_data
        self.event_name: str = event_data.name
        self.event_time: time = event_data.time
        self.game_url: str = event_data.game_url
        self.event_url: str = event_data.event_url
        self.event_round: Round = event_data.round

    def get_json(self):
        self.event_url = self.event_url.replace("html", "json")
        result_url = self.base_url + self.game_url + self.event_url
        print(result_url)
        response = requests.get(result_url)
        response.encoding = 'utf-8'
        result_json = response.json()
        return result_json

    def get_timerace_json(self):
        json_path = "timeraceshukei/TimeraceShukei.json"
        print(self.base_url + self.game_url + json_path)
        response = requests.get(self.base_url + self.game_url + json_path)
        response.encoding = 'utf-8'
        timerace_datas: list[dict] = response.json()['TimeraceShukeiList']

        totaling_url: str | None = None
        for timerace_data in timerace_datas:
            if timerace_data['KyogiMei'] == self.event_name:
                totaling_url = timerace_data['Link'][2:]
                totaling_url = totaling_url.replace("html", "json")
                break

        if not totaling_url:
            return None

        result_url = self.base_url + self.game_url + "timeraceshukei/" + totaling_url
        response = requests.get(result_url)
        response.encoding = 'utf-8'
        result_json = response.json()
        return result_json

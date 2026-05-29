import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta, time
from datamodel.gender import Gender
from datamodel.event import EventData, Round


class TimetablePage:
    def __init__(self, game_url: str, gender: Gender, event_name: str):
        self.base_url = "https://result.jaaf-sapporo.jp/"
        self.game_url = game_url
        self.json_url = f"{self.base_url}{self.game_url}TimeTable.json"
        self.gender = gender
        self.event_name = gender.value + event_name
        self.event_data: EventData | None = None

    def get_event_list(self):
        print(self.json_url)
        response = requests.get(self.json_url)
        response.encoding = 'utf-8'

        event_list: list[dict] = response.json()['SyumokuBetsuList']
        # 全角スペースの削除
        for event in event_list:
            for key, value in event.items():
                if value is not None and isinstance(value, str):
                    event[key] = value.replace('\u3000', '')

        target_event_list: list[dict] = []
        for event in event_list:
            if event['KyogiMei'] == self.event_name:
                target_event_list.append(event)

        return target_event_list

    def get_event_data(self, event_list: list[dict]) -> EventData | None:
        timerace_list: list[dict] = []
        semi_final_list: list[dict] = []
        preliminarys_list: list[dict] = []
        target_event_list: list[dict] = []

        for event in event_list:
            if event['Round'] == Round.TIMERACE:
                timerace_list.append(event)
            elif event['Round'] == Round.SEMIFINAL:
                semi_final_list.append(event)
            elif event['Round'] == Round.PRELIMINARY:
                preliminarys_list.append(event)

        round: Round | None = None
        if timerace_list:
            target_event_list = timerace_list[0]
            round = Round.TIMERACE
        elif semi_final_list:
            target_event_list = semi_final_list[0]
            round = Round.SEMIFINAL
        elif preliminarys_list:
            target_event_list = preliminarys_list[0]
            round = Round.PRELIMINARY

        if not target_event_list:
            return None

        event_time_str = target_event_list['KaishiJikan']
        event_datetime = datetime.strptime(event_time_str, "%H:%M")
        event_time = event_datetime.time()
        url = target_event_list['LinkRound'][2:]

        result: EventData = EventData(
            target_event_list['KyogiMei'], event_time, self.game_url, url, round)

        self.event_data = result
        return result


if __name__ == "__main__":
    page = TimetablePage(
        "20230819-kokoshibushinjin/nans21v/shtml/", Gender.MALE, "5000m")
    page.get_event_data()

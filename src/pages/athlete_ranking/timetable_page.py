import requests
from bs4 import BeautifulSoup


class timetable_page:
    def __init__(self, game_id: str):
        self.url = "https://games.athleteranking.com/timetable.php"
        self.game_id = game_id
        self.year: int = None

    def get_year(self):
        payload = {"id": self.game_id}
        response = requests.post(self.url, data=payload)
        response.encoding = 'euc_jis_2004'  # EUC-JPの拡張（機種依存文字対応）
        soup = BeautifulSoup(response.text, "html.parser")

        year_text = soup.find('th', class_='timetable_date').get_text()
        self.year = int(year_text[:4])
        return self.year

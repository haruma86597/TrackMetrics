import requests
from bs4 import BeautifulSoup
import re
from datamodel.gender import Gender


class RaceDataPage:
    def __init__(self, game_id: str, gender: Gender, event_name: str):
        self.url = "https://games.athleteranking.com/racedata.php"
        self.game_id = game_id
        self.event_name = event_name
        self.gender = gender
        self.event_id = None

    def get_event_id(self) -> str | None:
        payload: dict = {
            "id": self.game_id,
            "select_game_num": self.game_id,
        }

        print(self.url)
        response = requests.post(self.url, data=payload)
        response.encoding = 'euc_jis_2004'  # EUC-JPの拡張（機種依存文字対応）
        soup = BeautifulSoup(response.text, "html.parser")

        if self.gender == Gender.MALE:
            target_a_tags = soup.select("td.race_l_td1 a")
        else:
            target_a_tags = soup.select("td.race_l_td2 a")

        for a_tag in target_a_tags:
            if self.event_name == a_tag.get_text(strip=True):
                onclick_text = a_tag.get('onclick', '')
                # ダブルクォートで囲まれた最初の文字列（ID）を抽出
                match = re.search(r'"(.*?)"', onclick_text)
                if match:
                    event_id = match.group(1).removeprefix(self.game_id)
                    return event_id
        return None


if __name__ == "__main__":
    page = RaceDataPage("aa512022021", Gender.MALE, "5000m")
    page.get_event_id()

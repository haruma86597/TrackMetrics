import requests
from bs4 import BeautifulSoup
from parser import parse_resultdata
from csv_exporter import export_to_csv

class ResultDataPage:
    def __init__(self, game_id: str, event_id: str):
        self.url = "https://games.athleteranking.com/resultdata.php"
        self.event_id = event_id
        self.game_id = game_id
        self.soup = None

    def get_soup(self) -> BeautifulSoup:
        payload = {
            "id": self.game_id + self.event_id,
            "TOTAL_LIST": "1"  # 総合結果
        }
        response = requests.post(self.url, data=payload)
        response.encoding = 'euc_jis_2004'  # EUC-JPの拡張（機種依存文字対応）
        response.raise_for_status()  # リクエスト成功確認
        self.soup = BeautifulSoup(response.text, "html.parser")
        return self.soup

if __name__ == "__main__":
    page = ResultDataPage("aa512022021", "@1@0@0@A1500@ALL")
    # For testing parsing, year is required now:
    # data = parse_resultdata(page.get_soup(), 2022)
    # export_to_csv(data)

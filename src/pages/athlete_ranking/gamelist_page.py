import requests
from bs4 import BeautifulSoup


class GameListPage:
    def __init__(self, pref: int, game_search_word: str):
        self.url = "https://games.athleteranking.com/gamelist.php"
        self.game_ids: list[str] = []
        self.game_search_word = game_search_word
        self.pref = pref

    def get_game_ids(self) -> list[str]:
        payload: dict = {
            "pref": self.pref,  # 1は北海道
            "year_s": "2001",
            "month_s": "1",
            "year_e": "2030",
            "month_e": "12"
        }

        print(self.url)
        response = requests.post(self.url, data=payload)
        response.encoding = 'euc_jis_2004'  # EUC-JPの拡張（機種依存文字対応）
        soup = BeautifulSoup(response.text, "html.parser")

        # CSSセレクタで対象のリンクを一括取得
        a_tags = soup.select("td.g_l_td1 a, td.g_l_td2 a")

        for a_tag in a_tags:
            if self.game_search_word in a_tag.get_text(strip=True):
                # href属性を取得し、"gid=" で分割した最後の要素（ID部分）を抽出
                href = a_tag.get('href', '')
                game_id = href.split('gid=')[-1]
                self.game_ids.append(game_id)

        return self.game_ids


if __name__ == "__main__":
    page = GameListPage(1, "高体連新人")
    page.get_game_ids()

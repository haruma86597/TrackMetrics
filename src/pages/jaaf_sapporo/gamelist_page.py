import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import re
from urllib.parse import urlparse, urlunparse
import posixpath
import time


class GameListPage:
    def __init__(self, game_search_word: str):
        self.base_url = "https://result.jaaf-sapporo.jp/"
        self.initial_yaer: int = 2023
        self.current_year: int = datetime.now().year
        self.game_urls: list[str] = []
        self.game_search_word = game_search_word

    def get_game_urls(self):
        # 今年度の大会の処理
        print(self.base_url)
        time.sleep(1)
        response = requests.get(self.base_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        div_tag = self.get_target_div(soup)
        if div_tag:
            latest_game_date = self.parse_date(div_tag, self.current_year)
            latest_game_end_date = latest_game_date + \
                timedelta(days=1)  # 大会終了の次の日
            if latest_game_end_date < date.today():
                a_tag = div_tag.find('a')
                href = a_tag.get('href')
                self.game_urls.append(href)

        # 過去の大会の処理
        for year in range(self.initial_yaer, self.current_year):
            time.sleep(1)
            print(f"{self.base_url}result{year}.html")
            response = requests.get(f"{self.base_url}result{year}.html")
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")

            div_tag = self.get_target_div(soup)
            if div_tag:
                a_tag = div_tag.find('a')
                href = a_tag.get('href')
                game_url = self.replace_url(href)
                self.game_urls.append(game_url)

        return self.game_urls

    def parse_date(self, div_tag: BeautifulSoup, year: int) -> date:
        date_text: str = div_tag.find('p', class_='day').get_text(strip=True)
        date_text = re.findall(r"\d+", date_text)
        month = int(date_text[0])
        day = int(date_text[2])
        game_date = date(year, month, day)
        return game_date

    def get_target_div(self, soup: BeautifulSoup) -> BeautifulSoup | None:
        div_tags = soup.find_all('div', class_='block')
        for div_tag in div_tags:
            if self.game_search_word in div_tag.get_text(strip=True):
                return div_tag
        return None

    def replace_url(self, url):
        parsed = urlparse(url)
        new_path = posixpath.dirname(parsed.path)
        if not new_path.endswith('/'):
            new_path += '/'
        clean_parsed = parsed._replace(path=new_path, query='', fragment='')
        result = urlunparse(clean_parsed)
        return result


if __name__ == "__main__":
    page = GameListPage("札幌支部高等学校新人陸上競技大会")
    page.get_game_urls()

import pandas as pd
from datetime import datetime, date


def parse_weather_data(weather_df: pd.DataFrame, csv: list[dict]) -> list[dict]:
    for data in csv:
        weather_df['date'] = pd.to_datetime(weather_df['date'])
        search_date = data['date'].date()

        result = weather_df[weather_df['date'].dt.date == search_date]

        data['temperature'] = result['気温(℃)'].values[0]
        data['apparent_temperature'] = result['体感温度(℃)'].values[0]
        data['humidity'] = result['湿度(%)'].values[0]
        data['precipitation'] = result['降水量(mm)'].values[0]
        data['wind_speed'] = result['風速(m/s)'].values[0]
        data['wind_gusts'] = result['最大瞬間風速(m/s)'].values[0]

    return csv

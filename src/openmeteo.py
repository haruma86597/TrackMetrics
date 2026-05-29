import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime


def call_api(date_list: list[datetime]):
    if not date_list:
        print("日付リストが空です。")
        return pd.DataFrame()

    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"

    # タイムゾーンを指定して時刻を丸める
    target_times = pd.to_datetime(
        date_list).tz_localize("Asia/Tokyo").floor("h")
    # ユニークな日付を取得 (Asia/Tokyo基準で)
    unique_dates = target_times.tz_convert(
        "Asia/Tokyo").strftime("%Y-%m-%d").unique()

    df_list = []

    print(
        f"OpenMeteo API を{len(unique_dates)}回呼び出します。しばらくお待ちください...")

    for date_str in unique_dates:
        params = {
            "latitude": 43.0621,
            "longitude": 141.3544,
            "start_date": date_str,
            "end_date": date_str,
            "hourly": [
                "temperature_2m",
                "apparent_temperature",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_gusts_10m",
            ],
            "timezone": "Asia/Tokyo",
        }

        try:
            responses = openmeteo.weather_api(url, params=params)
        except Exception as e:
            print(f"日付 {date_str} のOpenMeteo APIリクエスト中にエラーが発生しました: {e}")
            continue

        response = responses[0]
        hourly = response.Hourly()

        # ==========================================
        # 2. 取得データを DataFrame にする
        # ==========================================
        start_time = pd.to_datetime(hourly.Time(), unit="s", utc=True).tz_convert(
            "Asia/Tokyo"
        )
        end_time = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True).tz_convert(
            "Asia/Tokyo"
        )

        df = pd.DataFrame(
            {
                "date": pd.date_range(
                    start=start_time,
                    end=end_time,
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left",
                ),
                "気温(℃)": hourly.Variables(0).ValuesAsNumpy(),
                "体感温度(℃)": hourly.Variables(1).ValuesAsNumpy(),
                "湿度(%)": hourly.Variables(2).ValuesAsNumpy(),
                "降水量(mm)": hourly.Variables(3).ValuesAsNumpy(),
                "風速(m/s)": hourly.Variables(4).ValuesAsNumpy(),
                "最大瞬間風速(m/s)": hourly.Variables(5).ValuesAsNumpy(),
            }
        )
        df_list.append(df)

    if not df_list:
        print("データを取得できませんでした。")
        return pd.DataFrame()

    df_all = pd.concat(df_list, ignore_index=True)

    # ==========================================
    # 3. 指定された日時だけでフィルタリングする
    # ==========================================
    df_result = df_all[df_all["date"].isin(target_times)]

    return df_result

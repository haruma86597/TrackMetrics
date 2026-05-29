import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime

date_list = [datetime(2025, 8, 23, 16, 25), datetime(2024, 8, 17, 16, 5)]

cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

target_times = pd.to_datetime(date_list).tz_localize("Asia/Tokyo").floor("h")
unique_dates = target_times.tz_convert("Asia/Tokyo").strftime("%Y-%m-%d").unique()

df_list = []
for date_str in unique_dates:
    params = {
        "latitude": 43.0621,
        "longitude": 141.3544,
        "start_date": date_str,
        "end_date": date_str,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "shortwave_radiation",
        ],
        "timezone": "Asia/Tokyo",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    start_time = pd.to_datetime(hourly.Time(), unit="s", utc=True).tz_convert("Asia/Tokyo")
    end_time = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True).tz_convert("Asia/Tokyo")

    df = pd.DataFrame(
        {
            "date": pd.date_range(
                start=start_time,
                end=end_time,
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ),
            "気温(℃)": hourly.Variables(0).ValuesAsNumpy(),
            "湿度(%)": hourly.Variables(1).ValuesAsNumpy(),
            "降水量(mm)": hourly.Variables(2).ValuesAsNumpy(),
            "風速(m/s)": hourly.Variables(3).ValuesAsNumpy(),
            "日射量(W/m²)": hourly.Variables(4).ValuesAsNumpy(),
        }
    )
    df_list.append(df)

df_all = pd.concat(df_list, ignore_index=True)
df_result = df_all[df_all["date"].isin(target_times)]
print(df_result)

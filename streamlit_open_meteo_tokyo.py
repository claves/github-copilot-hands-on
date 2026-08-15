"""
Streamlit app: Tokyo 7-day weather forecast using Open-Meteo

Usage:
1. Install dependencies:
   pip install streamlit requests pandas
2. Run:
   streamlit run streamlit_open_meteo_tokyo.py

This app fetches a 7-day forecast for Tokyo (latitude 35.6895, longitude 139.6917)
from Open-Meteo and displays a table, charts, and a CSV download.
"""

import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta

# Tokyo coordinates
LATITUDE = 35.6895
LONGITUDE = 139.6917

st.set_page_config(page_title="Tokyo 7-day Forecast (Open-Meteo)", layout="wide")

st.title("東京の7日間天気予報")
st.markdown("データ提供: Open-Meteo (https://open-meteo.com)")

@st.cache_data(ttl=600)
def fetch_tokyo_forecast():
    """Fetch 7-day daily forecast for Tokyo from Open-Meteo."""
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        # daily fields to request
        "daily": 
            ",".join([
                "weathercode",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "windspeed_10m_max",
            ]),
        "forecast_days": 7,
        "timezone": "Asia/Tokyo",
    }

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        st.error(f"API取得中にエラーが発生しました: {e}")
        return None

    data = resp.json()

    # Extract daily arrays
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    weathercodes = daily.get("weathercode", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wind = daily.get("windspeed_10m_max", [])

    df = pd.DataFrame({
        "date": pd.to_datetime(dates).date,
        "weathercode": weathercodes,
        "temp_max_C": tmax,
        "temp_min_C": tmin,
        "precipitation_mm": precip,
        "wind_max_kmh": wind,
    })

    return df


# Map Open-Meteo weather codes to descriptions and emoji
WEATHER_CODE_MAP = {
    0: ("晴天", "☀️"),
    1: ("主に晴れ", "🌤️"),
    2: ("部分的に曇り", "⛅"),
    3: ("曇り", "☁️"),
    45: ("霧", "🌫️"),
    48: ("霧（凍結露）", "🌫️"),
    51: ("小雨（霧雨）", "🌦️"),
    53: ("中程度の霧雨", "🌦️"),
    55: ("激しい霧雨", "🌧️"),
    56: ("凍結霧雨（軽）", "🥶🌧️"),
    57: ("凍結霧雨（重）", "🥶🌧️"),
    61: ("小雨", "🌧️"),
    63: ("中雨", "🌧️"),
    65: ("激しい雨", "⛈️"),
    66: ("軽い凍雨", "🥶🌧️"),
    67: ("重い凍雨", "🥶⛈️"),
    71: ("小雪", "🌨️"),
    73: ("中雪", "🌨️"),
    75: ("激しい雪", "❄️"),
    77: ("雪粒", "🌨️"),
    80: ("小さなにわか雨", "🌦️"),
    81: ("中程度のにわか雨", "🌧️"),
    82: ("激しいにわか雨", "⛈️"),
    85: ("小さなにわか雪", "🌨️"),
    86: ("激しいにわか雪", "❄️"),
    95: ("雷雨", "⛈️"),
    96: ("雷雨（軽い雹）", "⛈️"),
    99: ("雷雨（激しい雹）", "⛈️"),
}


def code_to_desc(code: int):
    return WEATHER_CODE_MAP.get(code, ("不明", "❓"))


# Fetch data
with st.spinner("Open-Meteo から天気データを取得中..."):
    df = fetch_tokyo_forecast()

if df is None:
    st.stop()

# Enrich df with descriptions and emoji
df = df.copy()
descs = [code_to_desc(int(c))[0] for c in df["weathercode"]]
emojis = [code_to_desc(int(c))[1] for c in df["weathercode"]]
df["description"] = descs
df["emoji"] = emojis

# Show summary
st.subheader("場所: 東京 (緯度 35.6895 / 経度 139.6917)")

# Two-column layout: table and charts
col1, col2 = st.columns((1, 1))

with col1:
    st.markdown("### 日別の予報（7日分）")
    # Display a friendly table
    display_df = df[["date", "emoji", "description", "temp_max_C", "temp_min_C", "precipitation_mm", "wind_max_kmh"]]
    display_df = display_df.rename(columns={
        "date": "日付",
        "emoji": "天気",
        "description": "説明",
        "temp_max_C": "最高気温 (°C)",
        "temp_min_C": "最低気温 (°C)",
        "precipitation_mm": "降水量合計 (mm)",
        "wind_max_kmh": "最大風速 (km/h)",
    })
    st.dataframe(display_df.style.set_properties(**{"font-size": "14px"}), height=420)

    csv = df.to_csv(index=False)
    st.download_button("CSV をダウンロード", csv, file_name="tokyo_7day_forecast.csv", mime="text/csv")

with col2:
    st.markdown("### 気温の推移")
    temp_chart_df = df.set_index("date")[ ["temp_max_C", "temp_min_C"] ]
    st.line_chart(temp_chart_df, height=300)

    st.markdown("### 降水量（合計）と最大風速")
    precip_chart_df = df.set_index("date")[ ["precipitation_mm", "wind_max_kmh"] ]
    st.bar_chart(precip_chart_df, height=300)

st.markdown("---")

# Show raw JSON toggle
if st.expander("API レスポンスの生データを確認する"):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params_preview = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "forecast_days": 7,
        "timezone": "Asia/Tokyo",
    }
    try:
        r = requests.get(base_url, params=params_preview, timeout=10)
        r.raise_for_status()
        st.json(r.json())
    except requests.RequestException as e:
        st.write(f"取得に失敗しました: {e}")

st.caption("注意: このアプリは学習/デモ目的のものです。実運用ではエラーハンドリング、再試行、レート制限の考慮を強化してください。")

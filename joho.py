import streamlit as st
import requests
from datetime import datetime

# ---------- タイトル ----------
st.title("🎵 気分で選ぶ Official髭男dism のおすすめ曲")
mode = st.radio(
    "🎧 表示モードを選んでください",
    ("有名な曲モード", "マニアックモード")
)
# ---------- 気分選択 ----------
user_text = st.text_input("今の気持ちを文章で書いてください（例：今日は最悪…）")

def judge_mood(text):
    if "疲" in text or "眠" in text or "しんど" in text:
        return "落ち着きたい"
    elif "悲" in text or "泣" in text or "つら" in text:
        return "悲しい"
    elif "むかつ" in text or "怒" in text or "イライラ" in text:
        return "やる気を出したい"
    else:
        return "楽しい"

if user_text:
    mood = judge_mood(user_text)
    st.write(f"👉 判定された気分：**{mood}**")
else:
    mood = "楽しい"

max_songs = st.slider(
    "表示する曲数を選んでください",
    min_value=1,
    max_value=20,
    value=5
)

# ---------- データ取得 ----------
def get_higedan_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "Official髭男dism",
        "country": "JP",
        "media": "music",
        "entity": "song",
        "limit": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data["results"]

# ---------- 説明文 ----------
def make_description(song):
    album = song.get("collectionName", "不明なアルバム")

    release = song.get("releaseDate")
    if release:
        try:
            dt = datetime.fromisoformat(release.replace("Z", "+00:00"))
            release_str = dt.strftime("%Y年%m月%d日")
        except:
            release_str = release
    else:
        release_str = "不明"

    genre = song.get("primaryGenreName", "不明")

    duration_ms = song.get("trackTimeMillis")
    if duration_ms:
        seconds = duration_ms // 1000
        minutes = seconds // 60
        sec = seconds % 60
        duration_str = f"{minutes}分{sec:02d}秒"
    else:
        duration_str = "不明"

    desc = (
        f"本楽曲は Official髭男dism のアルバム『{album}』に収録されている作品である。  \n"
        f"{release_str} に発表され、ジャンルは {genre} に分類される。  \n"
        f"楽曲時間は {duration_str} で、魅力的な音楽性を備えている。"
    )
    return desc

# ---------- 曲取得 ----------
songs = get_higedan_songs()

# ---------- 気分別おすすめキーワード ----------
songs = get_higedan_songs()
# モードによって並びを変更
if mode == "マニアックモード":
    songs = list(reversed(songs))  # あまり知られてない曲が出やすくなる

# ---------- 気分別キーワード ----------
if mood == "楽しい":
    keywords = ["イエスタデイ"]
elif mood == "悲しい":
    keywords = ["Pretender"]
elif mood == "落ち着きたい":
    keywords = ["パラボラ"]
else:
    keywords = ["Stand By You"]

MAX_SONGS = 5
count = 0
displayed = set()

# ---------- 曲の表示 ----------
for song in songs:

    title = song["trackName"]

    # 重複防止
    if title in displayed:
        continue

    # キーワードに一致したら表示
    if any(k in title for k in keywords):

        st.subheader(title)
        st.write(f"🎤 アーティスト：{song['artistName']}")
        st.write(make_description(song))
        st.markdown("---")

        displayed.add(title)
        count += 1

        # 5曲出たら終了
        if count == MAX_SONGS:
            break


# ---------- 足りなかったときの保険 ----------
if count < MAX_SONGS:
    for song in songs:

        title = song["trackName"]

        if title in displayed:
            continue

        st.subheader(title)
        st.write(f"🎤 アーティスト：{song['artistName']}")
        st.write(make_description(song))
        st.markdown("---")

        displayed.add(title)
        count += 1

        if count == MAX_SONGS:
            break

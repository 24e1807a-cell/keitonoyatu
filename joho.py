import streamlit as st
import requests
import random

TEXT = {
    "app_title": {
        "日本語": "🎵 unofficialな髭男の曲紹介",
        "English": "🎵 Unofficial HIGE DANDISM Song Guide"
    },
    "language_label": {
        "日本語": "言語を選択",
        "English": "Select Language"
    },
    "mood_input": {
        "日本語": "今の気持ちを書いてね（例：悲しい、疲れた など）",
        "English": "Write how you feel now (ex: sad, tired)"
    },
    "mood_result": {
        "日本語": "👉 判定された気分",
        "English": "👉 Detected mood"
    }
}
language = st.radio(
    TEXT["language_label"]["English"] + " / " + TEXT["language_label"]["日本語"],
    ("日本語", "English"),
    horizontal=True
)
user_text = st.text_input(TEXT["mood_input"][language])
st.write("DEBUG language =", language)
st.write("DEBUG TEXT keys =", TEXT["mood_input"].keys())

# 背景色を設定
st.markdown("""
<style>
.stApp {
    background-color: #C7D2FE;
}
</style>
""", unsafe_allow_html=True)


st.title(TEXT["app_title"][language])
TEXT = {
    "app_title": {
        "日本語": "🎵 unofficialな髭男の曲紹介",
        "English": "🎵 Unofficial HIGE DANDISM Song Guide"
    }
}

# -------------------------------
# 髭男の曲をAPIで取得
# -------------------------------
def get_higedan_songs():
    url = "https://itunes.apple.com/search"
    params = {
        "term": "Official髭男dism",
        "entity": "song",
        "country": "JP",
        "limit": 200
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json()["results"]

    # 重複削除（曲名＋アーティストで判定）
    unique = {}
    for song in data:
        key = song["trackName"] + song["artistName"]
        if key not in unique:
            unique[key] = song

    return list(unique.values())


# -------------------------------
# 曲の説明
# -------------------------------
def make_description(song):
    album = song.get("collectionName", "不明")
    year = song.get("releaseDate", "不明")[:4]
    return f"アルバム：{album} / リリース年：{year}"


user_text = st.text_input(TEXT["mood_input"][language])

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
else:
    mood = "楽しい"

st.write(
    f"{TEXT['mood_result'][language]}：**{mood}**"
)


# -------------------------------
# モード切り替え
# -------------------------------
mode = st.radio(
    "表示モードを選んでください",
    ["有名な曲モード", "マニアックモード"]
)

# -------------------------------
# 曲取得
# -------------------------------
songs = get_higedan_songs()
# -------------------------------
# 気分別キーワード（複数）
# -------------------------------
if mood == "楽しい":
    keywords = ["イエスタデイ", "ノーダウト", "FIRE"]
elif mood == "悲しい":
    keywords = ["Pretender", "Laughter", "115万"]
elif mood == "落ち着きたい":
    keywords = ["パラボラ", "Bedroom", "Driver"]
else:
    keywords = ["Stand By You", "Cry Baby"]

# -------------------------------
# 並び替え（マニアックモード対応）
# -------------------------------
if mode == "マニアックモード":
    songs_list = list(reversed(songs))
else:
    songs_list = songs

# -------------------------------
# 曲表示
# -------------------------------
count = 0
MAX_SONGS = st.slider("🎧 表示する曲の数", 1, 5, 1)

for song in songs_list:
     title = song["trackName"]

     if any(k in title for k in keywords):


        cols = st.columns([1, 3])

        with cols[0]:
            if song.get("artworkUrl100"):
                st.image(song["artworkUrl100"], width=120)

        with cols[1]:
            st.markdown(f"### 🎵 {title}")
            st.write(f"🎤 {song['artistName']}")
            st.write(make_description(song))

        st.markdown("---")

        count += 1
        if count >= MAX_SONGS:
            break 

st.header("🔍 曲名で検索")

search_word = st.text_input("曲名を入力してください")

if search_word:

    count = 0

    for song in songs:
        title = song["trackName"]

        if search_word in title:

            st.subheader(f"🎵 {title}")
            st.write(f"🎤 {song['artistName']}")
            st.write(make_description(song))
            st.markdown("---")

            count += 1
            if count >= 5:
                break


if count == 0:
    st.write("この条件に合う曲が見つかりませんでした。")
st.header("🎲 ランダムで今日の一曲！！")

if st.button("ランダムで曲を選ぶ"):

    random_song = random.choice(songs)
    title = random_song["trackName"]

    # -------- あたり判定（20%）--------
    atari = random.randint(1, 5)  # 1〜5のどれか
    if atari == 1:
        st.balloons()
        st.success("🎉🎉 あたり！！今日のラッキーソング！ 🎉🎉")

    st.subheader(f"🎵 {title}")
    st.write(f"🎤 {random_song['artistName']}")

    # ジャケット画像
    if "artworkUrl100" in random_song:
        st.image(random_song["artworkUrl100"])

    st.write(make_description(random_song))
    # …（曲表示コードなど終わり）

st.write("---")

st.markdown("""
<a href="https://higedan.com" target="_blank" style="
    text-decoration: none;
">
  <div style="
      background-color:#1f2937;
      color:white;
      padding:16px 24px;
      border-radius:14px;
      text-align:center;
      font-size:20px;
      font-weight:bold;
      transition:0.2s;
  ">
      🎤 Official髭男dism 公式サイトへ
  </div>
</a>
""", unsafe_allow_html=True)
def open_new_song():
    webbrowser.open("https://hgdn.lnk.to/Sanitizer")
    st.header("🆕 新曲はこちら")

st.header("🆕 新曲はこちら")

st.link_button(
    "Sanitizer を聴く",
    "https://hgdn.lnk.to/Sanitizer"
)

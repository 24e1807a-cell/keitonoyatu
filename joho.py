import streamlit as st
import requests
import random

# ▼ iTunes APIで髭男の曲を取得
@st.cache_data
def get_higedan_songs():
    url = "https://itunes.apple.com/search?term=official+hige+dandism&country=jp&media=music&limit=50"
    response = requests.get(url)
    data = response.json()
    return data["results"]

# ▼ 気分ごとの推薦ロジック
def recommend_by_mood(mood, songs):
    mood_keywords = {
        "元気": ["ミックスナッツ", "FIRE", "Stand", "Parabola", "No Doubt"],
        "落ち着き": ["Pretender", "I LOVE", "宿命", "I Love...", "バラード"],
        "泣きたい": ["Cry", "Laughter", "イエスタデイ", "アポトーシス"]
    }

    keywords = mood_keywords[mood]
    filtered = []

    for s in songs:
        name = s["trackName"]
        for kw in keywords:
            if kw.lower() in name.lower():
                filtered.append(s)

    if len(filtered) == 0:
        return random.choice(songs)
    else:
        return random.choice(filtered)


# ▼ Streamlit UI
st.title("🎵 髭男おすすめ曲アプリ（API × Streamlit）")

st.write("気分を選んでください👇")

mood = st.selectbox("気分を選ぶ", ["元気", "落ち着き", "泣きたい"])

if st.button("おすすめ曲を見る"):
    songs = get_higedan_songs()
    song = recommend_by_mood(mood, songs)

    st.subheader("🎶 あなたへのおすすめ曲")
    st.write(f"**{song['trackName']}**")

    # ジャケット画像
    st.image(song["artworkUrl100"], width=200)

    # 試聴URL
    if "previewUrl" in song:
        st.audio(song["previewUrl"])

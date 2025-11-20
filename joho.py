import streamlit as st
import requests
import random

# ▼ iTunes APIで髭男の曲を取得
@st.cache_data
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


# ▼ 気分ごとのキーワード設定
mood_keywords = {
    "元気": ["ミックスナッツ", "FIRE", "Stand", "パラボラ", "No Doubt"],
    "落ち着き": ["Pretender", "I LOVE", "宿命", "バラード", "Stand By You"],
    "泣きたい": ["Cry", "Laughter", "イエスタデイ", "アポトーシス"],
}

# ▼ 気分に合う曲を複数返す
def recommend_by_mood(mood, songs, count=5):
    keywords = mood_keywords[mood]
    filtered = []

    for s in songs:
        name = s["trackName"]
        if any(kw.lower() in name.lower() for kw in keywords):
            filtered.append(s)

    # 該当曲が少ない → APIの中からランダム補完
    if len(filtered) < count:
        while len(filtered) < count:
            filtered.append(random.choice(songs))

    # ランダムで「数曲」選ぶ
    return random.sample(filtered, count)


# ▼ Streamlit UI
st.title("🎵 髭男おすすめ曲アプリ（API × Streamlit）")
st.write("気分を選んでください👇")

mood = st.selectbox("気分を選ぶ", ["元気", "落ち着き", "泣きたい"])
num = st.slider("表示する曲数", min_value=3, max_value=10, value=5)

if st.button("おすすめ曲を見る"):
    songs = get_higedan_songs()
    results = recommend_by_mood(mood, songs, count=num)

    st.subheader(f"🎶 あなたへのおすすめ曲（{num} 曲）")

    # 複数曲をカード形式で表示
    for song in results:
        st.write(f"### {song['trackName']}")
        st.image(song["artworkUrl100"], width=150)
        if "previewUrl" in song:
            st.audio(song["previewUrl"])
        st.markdown("---")

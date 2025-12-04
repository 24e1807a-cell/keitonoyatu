import streamlit as st

# 曲を取得する関数（君の元の関数）
songs = get_higedan_songs()

st.title("🎧 Official髭男dism レコメンド")

# モード選択
mode = st.radio("モードを選んでね", ["有名な曲モード", "マニアックモード"])

# 気分選択
mood = st.selectbox(
    "今の気分は？",
    ["楽しい", "悲しい", "落ち着きたい", "元気を出したい"]
)

# 気分によるキーワード
if mood == "楽しい":
    keywords = ["イエスタデイ", "ノーダウト"]
elif mood == "悲しい":
    keywords = ["Pretender", "115万キロのフィルム"]
elif mood == "落ち着きたい":
    keywords = ["パラボラ", "Laughter"]
else:
    keywords = ["Stand By You", "FIRE GROUND"]

# ===== 重複を消す処理 =====
unique_songs = []
used_titles = set()

for song in songs:
    title = song["trackName"]

    if title not in used_titles:
        unique_songs.append(song)
        used_titles.add(title)

# ===== モードで並び替え =====
if mode == "マニアックモード":
    song_list = list(reversed(unique_songs))
else:
    song_list = unique_songs


# ===== 表示 =====
st.subheader("🎵 あなたにおすすめの5曲")

count = 0

for song in song_list:

    if any(k in song["trackName"] for k in keywords):

        st.markdown(f"""
        <div style="
        background-color: #C7D2FE;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        color: black;
        border: 1px solid #ddd;
        ">
        <h3>🎵 {song['trackName']}</h3>
        <p>🎤 {song['artistName']}</p>
        <p>{make_description(song)}</p>
        </div>
        """, unsafe_allow_html=True)

        count += 1

    if count >= 5:
        break


if count == 0:
    st.warning("この気分に合う曲が見つかりませんでした。")

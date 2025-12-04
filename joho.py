# debug_app.py -- デバッグ用（そのまま貼って実行してください）
import streamlit as st
import requests
import traceback

st.set_page_config(page_title="デバッグ：曲が出ない原因確認", layout="centered")
st.title("デバッグ：曲取得と表示の確認")

st.write("まずは iTunes API に問い合わせて曲データを取得して、その中身を確認します。")

API_URL = "https://itunes.apple.com/search"
params = {
    "term": "official+hige+dandism",
    "country": "JP",
    "media": "music",
    "entity": "song",
    "limit": 50
}

# --- API 呼び出し ---
try:
    r = requests.get(API_URL, params=params, timeout=10)
    st.write(f"HTTP ステータスコード: {r.status_code}")
    data = r.json()
except Exception as e:
    st.error("⚠️ API 呼び出しで例外が発生しました。下の詳細を確認してください。")
    st.text(traceback.format_exc())
    st.stop()

# --- データの構造チェック ---
st.subheader("レスポンスのトップ情報")
st.write("keys:", list(data.keys()))
st.write("結果数 (resultCount):", data.get("resultCount"))

results = data.get("results")
if results is None:
    st.error("レスポンスに 'results' が含まれていません。API のレスポンスを確認してください。")
    st.json(data)
    st.stop()

if not isinstance(results, list):
    st.error("'results' がリストではありません。→ 型: " + str(type(results)))
    st.json(data)
    st.stop()

st.success(f"曲データを {len(results)} 件取得しました。最初の5件を表示します。")

# --- 取得した最初の5件の要点を表示 ---
for i, item in enumerate(results[:5], start=1):
    st.markdown(f"**{i}. {item.get('trackName', '曲名なし')}**")
    st.write(f"- アーティスト: {item.get('artistName')}")
    st.write(f"- アルバム: {item.get('collectionName')}")
    st.write(f"- trackId: {item.get('trackId')}")
    st.write(f"- previewUrl: {item.get('previewUrl') is not None}")
    st.write("---")

# --- 実際に「表示ループ」で5曲表示する（重複チェックあり） ---
st.subheader("実際に画面に表示するテスト（重複除去＋5曲固定）")
displayed = set()
count = 0
for song in results:
    title = song.get("trackName")
    if not title or title in displayed:
        continue

    # 簡易カード表示（画像があれば表示）
    artwork = song.get("artworkUrl100")
    if artwork:
        cols = st.columns([1,3])
        with cols[0]:
            st.image(artwork, width=80)
        with cols[1]:
            st.markdown(f"**{title}**")
            st.write(f"🎤 {song.get('artistName')}")
            st.write(f"⏱ {int(song.get('trackTimeMillis',0)//1000)}秒")
    else:
        st.markdown(f"**{title}** — {song.get('artistName')}")

    displayed.add(title)
    count += 1
    if count >= 5:
        break

if count == 0:
    st.warning("表示できる曲が 0 件でした（重複除去で全てスキップされた可能性あり）。")
else:
    st.success(f"{count} 曲を表示しました。")

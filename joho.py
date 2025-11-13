# app.py
import streamlit as st

st.set_page_config(page_title="気分で音楽おすすめ（髭団ver.）", layout="centered")

st.title("気分で音楽おすすめアプリ（髭団セレクト）")
st.caption("気分または歌詞キーワードで髭団の曲を探します。")

# --- 曲データ（タイトル / アーティスト / 気分 / キーワード） ---
songs = [
    {"title": "Pretender", "artist": "Official髭男dism", "mood": "かなしい", "keywords": "love goodbye night"},
    {"title": "I LOVE…", "artist": "Official髭男dism", "mood": "うれしい", "keywords": "love positive bright"},
    {"title": "Subtitle", "artist": "Official髭男dism", "mood": "かなしい", "keywords": "warm story gentle"},
    {"title": "異端なスター", "artist": "Official髭男dism", "mood": "元気", "keywords": "wild rock strong"},
    {"title": "Stand By You", "artist": "Official髭男dism", "mood": "元気", "keywords": "support care close"},
    {"title": "パラボラ", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "soft float mellow"},
    {"title": "イエスタデイ", "artist": "Official髭男dism", "mood": "かなしい", "keywords": "memory past think anime"},
    {"title": "Cry Baby", "artist": "Official髭男dism", "mood": "怒り", "keywords": "angry conflict fight anime"},
    {"title": "らしさ", "artist": "Official髭男dism", "mood": "元気", "keywords": "new speed fight anime"},
    {"title": "犬かキャットかで死ぬまで喧嘩しよう", "artist": "Official髭男dism", "mood": "うれしい", "keywords": "love future couple"},
    {"title": "Bedloom Tolk", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "Anarchy", "artist": "Official髭男dism", "mood": "怒り", "keywords": "monkey speed study"},
    {"title": "むっちゃんの歌", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "変更点"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
    {"title": "", "artist": "Official髭男dism", "mood": "リラックス", "keywords": "bed night tolk alone"},
]

# --- UI: 気分選択（日本語） ---
mood_choice = st.selectbox("今の気分を選んでください", ["うれしい", "かなしい", "リラックス", "怒り", "元気"])

# 感情に応じたアイコン（簡易の「絵」代わり）
mood_icons = {
    "うれしい": "😊 うれしい",
    "かなしい": "😢 かなしい",
    "リラックス": "🌿 リラックス",
    "怒り": "🔥 怒り",
    "元気": "⚡ 元気"
}
st.markdown(f"**選択中：** {mood_icons.get(mood_choice, '')}")

st.write("---")

# --- AIっぽい簡易スコア方式によるおすすめ（A案） ---
st.subheader("おすすめ（気分に合わせたスコア順）")
if st.button("気分でおすすめを表示"):
    # スコア付けルール（簡易）
    # - 気分が一致したら +2
    # - 曲のキーワードに同じ語があれば +1（今回は気分語とキーワードの一致は薄いが将来拡張可）
    scored = []
    for s in songs:
        score = 0
        if s["mood"] == mood_choice:
            score += 2
        # ここではキーワード一致で加点（後でユーザー履歴などで重み変えられる）
        for kw in s["keywords"].split():
            # 気分語とマッチすることは少ないが一応処理（拡張用）
            if kw == mood_choice:
                score += 1
        scored.append((score, s))
    # スコアでソート（高い順）
    scored.sort(key=lambda x: x[0], reverse=True)

    # 上位を表示（スコア0の曲は「候補」扱い）
    top = [t for sc, t in scored if sc > 0]
    if not top:
        st.write("同じ気分の一致曲がありません。以下は全曲からの提案です。")
        for s in [x[1] for x in scored[:3]]:
            st.write(f"- {s['title']} （{s['artist']}） — キーワード: {s['keywords']}")
    else:
        st.write("おすすめ（上から）：")
        for s in top:
            st.write(f"- {s['title']} （{s['artist']}） — 気分: {s['mood']} / キーワード: {s['keywords']}")

st.write("---")

# --- 歌詞キーワード検索 ---
st.subheader("歌詞（雰囲気）キーワード検索")
keyword = st.text_input("曲の雰囲気を表す単語で検索（例：love / night / relax）")

if st.button("歌詞キーワードで検索"):
    q = keyword.strip().lower()
    if q == "":
        st.write("キーワードを入力してください。")
    else:
        results = []
        for s in songs:
            if q in s["keywords"].lower().split():
                results.append(s)
        if not results:
            st.write("該当する曲は見つかりませんでした。")
        else:
            st.write(f"「{q}」に該当する曲：")
            for r in results:
                st.write(f"- {r['title']} （{r['artist']}） — 気分: {r['mood']} / キーワード: {r['keywords']}")

st.write("---")

# --- 全曲一覧（確認用） ---
if st.checkbox("全曲データを表示する"):
    for s in songs:
        st.write(f"- {s['title']} — アーティスト: {s['artist']} / 気分: {s['mood']} / キーワード: {s['keywords']}")

st.write("")
st.info("使い方：気分を選ぶ → 「気分でおすすめを表示」を押す。歌詞っぽい単語で探したいときは下の検索欄を使ってください。")

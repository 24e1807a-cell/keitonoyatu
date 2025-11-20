import requests
import random

# ▼ 髭男の曲を API から取得する関数
def get_higedan_songs():
    url = "https://itunes.apple.com/search?term=official+hige+dandism&country=jp&media=music&limit=50"
    response = requests.get(url)
    data = response.json()
    return data["results"]

# ▼ 気分ごとのおすすめ条件
def recommend_by_mood(mood, songs):
    mood_keywords = {
        "1": ["happy", "upbeat", "ミックスナッツ", "FIRE", "Stand", "Parabola"],
        "2": ["calm", "ballad", "I LOVE", "宿命", "Pretender"],
        "3": ["cry", "emotional", "Cry", "Laughter", "イエスタデイ"]
    }

    keywords = mood_keywords[mood]

    # 曲名にキーワードが入っているものを探す
    filtered = []
    for s in songs:
        name = s["trackName"]
        for kw in keywords:
            if kw.lower() in name.lower():
                filtered.append(name)

    # 該当曲が無かったらランダム
    if len(filtered) == 0:
        return random.choice(songs)["trackName"]
    else:
        return random.choice(filtered)

# ▼ メイン処理
print("★ 髭男おすすめ曲アプリ（API対応）★")
print("気分を選んでください")
print("1: 元気になりたい")
print("2: 落ち着きたい")
print("3: 泣きたい・感動したい")

choice = input("番号を入力 → ")

# APIから曲を取得
songs = get_higedan_songs()

# おすすめ曲を選択
recommend = recommend_by_mood(choice, songs)

print("\n🎵 あなたへのおすすめ曲は…")
print("➡", recommend)


import requests

TOKEN = "1234"
URL = "http://localhost:3000"
id = 10

def show_match_info():
    try:
        response = requests.get("{}/matches/{}?token={}".format(URL, id, TOKEN))
        response.raise_for_status()  # HTTPエラーチェック
        match_data = response.json()  # JSONデータを取得
        print("取得したJSONデータ:")
        print(match_data)
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")

show_match_info()

import requests

# サーバーのURL
url = 'http://localhost:3000/matches/10'

# クエリパラメータ
params = {'token': '1234'}

# GETリクエストを送信
response = requests.get(url, params=params)

# サーバーからの応答を表示
print("レスポンス内容:", response)
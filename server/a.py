import asyncio
import requests
import json

# サーバーのURL
url = 'http://localhost:3000/matches/10'

# クエリパラメータ
params = {'token': '1234'}

async def my_function():
    # GETリクエストを送信
    response = requests.get(url, params=params)

    # サーバーからの応答を表示
    print("レスポンス内容:", response.json())

async def schedule_function(interval):
    while True:
        await my_function()  # 非同期関数を呼び出す
        await asyncio.sleep(interval)  # 指定の秒数待つ

async def main():
    interval = 5  # 関数を呼び出す間隔（秒）
    await schedule_function(interval)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

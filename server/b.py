import asyncio
import aiohttp
import json

headers = {
    'Content-Type': 'application/json',
}

params = {
    'token': '1234',
}

async def my_function(turn, json_data):
    async with aiohttp.ClientSession() as session:
        # "json_data" を更新
        turn += 1  # "turn" を1ずつ増やす
        json_data['turn'] = turn
        json_data['actions'][0]['type'] = 1
        json_data['actions'][0]['dir'] = 3
        json_data['actions'][1]['type'] = 2
        json_data['actions'][1]['dir'] = 1

        print(turn)
        print(json_data)  # 更新された json_data をプリント
        try:
            request = await session.post('http://localhost:3000/matches/10', params=params, headers=headers, json=json_data)
            if request.status == 200:
                print("Request was successful")
            else:
                print(f"Request failed with status code: {request.status}")
                response_text = await request.text()
                print(f"Response: {response_text}")
        except aiohttp.ClientError as e:
            print(f"Request failed with error: {e}")
        return turn

async def schedule_function(interval, turn, json_data):
    while True:
        turn = await my_function(turn, json_data)  # 非同期関数を呼び出し、"turn" を更新
        await asyncio.sleep(interval)  # 指定の秒数待つ

async def main():
    interval = 15  # 関数を呼び出す間隔（秒）
    turn = 0  # "turn" の初期値
    json_data = {
        'turn': turn,
        'actions': [
            {
                'type': 1,
                'dir': 3,
            },
            {
                'type': 2,
                'dir': 1,
            },
        ],
    }

    await schedule_function(interval, turn, json_data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

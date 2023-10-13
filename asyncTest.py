import asyncio

async def your_function(counter):
    # ここに呼び出したい関数の処理を書く
    print(counter, " First")
    await asyncio.sleep(1)
    print(counter, " Second")

async def periodic_task(interval):
    counter = 0
    while True:
        await your_function(counter)
        await asyncio.sleep(interval)
        counter+=1

# 関数を1秒ごとに呼び出す例
interval_seconds = 10
asyncio.run(periodic_task(interval_seconds))
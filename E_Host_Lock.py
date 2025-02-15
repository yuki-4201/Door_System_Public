import asyncio # type: ignore
import datetime # type: ignore
from random import randint # type: ignore
from realtime import AsyncRealtimeClient # type: ignore

import A_Setting
import G_Servo


# イベントを受信するための設定
url = A_Setting.host_url
key = A_Setting.login_database_Key

# イベント名とチャンネル名
eventName = "RequestForLocking"
channelName = "admin"


# イベントを受信したときの処理
def handle_broadcast(data):
    dt_now = datetime.datetime.now()

    # イベント名が一致しているか確認
    if "event" in data and data["event"] == eventName:
        code = data["payload"]
        user = data["user"]

        # 正規の操作であるかの確認
        if code and code == 424242:
            print(str(dt_now) + "施錠命令受信:施錠します" + user)

            # 施錠処理
            G_Servo.lock("user")

        # 正規の操作でない場合は操作を行わない
        else:
            print(str(dt_now) +"施錠失敗")

    # イベント名が一致しない場合操作を行わない
    else:
        print(str(dt_now) +f"*** 不明なイベントを受信しました:{data}")


# クライアントからのメッセージを受信する
async def listenToBloadcastMessages():
    client = AsyncRealtimeClient(url, key)
    await client.connect()
    channel = client.channel(channelName)
    await channel.on_broadcast(eventName , handle_broadcast).subscribe()
    await client.listen()


# メイン関数
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [listenToBloadcastMessages()]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()
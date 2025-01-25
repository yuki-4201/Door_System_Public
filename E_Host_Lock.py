import asyncio
import datetime
from random import randint
from realtime import AsyncRealtimeClient
import A_Setting
import G_Lock

# イベントを受信するための設定
url = A_Setting.host_url
key = A_Setting.login_database_Key

# イベント名とチャンネル名
eventName = "RequestForLocking"
channelName = "admin"

# イベントを受信したときの処理
def handle_broadcast(data):
    dt_now = datetime.datetime.now()

    #イベント名が一致しているか確認
    if "event" in data and data["event"] == eventName:
        code = data["payload"]
        user = data["user"]

        #コードが一致しているか確認
        if code and code == 424242:
            #sys.stdout = open("_Application_Lock.log", "a")
            print(str(dt_now) + "施錠命令受信:施錠します" + user)
            #sys.stdout = sys.__stdout__

            #施錠処理
            G_Lock.lock("user")
        else:
            #sys.stdout = open("_Application_Lock.log", "a")
            print(str(dt_now) +"施錠失敗")
            #sys.stdout = sys.__stdout__

    else:
        #sys.stdout = open("_Application_Lock.log", "a")
        print(str(dt_now) +f"*** 不明なイベントを受信しました:{data}")
        #sys.stdout = sys.__stdout__

#クライアントからのメッセージを受信する
async def listenToBloadcastMessages():
    client = AsyncRealtimeClient(url, key)
    await client.connect()
    channel = client.channel(channelName)
    await channel.on_broadcast(eventName , handle_broadcast).subscribe()
    await client.listen()

#メイン関数
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [listenToBloadcastMessages()]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()

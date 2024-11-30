import asyncio
import datetime
from random import randint
from realtime import AsyncRealtimeClient
import A_Setting
import H_Unlock
import I_Passcode

#Supabaseの設定
url = A_Setting.host_url
key = A_Setting.login_database_Key

#ブロードキャストの設定
eventName = "RequestForUnlocking"
channelName = "admin"

Systemstart = A_Setting.Systemstart
Systemend = A_Setting.Systemend

#パスコードの設定
newPassCodeInterval = 20
passCode1, passCode2 = None, None

#パスコードを生成する
def randomPassCode():
    return str(randint(1000, 8999))

#パスコードを変更する(直近2つを保持)
def changePassCodes():
    global passCode1, passCode2
    passCode1 = passCode2
    passCode2 = randomPassCode()
    print(f"新しいパスコードが生成されました:{passCode2}")
    I_Passcode.passcode(passCode1,passCode2)


#ブロードキャストを受信したときの処理
def handle_broadcast(data):
    dt_now = datetime.datetime.now()

    #イベント名が一致しているか確認
    if "event" in data and data["event"] == eventName:
        code = data["payload"]
        user = data["user"]
        print(str(dt_now) +f'\t パスコード受信：{code}')

        #パスコードが一致しているか確認
        if code and code == passCode1 or code == passCode2:
            dt_now = datetime.datetime.now()
            nowtime = dt_now.time()

            if nowtime >= Systemstart and nowtime <= Systemend:
                #解錠処理
                H_Unlock.unlock("student")
            else:
                print("時間外労働はお断りします")

        elif user == "teacher":
            print("特別措置")
            H_Unlock.unlock("user")

        else:
            print("*** パスコードが一致しません")

    else:
        print(str(dt_now) +f"*** 不明なイベントを受信しました:{data}")

#新しいパスコードを生成する
async def generatePassCodeContinuously():
    while True:
        changePassCodes()
        await asyncio.sleep(newPassCodeInterval)

#クライアントからのメッセージを受信する
async def listenToBoadcasMessages():
    client = AsyncRealtimeClient(url, key)
    await client.connect()
    channel = client.channel(channelName)
    await channel.on_broadcast(eventName , handle_broadcast).subscribe()
    await client.listen()

#メイン処理
if __name__ == "__main__":
    changePassCodes()
    loop = asyncio.get_event_loop()
    tasks = [generatePassCodeContinuously(), listenToBoadcasMessages()]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()
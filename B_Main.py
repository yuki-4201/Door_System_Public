import datetime
import subprocess
from supabase import create_client
import A_Setting
import D_Suspicious # type: ignore

#動体検知システムを作動させない時間帯の設定
Systemstart = A_Setting.Systemstart
Systemend = A_Setting.Systemend

while True:
    #現在時刻の取得
    dt_now = datetime.datetime.now()
    nowtime = dt_now.time()

    #時間帯によるシステムの切り替え
    if nowtime <= Systemstart and nowtime >= Systemend:
        #動体検知システムを作動
        proc = subprocess.Popen(D_Suspicious)
        proc.communicate

import pigpio
import time
from supabase import create_client
from functools import partial
import A_Setting

#supabaseにアクセスできるようにする
PROJECT_URL = A_Setting.PROJECT_URL
API_KEY = A_Setting.API_KEY
supabase = create_client(PROJECT_URL, API_KEY)

#サーボモーターの設定
SERVO_PIN = 18
pi = pigpio.pi()

#サーボモーターの準備
def set_angle(angle):
	assert 0 <= angle <= 180.
	pulse_width = (angle / 180) * (2500 - 500) + 500
	pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
def afrer(n, started):
	return time.time() - started > n

def unlock(user):
	#sys.stdout = open("_Application_Unlock.log", "a")
	#データベースのテーブル名を取得
	listname3 = A_Setting.listname3
	listname4 = A_Setting.listname4

	#ドアの状態を取得
	Door_Log_datalist = supabase.table(listname3).select("*").execute()
	Door_list=[f"{user['door']}" for user in Door_Log_datalist.data]
	Door_list= [s for s in Door_list if s != '操作なし']
	Door_condition = (Door_list[0])

	#ドアの状態によって処理を変更
	if Door_condition == "施錠":
		set_angle (0)
		message_door="解錠"
		print ("認証されたユーザーです。ドアを解錠します。\n")

	else:
		print ("認証されたユーザーです。ドアは解錠されているため追加の操作を行いません。\n")
		message_door="操作なし"

	#ログを記録
	message_log =  "認証済"
	UserName = user + "_Application"
	logdata = {"username": UserName,"certification": message_log, "door":message_door }
	supabase.table(listname4).insert(logdata).execute()
	return True
	#sys.stdout = sys.__stdout__


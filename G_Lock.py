import pigpio # type: ignore
from supabase import create_client # type: ignore
from functools import partial # type: ignore

import A_Setting

# supabaseにアクセスできるようにする
PROJECT_URL = A_Setting.PROJECT_URL
API_KEY = A_Setting.API_KEY
supabase = create_client(PROJECT_URL, API_KEY)

# サーボモーターの設定
SERVO_PIN = 18
pi = pigpio.pi()

# サーボモーターの準備
def set_angle(angle):
	assert 0 <= angle <= 180.
	pulse_width = (angle / 180) * (2500 - 500) + 500
	pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

def lock(user):
	# データベースのテーブル名を取得
	listname1 = A_Setting.listname1
	listname2 = A_Setting.listname2

	# ドアの状態を取得
	Door_Log_datalist = supabase.table(listname1).select("*").execute()
	Door_list=[f"{user['door']}" for user in Door_Log_datalist.data]
	Door_list= [s for s in Door_list if s != '操作なし']
	Door_condition = (Door_list[0])

	# 通常操作
	if Door_condition == "解錠":
		set_angle (95)
		message_door="施錠"
		print ("認証されたユーザーです。ドアを施錠します。\n")
	
	# 定時操作
	elif user == "定時操作":
		set_angle (95)
		message_door="施錠"
		print ("定時操作を行います。\n")
	
	# 鍵がすでに施錠されている場合
	else:
		print ("認証されたユーザーです。ドアは施錠されているため追加の操作を行いません。\n")
		message_door="操作なし"

	# ログを記録
	message_log =  "認証済"
	logdata = {"username": user,"certification": message_log, "door":message_door }
	supabase.table(listname2).insert(logdata).execute()

	return True

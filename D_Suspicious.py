import discord # type: ignore
import aiohttp
import asyncio
import datetime
import cv2 # type: ignore
import cv2 as cv # type: ignore
from discord import Webhook # type: ignore
import A_Setting
import G_Lock

#discordのwebhookのURL
webhook_url = A_Setting.webhook_url

#時間の設定
start = A_Setting.Systemstart
end = A_Setting.Systemend

#カメラで撮影用
camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
DELTA_MAX = 255
DOT_TH = 20
MOTHON_FACTOR_TH = 0.20
avg = None

#現在の時刻を取得
dt_now = datetime.datetime.now()
now = dt_now.time()
count = 0

while now < start or now >end:
	if count == 0:
		G_Lock.lock("定時操作")
		print("定時操作")
		count = 1
	#現在の時刻の更新
	dt_now = datetime.datetime.now()
	#sys.stdout = open("_System.log", "a")
	print(dt_now)
	now = dt_now.time()

	#カメラの画像を取得
	ret,frame =camera.read()
	motion_detected = False
	dt_now = datetime.datetime.now() #データを取得した時刻

    # モノクロにする
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    #比較用のフレームを取得する
	if avg is None:
		avg = gray.copy().astype("float")
		continue

    # 現在のフレームと移動平均との差を計算
	cv.accumulateWeighted(gray, avg, 0.6)
	frameDelta = cv.absdiff(gray, cv.convertScaleAbs(avg))

    # デルタ画像を閾値処理を行う
	thresh = cv.threshold(frameDelta, DOT_TH, DELTA_MAX, cv.THRESH_BINARY)[1]

    #モーションファクターを計算する。全体としてどれくらいの割合が変化したか。
	motion_factor = thresh.sum() * 1.0 / thresh.size / DELTA_MAX
	motion_factor_str = '{:.08f}'.format(motion_factor)

    #モーションファクターがしきい値を超えていれば動きを検知したことにする
	if motion_factor > MOTHON_FACTOR_TH:
		motion_detected = True

    # 動き検出していれば画像を保存する
	if motion_detected  == True:
		title="DoorAleart.jpeg"
		cv.imwrite(title, frame)
		img = cv2.imread('DoorAleart.jpeg')
		img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
		cv2.imwrite(title, img_rotate_180)
		print(title)
		dt_now = datetime.datetime.now()

		#メッセージの詳細
		username = A_Setting.username
		title = (dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
		description = A_Setting.description2
		color_hex = A_Setting.color_hex
		image_path = "DoorAleart.jpeg"
		pathid = "DoorAleart.jpeg"

		#discordに画像を送信する
		file = discord.File(image_path, filename="DoorAleart.jpeg")
		embed = discord.Embed(
			title=title, description=description, color=int(color_hex, 16)
		).set_image(url="attachment://"+pathid)
		async def foo():
			async with aiohttp.ClientSession() as session:
				webhookdata = Webhook.from_url(webhook_url, session=session)
				await webhookdata.send(username=username, embed=embed, file=file)
		asyncio.run(foo())
		#sys.stdout = sys.__stdout__

	key = cv.waitKey(1)

	#ESCキーが押されたら終了する
	if key == 27:
		break

count = 0
camera.release()
cv.destroyAllWindows()

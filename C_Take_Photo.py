import discord # type: ignore
import aiohttp
import asyncio
import cv2 # type: ignore
import datetime
from discord import Webhook # type: ignore
import A_Setting

#discordのwebhookのURL
webhook_url = A_Setting.webhook_url

#カメラで撮影用
camera = cv2.VideoCapture(0)
count_number = 0

#フレーム設定
ret,frame =camera.read()
motion_detected = False

#データを取得した時刻
dt_now = datetime.datetime.now()

#ファイル名と、画像中に埋め込む日付時刻
dt_format_string = dt_now.strftime('%Y-%m-%d %H:%M:%S')

# 動き検出していれば画像を保存する
if 1+1 == 2:
	title="DoorAleart.jpeg"
	cv2.imwrite(title, frame)
	print(title + "\n")

	#メッセージの詳細
	username = A_Setting.username
	title = (dt_now.strftime('%Y/%m/%d  %H:%M:%S') + "不審者が確認されました")
	description = A_Setting.description1
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

	count_number +=1

	key = cv2.waitKey(1)



count_number -=1

camera.release()
cv2.destroyAllWindows()

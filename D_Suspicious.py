import aiohttp # type: ignore
import asyncio # type: ignore
import cv2 # type: ignore
import datetime # type: ignore
import discord # type: ignore
import smtplib # type: ignore
import cv2 as cv # type: ignore
from discord import Webhook # type: ignore
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import A_Setting
import G_Servo


# メールの送信設定
SELF_MAIL_ADDRESS = A_Setting.SELF_MAIL_ADDRESS
SELF_MAIL_PASSWORD = A_Setting.SELF_MAIL_PASSWORD
SELF_SMTP_SERVER = 'smtp.gmail.com'
SELF_SMTP_PORT = 587

# discordのwebhookのURL
webhook_url = A_Setting.webhook_url

# discordまたはmailのいづれかから送信先の選択
select_function = A_Setting.select_function

# 起動時間の設定
start = A_Setting.Systemstart
end = A_Setting.Systemend

# カメラの撮影設定
camera = cv.VideoCapture(0)

# エラーメッセージ
if not camera.isOpened():
    print("Error: カメラを開けませんでした")
    exit(0)

camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
DELTA_MAX = 255
DOT_TH = 20
MOTHON_FACTOR_TH = 0.001
avg = None

# 現在の時刻を取得
dt_now = datetime.datetime.now()
now = dt_now.time()
count = 0


# 通知メールを生成する関数
def create_mail(mail_subject, mail_body, mail_from, mail_to, attach_filename = None):
    # 添付ファイル名の指定有無により切り分け
    if attach_filename == None:
        mail_message = MIMEText(mail_body)
    else:
        mail_message = MIMEMultipart()

        # 本文
        mail_message.attach(MIMEText(mail_body, "plain"))

        try:
            # 添付ファイル名が指定されている場合、ファイルを読み込む
            with open(attach_filename, 'rb') as attach_File:
                att = MIMEBase('application', 'octet-stream')
                att.set_payload(attach_File.read())

        except Exception as e:
            # 指定された添付ファイルが読み込めなかった場合は、ログを吐いて終了
            print(f'Error:{e}')
            exit(0)        

        # 添付ファイルをbase64エンコードして添付
        encoders.encode_base64(att)
        att.add_header('Content-Disposition', f'attachment; filename={attach_filename}')
        mail_message.attach(att)

    # 送信メールを編集
    mail_message['Subject'] = mail_subject
    mail_message['From'] = mail_from
    mail_message['To'] = mail_to
    mail_message['Date'] = formatdate(localtime=True)        

    return mail_message


# メールの操作心を行う関数
def send_mail(mail_message, mail_to):
    try:
        smtp = smtplib.SMTP(SELF_SMTP_SERVER, SELF_SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(SELF_MAIL_ADDRESS, SELF_MAIL_PASSWORD)
    
        smtp.sendmail(SELF_MAIL_ADDRESS, mail_to, mail_message.as_string())
    except Exception as e:
        print(f'Error:{e}')
    finally:
        smtp.quit()


# 事前に設定された時間内のみ不審者通知を行う
while now < start or now >end:
	if count == 0:
		G_Servo.lock("定時操作")
		print("定時操作")
		count = 1

	# 現在の時刻の更新
	dt_now = datetime.datetime.now()
	print(dt_now)
	now = dt_now.time()

	# カメラの画像を取得
	ret,frame =camera.read()
	motion_detected = False
	dt_now = datetime.datetime.now()

	# エラーメッセージ
	if not ret:
		print("Error: カメラからフレームを取得できませんでした")
		exit(0)

    # モノクロにする
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 比較用のフレームを取得する
	if avg is None:
		avg = gray.copy().astype("float")
		continue

    # 現在のフレームと移動平均との差を計算
	cv.accumulateWeighted(gray, avg, 0.6)
	frameDelta = cv.absdiff(gray, cv.convertScaleAbs(avg))

    # デルタ画像を閾値処理を行う
	thresh = cv.threshold(frameDelta, DOT_TH, DELTA_MAX, cv.THRESH_BINARY)[1]

    # モーションファクターを計算する。全体としてどれくらいの割合が変化したか。
	motion_factor = thresh.sum() * 1.0 / thresh.size / DELTA_MAX
	motion_factor_str = '{:.08f}'.format(motion_factor)

    # モーションファクターがしきい値を超えていれば動きを検知したことにする
	if motion_factor > MOTHON_FACTOR_TH:
		motion_detected = True

    # 動き検出していれば画像を保存する
	if motion_detected  == True:

		# 2回撮影を行い2回目に撮影したものを使用することで白飛びを防ぐ
		for i in range(2):
			title="DoorAleart.jpeg"
			cv.imwrite(title, frame)
			img = cv2.imread('DoorAleart.jpeg')
			img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
			cv2.imwrite(title, img_rotate_180)
			print(title)
			dt_now = datetime.datetime.now()
        
		# メールを用いた不審者通知を行う
		if select_function == "mail":
			if __name__ == '__main__':
				dt_now = datetime.datetime.now()
				time = dt_now.strftime('%Y/%m/%d %H:%M:%S')

				# メールの内容
				mail_to = A_Setting.mail_to
				
				# メールの件名
				mail_subject = '《重要》探究ラボにて不審者が検知されました。'
				
				# メールの本文
				mail_body = 'このメールアドレスは送信専用です。お問い合わせ等は下記のメールアドレスにお願いします。\n'+time + 'にて不審者が確認されました。撮影した写真を添付します。\nこのシステムの精度は100%ではありません。誤報の可能性に注意しいてください。\n\nKenryo Steam\n\n\n\n ____________________\n縣陵探究科6期生 三澤陽\nkenryo-steam-lab@yuki4201.uk\n____________________'
				
				# 添付ファイル名
				mail_att = 'DoorAleart.jpeg'

				# 送信メールを作成する(添付ファイル付き)
				mail_message = create_mail(mail_subject, mail_body, SELF_MAIL_ADDRESS, ', '.join(mail_to), mail_att)
				
				# メールを送信する
				send_mail(mail_message, mail_to)
		
		# Discordを用いた不審者通知を行う
		elif select_function == "discord":

			# メッセージの詳細s
			username = A_Setting.username
			title = (dt_now.strftime('%Y/%m/%d  %H:%M:%S') + "不審者が確認されました")
			description = A_Setting.description1
			color_hex = A_Setting.color_hex
			image_path = "DoorAleart.jpeg"
			pathid = "DoorAleart.jpeg"

			# Discordに画像を送信する
			file = discord.File(image_path, filename="DoorAleart.jpeg")
			embed = discord.Embed(
				title=title, description=description, color=int(color_hex, 16)
			).set_image(url="attachment://"+pathid)
			async def foo():
				async with aiohttp.ClientSession() as session:
					webhookdata = Webhook.from_url(webhook_url, session=session)
					await webhookdata.send(username=username, embed=embed, file=file)
			asyncio.run(foo())

	key = cv.waitKey(1)

	# ESCキーが押されたら終了する
	if key == 27:
		break


count = 0
camera.release()
cv.destroyAllWindows()

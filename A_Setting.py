import datetime
import os
from dotenv import load_dotenv # type: ignore
from supabase import create_client # type: ignore

# .env ファイルをロード
load_dotenv()

# Supabaseのリンク
PROJECT_URL = os.getenv("PROJECT_URL")
API_KEY = os.getenv("API_KEY")
supabase = create_client(PROJECT_URL, API_KEY)

#supabaseの設定情報を入力したテーブルを取得
settingdata = supabase.table("setting").select("*").execute()
data ,_= settingdata
settinglist = { d['Item_name']:d for d in data[1]}

#DiscordのWebhook URL
webhook_url = settinglist['webhook_url']['1']

#不審者検知を行いたい時間
Systemstart = datetime.time(int(settinglist['Systemstart']['1']),int(settinglist['Systemstart']['2']),int(settinglist['Systemstart']['3']))
Systemend = datetime.time(int(settinglist['Systemend']['1']),int(settinglist['Systemend']['2']),int(settinglist['Systemend']['3']))

#Disccordのユーザー名
username = settinglist['username']['1']

#認証失敗時のメッセージ
description1 = settinglist['description1']['1']

#tablename
listname1, listname2 = settinglist['listname']['1'], settinglist['listname']['2']

#動体検知に引っかかったときのメッセージ
description2 = settinglist['description2']['1']
color_hex = settinglist['color_hex']['1']

#アプリに使用してるデータベースのURLとAPI_Key
login_database_URL = settinglist['supabase_Authentication']['1']
login_database_Key = settinglist['supabase_Authentication']['2']
host_url = settinglist['host_url']['1']

#メールの設定
SELF_MAIL_ADDRESS = settinglist['email_setting']['1']
SELF_MAIL_PASSWORD = settinglist['email_setting']['2']
mail_to01, mail_to02, mail_to03 = settinglist['mail_to']['1'], settinglist['mail_to']['2'], settinglist['mail_to']['3']
mail_to = [mail_to01, mail_to02, mail_to03]
mail_to.remove(None)

#機能の指定(mail or discord)
select_function = settinglist['email_setting']['3']


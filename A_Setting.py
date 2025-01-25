import datetime
from supabase import create_client

#Supabaseのリンク
PROJECT_URL = URL
API_KEY = KEY
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

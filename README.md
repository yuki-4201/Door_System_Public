# Smart Door System


### 概要
このプロジェクトはRaspberry Piを用いて安価でカスタマイズ性の高いスマートロックシステムの実現を目的として活動してきました。具体的な機能としては不審者通知システムと鍵の解錠・施錠を行うシステムの2つに分かれています。


### 使用技術一覧
* ##### 言語
  * python
  * Flutter(別のレポジトリにて使用しています)
* ##### サービス
  * Supabase
  * Discord
  * Email
* ##### 使用したライブラリ
  * aiohttp
  * asyncio
  * discord
  * load_dotenv
  * opencv
  * pigpio
  * supabase
  * SPI
* ##### 使用した機材
  * Raspberry Pi4(4GB RAM)
  * Webカメラ(EMEET C960)
  * サーボモータ(MG996R)
  * LCDモジュール(ILI9341)


### 環境構築
* パッケージのインストール
```
pip install aiohttp
pip install asyncio
pip install discord
pip install load_dotenv
pip install opencv-python
pip install pigpio
pip install supabase
```
* プロジェクトのクローン
```
git clone git@github.com:yuki-4201/door_system-development.git
```
※自動実行などについては各自で調べて設定してください。


### 各プログラムの動作
* ```.env```
  > SupabaseのプロジェクトURLとAPI KEYを定義します。

* ```A_Setting.py```
  > Supabaseから設定情報の取得を行います。

* ```B_Main.py```
  > 不審者通知システムの起動を行います。
  > Supabaseにて設定した時間内のみ```D_Suspiciout.py```を呼び出します。

* ```C_Take_Photo.py```
  > 不審者通知システムの動作確認用のコードです。
  > このコードを実行するとSupabaseにて設定された送信元から指定されたメールアドレスにドアの前の写真を送信します。メールアドレスは最大3つまで設定可能です。

* ```D_Suspicious.py```
  > 不審者通知システムのコードです。discordへの通知またはメールを利用した通知に対応しています。それぞれの設定はSupabaseで行うことができます。また、このシステムは起動時に施錠操作を行います。

* ```E_Host_Lock.py```
  > webアプリからの施錠命令を受信します。受信した際に```G_Lock.py```を呼び出し施錠操作を行います。
  > 操作結果をSupabaseに記録します。

* ```F_Host_Unlock.py```
  > webアプリからの解錠命令を受信します。また、10秒ごとに```I_Passcodeを```呼び出しパスコードを発行することによってセキュリティ性を保ちます。
  > 解錠命令を受信した際はwebアプリ側で定義している所属Groupによって動作が異なります。解錠操作は```H_Unlock.py```を呼び出して行います。
  > また、解錠操作を行なった場合も行なっていない場合もSupabaseに操作を行なったアカウントのメールアドレスと操作内容、操作時間などを記録します。
  >
  >> ###### Group Teacher
  >> 常時鍵の解錠を行うことができます。また、パスコードの入力が不要です。
  >>
  >> ###### Group Students
  >> Supabaseで定義された時間の間のみ鍵の解錠を行うことができます。
  >> 解錠操作を行うためには4桁のパスコードの入力が必要です。

* ```G_Servo.py```
  > 鍵の操作を行うプログラムです。初期設定にて16、17行目の```lockangle = 95```(施錠操作の際の角度),```unlockangle = 0```(解錠操作の際の角度)の調整を行う必要があります。

* ```H_Passcode.py```
  > LCDディスプレイに接続し、```F_Host_Unlock.py```で生成したパスコードを表示します。
  > 45行目から48行目にてディスプレイに表示する内容を変更することができます。

※各システムの実行に必要なファイル
| システム名 | プログラムファイル | 
| --- | --- | 
| 不審者通知システム | ```A_Setting.py, B_Main.py, D_Take_Photo.py, G_Servo.py``` | 
| 施錠システム | ```A_Setting.py, E_Host_Lock.py, G_Servo.py``` | 
| 解錠システム | ```A_Setting.py, F_Host_Unlock.py, G_Servo.py, I_Passcode.py``` | 
| 動作確認 | ```A_Setting.py, C_Take_Photo.py``` | 


### バージョン情報
> ##### ver1.3.0
> システムの修正が完了
> DoorSystem(Python側)のリリース

> ##### ver1.2.4(修正パッチ ver1.2.4.3)
> ```G_Lock.py```と```H_Lock.py```を統合
> ```I_Passcode.py```を```h_Passcode.py```へ名称変更

> ##### ver1.2.3(修正パッチ ver1.2.3.1)
> ```README.md```への加筆
> 全てのファイルに対しコメントアウトの修正

> ##### ver1.2.2
> ```README.md```の追加

> ##### ver1.2.1
> 使用するライブラリの整理

> ##### ver1.2.0
> Cameraシステムの変更

> ##### ver1.1.0
> メール関係の設定をSupabaseで行うことができるように変更

> ##### ver1.0.0
> レポジトリの作成

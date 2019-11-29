xim
---
Overview
---

プロキシをいちいち設定するのが面倒なので私用に作りました。<br>
名前をつけたプロキシのデータを作成して、名前ごとに設定、管理するCLIです。<br>
動作環境: Windows

Requirement
---
Python Fire https://github.com/google/python-fire

Usage
---
```shell script
xim set proxy school http://example.com https://example.com
xim shells set git,npm,pip
xim set school  # run shell and proxy set.

xim help
```

Install
---
```shell script
git clone https://github.com/satoooon8888/xim.git
pip install -r requirements.txt
```
ダウンロードしたファイルにPATHを通しておいて下さい。

Add User Shell
---
1. xim.config.jsonの"shells"に追加したいシェルをキーを"名前"、値をTrueで追加してください。<br>
2. \shells内に名前.cmdで追加したいシェルを作成してください。<br>
第一引数にhttp、第二変数にhttpsのURLが与えられます。<br>

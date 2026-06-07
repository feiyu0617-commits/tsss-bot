import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 這裡請放入你的選股邏輯函式 (run_tsss_alert)
# 為了節省空間，請把你原本那一大段 def run_tsss_alert(): ... 的程式碼完整貼在這個位置
# 確保這些 import (yfinance, pandas 等) 也在檔案最上方

app = Flask(__name__)

# 請去 LINE Developers 控制台，找到 Messaging API 分頁取得這兩組鑰匙
line_bot_api = LineBotApi('你的_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('你的_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "查詢":
        # 呼叫你的選股函數
        result = run_tsss_alert() 
        msg = f"TSSS報告: {result['scenario']}，建議配置: {result['w_lever']}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run()

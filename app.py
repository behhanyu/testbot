# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
# 載入LineBot所需要的套件
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'TuWwNdW0ZSpc+bYs/tiW2eSNy2OHbJCQ9Ry0/BRrNrKGEBIkpByKcZek6p1G05VTPQZZpKrmYUNX5AhFvRrwglntt6CKb2XYyEXafpWmyEYTtBtLNZeb1q4B1hXLobHJUeHUgBsS4ghbICyGJoiAMwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('31092f163fbb7a9bd6af2e1d6c0bde4b')

line_bot_api.push_message(
    'Uf98cfa672a8785aa0b0d6bbd458a5bef', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request


@ app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####


@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

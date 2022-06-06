# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第四章 選單功能
按鈕樣板TemplateSendMessage
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('TuWwNdW0ZSpc+bYs/tiW2eSNy2OHbJCQ9Ry0/BRrNrKGEBIkpByKcZek6p1G05VTPQZZpKrmYUNX5AhFvRrwglntt6CKb2XYyEXafpWmyEYTtBtLNZeb1q4B1hXLobHJUeHUgBsS4ghbICyGJoiAMwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('31092f163fbb7a9bd6af2e1d6c0bde4b')

line_bot_api.push_message('Uf98cfa672a8785aa0b0d6bbd458a5bef', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if isinstance(event, MessageEvent):
        if event.message.text == "告訴我秘密":
            buttons_template_message = TemplateSendMessage(
            alt_text='這個看不到',
            template=ButtonsTemplate(
                title='Menu',
                text='請選擇類型',
                actions=[
                    PostbackTemplateAction(
                        label='酒吧',
                        display_text='酒吧',
                        data='A酒吧'
                    ),
                    PostbackTemplateAction(
                        label='旅館',
                        display_text='旅館',
                        data='A旅館'
                    ),
                    PostbackTemplateAction(
                        label='全都要',
                        display_text='全都要',
                        data='A全都要'
                    )
                ]
            )
        )
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
    if postback.data=='A酒吧':
        flex_message = TextSendMessage(text='以下有雷，請小心',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="別按我", text="你按屁喔！爆炸了拉！！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！"))
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)

        
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

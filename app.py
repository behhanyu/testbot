# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第四章 選單功能
按鈕樣板TemplateSendMessage
"""
# 載入LineBot所需要的套件
import os
from tryfunction import *
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
line_bot_api = LineBotApi(
    'TuWwNdW0ZSpc+bYs/tiW2eSNy2OHbJCQ9Ry0/BRrNrKGEBIkpByKcZek6p1G05VTPQZZpKrmYUNX5AhFvRrwglntt6CKb2XYyEXafpWmyEYTtBtLNZeb1q4B1hXLobHJUeHUgBsS4ghbICyGJoiAMwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('31092f163fbb7a9bd6af2e1d6c0bde4b')

line_bot_api.push_message(
    'Uf98cfa672a8785aa0b0d6bbd458a5bef', TextSendMessage(text='你可以開始了'))

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

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####


@handler.add(FollowEvent)
def handle_follow(event):
    buttons_template_message = TemplateSendMessage(
        alt_text='這個看不到',
        template=ButtonsTemplate(
            thumbnail_image_url='https://www.posist.com/restaurant-times/wp-content/uploads/2017/04/neon-170182_1920-768x510.jpg',
            title='今晚去哪瑟瑟',
            text='幫你找到最適合的酒吧或旅館，度過激情四射的夜生活！',
            actions=[
                MessageAction(
                    label='點我開始！',
                    text='開始'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "開始":
        flex_message = TextSendMessage(text='請選擇此刻的心情吧~',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(
                                               label="歡樂", text="歡樂", data='A&歡樂')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="憂鬱", text="憂鬱", data='A&憂鬱')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="低調", text="低調", data='A&低調')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="奢侈", text="奢侈", data='A&奢侈')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="活力", text="活力", data='A&活力')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="慵懶", text="慵懶", data='A&慵懶'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        message = event.message.text
        result = location(place_type)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=result))


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data[0:1] == "A":
        mood = event.postback.data[2:]
        buttons_template_message = TemplateSendMessage(
            alt_text='這個看不到',
            template=ButtonsTemplate(
                thumbnail_image_url='https://yhangry.com/wp-content/uploads/2021/11/Wine-1.jpg',
                title='今晚想去哪裡色色？',
                text='請選擇類型',
                actions=[
                    PostbackTemplateAction(
                        label='酒吧',
                        display_text='酒吧',
                        data='B&'+mood+'bar'
                    ),
                    PostbackTemplateAction(
                        label='旅館',
                        display_text='旅館',
                        data='B&'+mood+'hotel'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.postback.data[0:1] == "B":
        place_type = event.postback.data[4:]
        result = event.postback.data[2:].split('&')
        message = TextSendMessage(text=location(result[1]))
        line_bot_api.reply_message(
            event.reply_token, message)



# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

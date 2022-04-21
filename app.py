from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import re

app = Flask(__name__)

line_bot_api = LineBotApi(
    'iBqRd5lyQOdBIDD+gvgBGEpXkj0sybsgLKlSfAU9/QylW3OXFqMArYP02/7paCg6A8DdLIa59TrwXLxkuWYIEnul8U5LFKWBXpeH5XGqqmx3GmWdTADJ/crLCH42t8BydKsdBzzgwWd8oNnI7zPvMAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6a03ea922ed3c6e718b1ca4ac9f0897f')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 主要編輯程式的地方
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.push_message(
        'U84943d789c8a5078719df90a57144b1b', TextSendMessage(text='請開始你的表演'))
    message = event.message.text

    if re.match("你是誰啊", message):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("我是上帝安琪拉"))

    else:
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

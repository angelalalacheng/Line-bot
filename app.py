from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
)

import os
import re
import requests
import pandas as pd
from urllib.request import urlopen
import json
import numpy
import pandas as pd
from bs4 import BeautifulSoup

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


line_bot_api.push_message(
    'U84943d789c8a5078719df90a57144b1b', TextSendMessage(text='趕快來查查看今天股票資訊吧\n股市代碼表:https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'))


# stock function
def stock(stockname):
    # df = pd.read_excel("stocknumber.xlsx")

    # choose1 = (df['name'] == stockname)
    # if choose1.any():
    #     num = str(int(df[choose1]['number']))
    # else:
    #     choose2 = (df['number'] == numpy.int64(stockname))
    #     print(choose2)
    #     if choose2.any():
    #         num = stockname
    #     else:
    #         return "No company!"

    num = stockname
    stock_list = 'tse_'+num+'.tw'

    #　query data
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + stock_list
    res = requests.get(query_url, headers={
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "lxml")
    data = json.loads(soup.p.string)
    # 用到的欄位: c(代號)、n(公司)、o(開盤價)、h(最高價)、l(最低價)、y(昨日收盤價)
    try:
        Dict = data['msgArray'][0]  # type:dict
        reply = Dict["n"]+'\n'+"開盤價:"+Dict["o"]+'\n'+"最高價:" + \
            Dict["h"]+'\n'+"最低價:"+Dict["l"]+'\n'+"昨日收盤價:"+Dict["y"] + \
            '\n\n股市代碼表:https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        return reply
    except:
        return "沒有這間公司喔!再輸入一次"


def intro():
    intro = "大家好~我是Angela\n\n人格特質:\n‧resourceful\n‧broad-minded\n‧curious\n\n社團經驗:\n‧2021新生知訊網執行長\n‧親善大使公關進修組組長\n‧GDSC\n‧竹友會\n‧系上返服/迎新\n\nSideProject:\n‧專題\n‧類神經網路\n‧Line Bot\n‧Chat room(昨天寫完..)\n\n希望自己有機會可以成為Line的一份子~"
    return intro


# 主要編輯程式的地方

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if re.match("關於作者", msg):
        reply = intro()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply))

    else:
        reply = stock(msg)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    sticker_message = StickerSendMessage(
        package_id='11539', sticker_id='52114118')
    line_bot_api.reply_message(event.reply_token, sticker_message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

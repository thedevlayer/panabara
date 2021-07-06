import pandas as pd
from django.apps import AppConfig
import FinanceDataReader as fdr
import pyupbit as pu
import datetime
import os

import json
import urllib.request

# class MyAppConfig():
#     pass
#     print("my app config...")

# def my_function():

#     print("test test test ")

# if __name__ == "__main__":https://finance.naver.com/api/sise/etfItemList.nhn
#     my_function()

def getUseonju():
    currentPath = os.getcwd()
    filepath = currentPath+"\\examples\\uploadfiles\\UseonjuList.txt"
    # 탭으로 분리된(tsv) .txt 텍스트파일 불러오기
    # data = pd.read_csv('파일경로', sep = "\t", , engine='python', encoding = "인코딩방식")
    data = pd.read_csv(filepath, sep = "\t")
    print(data)



def getETFlist():
    import json
    import urllib.request

    url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
    raw_data = urllib.request.urlopen(url).read().decode('CP949')
    json_data = json.loads(raw_data)

    print('etf list size : ' , len(json_data))
    for each in json_data['result']['etfItemList']:
        print(each['itemcode'], each['itemname'])


def DCTEST(self):
    print('ddcccccccccccccccccccccccccccccccc')

    import FinanceDataReader as fdr
    import datetime
    import pandas as pd 

    now = datetime.datetime.now()
    now_before_5 = now - datetime.timedelta(days=365)
    print('now_before_5 : ',now_before_5)

    #코스피
    ks11 = fdr.DataReader('KS11', now_before_5)
    print(ks11)
    # print(ks11['Close'].tolist())


    df=pd.DataFrame(ks11)
    ts_list = df.index.tolist()  # a list of Timestamp's
    date_list = [ ts.date() for ts in ts_list ]  # a list of datetime.date's
    date_str_list = [ str(date) for date in date_list ]  # a list of strings

    print(df['Close'].tolist())
    print(date_str_list)



# #다우존스
# dji = fdr.DataReader('DJI', now_before_5)
# print(dji)

# # FX 환율, 1995 ~ 현재
# usdkrw = fdr.DataReader('USD/KRW', now_before_5) # 달러 원화
# print(usdkrw)


# # Bitcoin KRW price (Bithumbs), 2016 ~ Now
# btc = fdr.DataReader('BTC/KRW', now_before_5)
# print(btc)


# ########################## 업비트 현재가 가져오기
# import pyupbit
# print(pyupbit.Upbit)

# tickers = pyupbit.get_tickers()
# print(tickers)

# #모든 티커들 불러오기
# tickers = pyupbit.get_tickers(fiat="KRW")
# print(tickers)


# #현재가 불러오기
# price = pyupbit.get_current_price("KRW-XRP")
# price = pyupbit.get_current_price("KRW-BTC")

# print('KRW-XRP : ',price)
# print('KRW-BTC : ',price)



# ############################### 야후 파이낸스 현재가 가져오기
# # https://junyoru.tistory.com/129

# import yfinance as yf

# import datetime
 
# now = datetime.datetime.now()
# now_before_5 = now - datetime.timedelta(days=5)
# print(now_before_5)  # 2021-04-14 21:15:54.891525

# df = yf.download(['005930.KS','032620.KQ','BE','AAPL','sfsfsadfe'],start = now_before_5)

# print(df)
# print('-------------------호출-------------------------------------------------------------------------------')


# df = df['Close']
# print(df)
# print('--------------------바로 위의 데이터값으로 채우기------------------------------------------------------------------------------')


# df = df.fillna(method="ffill") #바로 위의 데이터값으로 채우기(보간)
# print(df)


# # 마지막 값만 가져오기
# print('------------------마지막 값만 가져오기--------------------------------------------------------------------------------')
# df = df.iloc[-1]
# print(df)



# print('-------------------환율 정보-------------------------------------------------------------------------------')

# from bs4 import BeautifulSoup
# import urllib.request as req

# # HTML 가져오기
# url = "http://finance.naver.com/marketindex/"
# res = req.urlopen(url)

# # HTML 분석하기
# soup = BeautifulSoup(res, "html.parser")

# #원하는 데이터 추출하기
# price = soup.select_one("div.head_info > span.value").string
# print(price)
# print("usd/krw = ",price)


# # DB select 
# from examples.models import StockBaseInfo
# import os

# os.environ['DJANGO_SETTINGS_MODULE'] = 'setup/settings'

# print(StockBaseInfo.objects.all())



if __name__ == "__main__":
    getUseonju()


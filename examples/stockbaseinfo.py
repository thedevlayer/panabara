import pandas as pd
from django.apps import AppConfig
import FinanceDataReader as fdr
import pyupbit as pu
import datetime
import os

import json
import urllib.request


# def get_kor_stock_all_list(request):
#     dfstockcode = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

#     dfstockcode = dfstockcode[['회사명', '종목코드']]
#     dfstockcode = dfstockcode.rename(columns={'회사명':'name', '종목코드':'code'})

#     print(dfstockcode)

# get_kor_stock_all_list()


class MyAppConfig(AppConfig):

    print('=== MyAppConfig start ===')


    name = 'examples'
    verbose_name = "My App"
    
    ready_has_run = False


    
    init = True

    def ready(self):
        # TODO: Write your codes to run on startup
        

        print('=== ready start ===')

        if self.ready_has_run:
            return

        # Do your stuff here, and then set the flag

        
        

        from examples.models import StockBaseInfo

        baseinfostarttime = datetime.datetime.now()
        
        # 기존 종목 리스트 삭제(서버 구동시 삭제 후 재적재)
        # StockBaseInfo.objects.all().delete()


        # 코스피, 코스닥, 코넥스 전체 목록 불러오기

        # 방법 1) FinanceDataReader 에서 가져옴
        # df = getFinanceDataList() #  모든 종목 리스트 가져오기
        # if df is not None:
        #     # StockBaseInfo.objects.all().delete()
        #     saveStockBaseInfo(self,df)

        # 방법 2) KRX 에서 가져옴
        # getStockBaseInfo()

        # ETF 리스트 가져오기
        getETFlist()

        # ETN 리스트 가져오기
        getETNlist()

        # 우선주 리스트 가져오기
        # getUseonjuList()

        # 엑셀파일(KRX 정보시스템) 에서 가져오기
        getStockBaseInfo_fromExcel()

        # 미국 주식 가져오기 (뉴욕거래소, 나스닥)
        getOverseasStockBaseInfo()

        # 업비트의 비트코인 전체 목록 불러오기
        tickers = pu.get_tickers(fiat="KRW")
        if tickers :
            saveUpbitBaseInfo(self,tickers)




        self.ready_has_run = True
        print('=== ready end ===')
        
        # print('df Size : ',df.size)
        # print('tickers size : ', len(tickers))

        baseinfoendtime = datetime.datetime.now()
        runningtime = baseinfoendtime - baseinfostarttime
        print('========== running baseinfo getting time  : ', format(runningtime.total_seconds(),".1f"), ' secs')
        
        pass

    print('=== MyAppConfig end ===')


def getStockBaseInfo_fromExcel():
    print("=== getStockBaseInfo_fromExcel started === ")
    # http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201 KRX 정보시스템에서 가져옴.
    

    currentPath = os.getcwd()
    filepath = currentPath+"\\examples\\uploadfiles\\KOSPI_KOSDAQ.csv"
    # 탭으로 분리된(tsv) .txt 텍스트파일 불러오기
    # data = pd.read_csv('파일경로', sep = "\t", , engine='python', encoding = "인코딩방식")
    data = pd.read_csv(filepath, sep = ",")
    print(data)

    # print(data.loc[0])


    if data is not None:

        print("input data len : ",len(data))

        from examples.models import StockBaseInfo
        StockBaseInfo.objects.all().delete()

        insert_queries= []
        for index, row in data.iterrows():
            # print(index, row)

   
            market = row['Market'] 
            marketindex = 1 # Domestic : 1, Overseas : 2, Coin : 3
            code = str(row['Code']).zfill(6)
            name = row['Name']
            business = row['Business']
            detail = row['Detail']
            discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code



            # 신규 insert 쿼리
            insert_queries.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))


        print('insert_queries 한방 업데이트 시작')
        print(datetime.datetime.now())
        if insert_queries is not None : # 마지막 행일 때 한방 업데이트
            result = list(divide_list(insert_queries, 777)) # 777  개씩 나눈다.
            for rs in result :
                print('rs size : ', len(rs))
                StockBaseInfo.objects.bulk_create(rs)

            print(datetime.datetime.now())
            print('insert_queries 한방 업데이트 종료')


        print('=== insert_queries End ===')



def getStockBaseInfo():
 
    
    print('=== StockBaseInfo Start ===')
    df1 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=stockMkt', header=0)[0]
    df2 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=kosdaqMkt', header=0)[0]
    
    print(list(df1))
    print(list(df2))
    df = pd.concat([df1, df2], ignore_index=True)
    
    print(df)

    print('KOSPI : ', len(df1), ', KOSDAQ : ', len(df2), ', TOTAL : ', len(df))
    
    
    # DB 에 저장하기
    # code = models.CharField(max_length=10)
    # name = models.CharField(max_length=20)
    # business = models.CharField(max_length=200)
    # detail = models.CharField(max_length=300)
    # startdate = models.DateField()
    # discuss_url = models.URLField(max_length=250)
    # ['회사명', '종목코드', '업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역']
    
    # if df is not None:
    #     try:
    #         StockBaseInfo.objects.all().delete()
    #     except:
    #         pass


    from examples.models import StockBaseInfo
    StockBaseInfo.objects.all().delete()
    
    insert_queries_kr = []

    # 코스피
    df1 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=stockMkt', header=0)[0]
    
    print(list(df1))
    # df = pd.concat([df1, df2], ignore_index=True)

    print('KOSPI : ', len(df1))


    for index, row in df1.iterrows():
        market = 'KS'
        marketindex = 1 # Domestic : 1, Overseas : 2, Coin : 3
        code = str(row['종목코드']).zfill(6)
        name = row['회사명']
        business = row['업종']
        detail = row['주요제품']
        # startdate = row['상장일']
        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        print(index)
        # print(', code : ',code,', name : ',name,', business : ',business, ', detail : ',detail,
        # ', startdate : ',startdate, ', discuss_url : ',discuss_url, )
        
        # 기존 insert 쿼리
        # StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url).save()

        # 신규 insert 쿼리
        insert_queries_kr.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))




    # 코스닥 가져오기
    df2 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=kosdaqMkt', header=0)[0]
    
    print(list(df2))
    # df = pd.concat([df1, df2], ignore_index=True)


    print( 'KOSDAQ : ', len(df2))


    for index, row in df2.iterrows():
        market = 'KQ'
        marketindex = 1  # Domestic : 1, Overseas : 2, Coin : 3
        code = str(row['종목코드']).zfill(6)
        name = row['회사명']
        business = row['업종']
        detail = row['주요제품']
        # startdate = row['상장일']
        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        print(index)
        # print(', code : ',code,', name : ',name,', business : ',business, ', detail : ',detail,
        # ', startdate : ',startdate, ', discuss_url : ',discuss_url, )
        
        # 기존 insert 쿼리
        # StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url).save()


        # 신규 insert 쿼리
        insert_queries_kr.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))



    print('insert_queries_kr 한방 업데이트 시작')
    print(datetime.datetime.now())
    if insert_queries_kr is not None : # 마지막 행일 때 한방 업데이트

        result = list(divide_list(insert_queries_kr, 777)) # 777  개씩 나눈다.
        for rs in result :
            StockBaseInfo.objects.bulk_create(rs)

        print(datetime.datetime.now())
        print('insert_queries_kr 한방 업데이트 종료')
    




    print('=== StockBaseInfo End ===')

    print(df)


def saveStockBaseInfo(self,df):

    print('=== saveStockBaseInfo Start ===')
    from examples.models import StockBaseInfo
    
    # DB 에 저장하기
    # code = models.CharField(max_length=10)
    # name = models.CharField(max_length=20)
    # business = models.CharField(max_length=200)
    # detail = models.CharField(max_length=300)
    # startdate = models.DateField()
    # discuss_url = models.URLField(max_length=250)
# ['회사명', '종목코드', '업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역']


    
    # if df is not None:
    #     StockBaseInfo.objects.all().delete()

    for index, row in df.iterrows():
        market = row['market']
        code = row['code']
        name = row['name']
        business = row['business']
        detail = row['detail']
        
        # startdate = formattedDate = row['startdate'].strftime("%Y-%m-%d")
        # if row['startdate'] is None:
        #     startdate = '1900-01-01'
        # else:
        #     startdate = row['startdate']

        # print(startdate)
        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        print(index)
        # print(', code : ',code,', name : ',name,', business : ',business, ', detail : ',detail,
        # ', startdate : ',startdate, ', discuss_url : ',discuss_url, )
        
        # StockBaseInfo(code=code,name=name,business=business,detail=detail,startdate=startdate,discuss_url=discuss_url).save()
        StockBaseInfo(market=market, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url).save()
        

    print('=== saveStockBaseInfo End ===')


def getETFlist():

    url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
    raw_data = urllib.request.urlopen(url).read().decode('CP949')
    json_data = json.loads(raw_data)


    from examples.models import StockBaseInfo

    insert_queries_etf = []

    for each in json_data['result']['etfItemList']:
        print(each['itemcode'], each['itemname'])


        market = 'KS'
        marketindex = 1 # Domestic : 1, Overseas : 2, Coin : 3
        code = each['itemcode']
        name = each['itemname']
        business = 'ETF'
        detail = 'ETF'

        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        # 신규 insert 쿼리
        insert_queries_etf.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))


    print('insert_queries_etf 한방 업데이트 시작')
    print(datetime.datetime.now())
    if insert_queries_etf is not None : # 마지막 행일 때 한방 업데이트
        result = list(divide_list(insert_queries_etf, 777)) # 777  개씩 나눈다.
        for rs in result :
            print('rs size : ', len(rs))
            StockBaseInfo.objects.bulk_create(rs)

        print(datetime.datetime.now())
        print('insert_queries_etf 한방 업데이트 종료')


    print('=== insert_queries_etf End ===')


def getETNlist():

    url = 'https://finance.naver.com/api/sise/etnItemList.nhn'
    raw_data = urllib.request.urlopen(url).read().decode('CP949')
    json_data = json.loads(raw_data)


    from examples.models import StockBaseInfo

    insert_queries_etn = []

    for each in json_data['result']['etnItemList']:
        print(each['itemcode'], each['itemname'])


        market = 'KS'
        marketindex = 1 # Domestic : 1, Overseas : 2, Coin : 3
        code = each['itemcode']
        name = each['itemname']
        business = 'ETN'
        detail = 'ETN'

        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        # 신규 insert 쿼리
        insert_queries_etn.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))


    print('insert_queries_etn 한방 업데이트 시작')
    print(datetime.datetime.now())
    if insert_queries_etn is not None : # 마지막 행일 때 한방 업데이트
        result = list(divide_list(insert_queries_etn, 777)) # 777  개씩 나눈다.
        for rs in result :
            print('rs size : ', len(rs))
            StockBaseInfo.objects.bulk_create(rs)

        print(datetime.datetime.now())
        print('insert_queries_etn 한방 업데이트 종료')


    print('=== insert_queries_etn End ===')


def getUseonjuList():

    currentPath = os.getcwd()
    filepath = currentPath+"\\examples\\uploadfiles\\UseonjuList.txt"
    # 탭으로 분리된(tsv) .txt 텍스트파일 불러오기
    # data = pd.read_csv('파일경로', sep = "\t", , engine='python', encoding = "인코딩방식")
    data = pd.read_csv(filepath, sep = "\t")
    print(data)

    if data is not None:

        print("input data len : ",len(data))

            
        from examples.models import StockBaseInfo

        insert_queries_useonju = []

        for index, row in data.iterrows():

            market = row['market']
            marketindex = 1 # Domestic : 1, Overseas : 2, Coin : 3
            code = row['code']
            name = row['name']
            business = row['sector']
            detail = row['sector']
            discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code



            # 신규 insert 쿼리
            insert_queries_useonju.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))


        print('insert_queries_useonju 한방 업데이트 시작')
        print(datetime.datetime.now())
        if insert_queries_useonju is not None : # 마지막 행일 때 한방 업데이트
            result = list(divide_list(insert_queries_useonju, 777)) # 777  개씩 나눈다.
            for rs in result :
                print('rs size : ', len(rs))
                StockBaseInfo.objects.bulk_create(rs)

            print(datetime.datetime.now())
            print('insert_queries_useonju 한방 업데이트 종료')


        print('=== insert_queries_useonju End ===')




def getOverseasStockBaseInfo():
    
    print('=== getOverseasStockBaseInfo Start ===')

    stocks1 = fdr.StockListing('NYSE')   # 뉴욕거래소
    stocks2 = fdr.StockListing('NASDAQ') # 나스닥

    from examples.models import StockBaseInfo


    df = pd.concat([stocks1, stocks2], ignore_index=True)

    print('뉴욕거래소 + 나스닥 : ', len(df))


    insert_queries_overseas = []

    for index, row in df.iterrows():
        market = 'Overseas'
        marketindex = 2 # Domestic : 1, Overseas : 2, Coin : 3
        code = row['Symbol']
        name = row['Name']
        business = row['Industry']
        detail = row['Industry']
        # startdate = row['상장일']
        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        # print(index)
        # print(', code : ',code,', name : ',name,', business : ',business, ', detail : ',detail,
        # ', startdate : ',startdate, ', discuss_url : ',discuss_url, )
        
        # 기존 insert 쿼리
        # StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url).save()


        # 신규 insert 쿼리
        insert_queries_overseas.append(StockBaseInfo(market=market,marketindex= marketindex, code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))


    print('insert_queries_overseas 한방 업데이트 시작')
    print(datetime.datetime.now())
    if insert_queries_overseas is not None : # 마지막 행일 때 한방 업데이트
        result = list(divide_list(insert_queries_overseas, 777)) # 777  개씩 나눈다.
        for rs in result :
            print('rs size : ', len(rs))
            StockBaseInfo.objects.bulk_create(rs)

        print(datetime.datetime.now())
        print('insert_queries_overseas 한방 업데이트 종료')


    print('=== getOverseasStockBaseInfo End ===')




def saveUpbitBaseInfo(self,tickers):

    print('=== saveUpbitBaseInfo Start ===')
    from examples.models import StockBaseInfo
    
    # DB 에 저장하기
    # code = models.CharField(max_length=10)
    # name = models.CharField(max_length=20)
    # business = models.CharField(max_length=200)
    # detail = models.CharField(max_length=300)
    # startdate = models.DateField()
    # discuss_url = models.URLField(max_length=250)
# ['회사명', '종목코드', '업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역']


    
    # if df is not None:
    #     StockBaseInfo.objects.all().delete()

    insert_queries_coin = []

    i = 0
    for ticker in tickers:
        market = 'Coin'
        marketindex = 3
        code = ticker
        name = ticker
        business = ''
        detail = ''
        
        # startdate = formattedDate = row['startdate'].strftime("%Y-%m-%d")
        # if row['startdate'] is None:
        #     startdate = '1900-01-01'
        # else:
        #     startdate = row['startdate']

        # print(startdate)
        discuss_url = ''
        i = i + 1
        print('bitcoin : ',i)
        # print(', code : ',code,', name : ',name,', business : ',business, ', detail : ',detail,
        # ', startdate : ',startdate, ', discuss_url : ',discuss_url, )
        
        # 기존 insert 쿼리
        # StockBaseInfo(code=code,name=name,business=business,detail=detail,startdate=startdate,discuss_url=discuss_url).save()
        # StockBaseInfo(market=market,marketindex=marketindex,  code=code,name=name,business=business,detail=detail,discuss_url=discuss_url).save()
        
        

        # 신규 insert 쿼리
        insert_queries_coin.append(StockBaseInfo(market=market,marketindex=marketindex,  code=code,name=name,business=business,detail=detail,discuss_url=discuss_url))



    print('insert_queries_coin 한방 업데이트 시작')
    print(datetime.datetime.now())
    if insert_queries_coin is not None : # 마지막 행일 때 한방 업데이트
        result = list(divide_list(insert_queries_coin, 777)) # 777  개씩 나눈다.
        for rs in result :
            print('rs size : ', len(rs))
            StockBaseInfo.objects.bulk_create(rs)
        print(datetime.datetime.now())
        print('insert_queries_coin 한방 업데이트 종료')
    




    print('=== saveUpbitBaseInfo End ===')



def getFinanceDataList():

    print('=== getFinanceDataList Start ===')

    df = fdr.StockListing('KRX') # 코스피, 코스닥, 코넥스 전체
    # 컬럼명 바꾸기
    df.rename(columns={'Symbol': 'code', 'Market': 'market', 'Name': 'name', 'Sector': 'business', 'Industry': 'detail', 'ListingDate': 'startdate'}, inplace=True)

    print(df)

    for col in df.columns: 
        print(col)
    
    
    print('=== getFinanceDataList End ===')
    return df


def divide_list(l, n): 
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(l), n): 
        yield l[i:i + n] 


if __name__ == '__main__':
    # getFinanceDataList()
    getStockBaseInfo()
import pandas as pd
from .models import StockBaseInfo

# def get_kor_stock_all_list(request):
#     dfstockcode = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

#     dfstockcode = dfstockcode[['회사명', '종목코드']]
#     dfstockcode = dfstockcode.rename(columns={'회사명':'name', '종목코드':'code'})

#     print(dfstockcode)

# get_kor_stock_all_list()

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
    for index, row in df.iterrows():
        code = str(row['종목코드']).zfill(6)
        name = row['회사명']
        business = row['업종']
        detail = row['주요제품']
        startdate = row['상장일']
        discuss_url = 'https://finance.naver.com/item/board.nhn?code=' + code

        print(index)
        # print(', code : ',code,', name : ',name,', business : ',business, ', detail : ',detail,
        # ', startdate : ',startdate, ', discuss_url : ',discuss_url, )
    
        StockBaseInfo(code=code,name=name,business=business,detail=detail,
         startdate=startdate,discuss_url=discuss_url)
    print('=== StockBaseInfo End ===')

    print(df)


if __name__ == '__main__':
    result_df = getStockBaseInfo()
 
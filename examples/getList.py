import pandas as pd
from django.apps import AppConfig
import FinanceDataReader as fdr
import pyupbit as pu



   
 
def getList():
    from django.db import connection
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

 
    print(StockBaseInfo.objects.all())


    print('=== saveUpbitBaseInfo End ===')



if __name__ == '__main__':
    getList()

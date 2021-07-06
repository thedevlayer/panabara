from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
# from django.contrib.auth.models import User # new

# 구분 - 국내주식, 해외주식, 코인
# 종목코드
# 종목명
# 매수가
# 현재가
# 수량
# 수익률


class MyStocks(models.Model):
    DOMESTICSTK = 1
    OVERSEASSTK = 2
    COIN = 3
    INVST_TYPES = (
        (DOMESTICSTK, 'Domestic'),
        (OVERSEASSTK, 'Overseas'),
        (COIN, 'Coin'),
    )


    # 입력값
    invst_type = models.PositiveSmallIntegerField(choices=INVST_TYPES)
    icode = models.CharField(max_length=10, blank=True)
    iname = models.CharField(max_length=20, blank=True, null=True)
    # 매수가(입력한 값)
    iunitbuyprice = models.DecimalField(max_digits=18, decimal_places=8, null=True)
    # 현재가(조회한값)
    iunitcurprice = models.DecimalField(max_digits=18, decimal_places=8, null=True, default=0.0)
    # 수량
    iquantity = models.DecimalField(max_digits=18, decimal_places=8, null=True)


    # 적용환율(default 1)
    kcurrencyrate = models.DecimalField(max_digits=8, decimal_places=1, null=True, default=1)
    # 환율적용 매수가
    kbuyprice = models.DecimalField(max_digits=18, decimal_places=8, null=True)
    # 환율적용 현재가
    kcurprice = models.DecimalField(max_digits=18, decimal_places=8, null=True, default=0.0)
    # 환율적용 수익률
    kprofitratio = models.DecimalField(max_digits=10, decimal_places=1,null=True, default=0.0)
    # 환율적용 매수금액
    ktotalbuyprice = models.DecimalField(max_digits=12, decimal_places=0, null=True, default=0.0)
    # 환율적용 평가금액
    ktotalcurprice = models.DecimalField(max_digits=12, decimal_places=0, null=True, default=0.0)


    # 이전 환율적용 매수금액
    ktotalprevbuyprice = models.DecimalField(max_digits=12, decimal_places=0, null=True, default=0.0)
    # 이전 환율적용 평가금액 
    ktotalprevprice = models.DecimalField(max_digits=12, decimal_places=0, null=True, default=0.0)
    # 이전 환율적용 수익률
    kprofitpreratio = models.DecimalField(max_digits=10, decimal_places=1,null=True, default=0.0)



    # 평생종목 여부
    # kforeverholdyn = models.CharField(max_length=20, blank=True, null=True)
    kforeverholdyn = models.BooleanField(default=False)
    # 업데이트 날짜
    iupdatedate = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

    # Additional information
    business = models.CharField(max_length=200, null=True)
    detail = models.CharField(max_length=300, null=True)
    # startdate = models.DateField(null=True)
    discuss_url = models.URLField(max_length=250, null=True)
    # # author = models.ForeignKey(Use, on_delete=models.CASCADE)
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,db_column="user"
    # )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)



        
    def __str__(self):
        return '[{}] [{}]  '.format(self.invst_type, self.icode)

# class MyStocks(models.Model):
#     HARDCOVER = 1
#     PAPERBACK = 2
#     EBOOK = 3
#     BOOK_TYPES = (
#         (HARDCOVER, 'Hardcover'),
#         (PAPERBACK, 'Paperback'),
#         (EBOOK, 'E-MyStocks'),
#     )
#     title = models.CharField(max_length=50)
#     publication_date = models.DateField(null=True)
#     author = models.CharField(max_length=30, blank=True)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     pages = models.IntegerField(blank=True, null=True)
#     mystock_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

#     timestamp = models.DateField(auto_now_add=True, auto_now=False)



class StockBaseInfo(models.Model):
    market = models.CharField(max_length=10, default='')
    marketindex = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    business = models.CharField(max_length=200)
    detail = models.CharField(max_length=300,default='')
    # startdate = models.DateField()
    discuss_url = models.URLField(max_length=250)

    def __str__(self):
        return '[{}] {}'.format(self.market, self.code)



class Balances(models.Model):
    bdate = models.DateField( auto_now=False, null=True)
    bamount = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    bauthor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    bincreased = models.DecimalField(max_digits=12, decimal_places=0, null=True) 
    bincreasedratio = models.DecimalField(max_digits=10, decimal_places=1,null=True, default=0.0)

    def __str__(self):
        return '[{}] {}'.format(self.bdate, self.bamount, self.bauthor, self.bincreased)


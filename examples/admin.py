from django.contrib import admin

# Register your models here.
from .models import MyStocks, StockBaseInfo,Balances

# 아래의 코드를 입력하면 admin 페이지에서 관리할 수 있습니다.
admin.site.register(MyStocks)
admin.site.register(StockBaseInfo)
admin.site.register(Balances)
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .forms import (
    MyStockModelForm,
    BalancesModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    MyStockFilterForm
)
from .models import MyStocks, Balances
from .models import StockBaseInfo

from django.db.models import Count
from django.shortcuts import redirect

import yfinance as yf
import datetime
import pyupbit
import FinanceDataReader as fdr
import pandas as pd 
import numpy as np

from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse



def population_chart(request):

    labels = []
    data = []

    if not request.user.is_anonymous:


        # queryset = MyStocks.objects.filter(author=request.user).order_by('-ktotalcurprice')
        # for entry in queryset:
        #     labels.append(entry.iname)
        #     data.append(entry.ktotalcurprice)
        
        # return JsonResponse(data={
        #     'labels': labels,
        #     'data': data,
        # })


        queryset = MyStocks.objects.filter(author=request.user).values('invst_type').annotate(Sum('ktotalcurprice')).order_by('-ktotalcurprice__sum')

        print(queryset)


        for entry in queryset:
            print(entry)
            # print('entry[invst_type]',entry['invst_type'].get_invst_type_display)
            # print(entry.invst_type)
            # print(entry.ktotalcurprice)
            itype = None
            if entry['invst_type'] == 1:
                itype = 'Domestic'
            elif entry['invst_type'] == 2:
                itype = 'Overseas'
            elif entry['invst_type'] == 3:
                itype = 'Coin'
            else:
                itype = 'N/A'

            labels.append(itype)
            data.append(entry['ktotalcurprice__sum'] )
            
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })
    
    else:
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })


def accumulate_chart(request):

    labels = []
    data = []


    if not request.user.is_anonymous:



        # queryset = MyStocks.objects.filter(author=request.user).order_by('-ktotalcurprice')
        # for entry in queryset:
        #     labels.append(entry.iname)
        #     data.append(entry.ktotalcurprice)
        
        # return JsonResponse(data={
        #     'labels': labels,
        #     'data': data,
        # })

        queryset = Balances.objects.filter(bauthor=request.user).order_by('bdate')

        print(queryset)


        for entry in queryset:
            print(entry)

            labels.append(entry.bdate)
            data.append(entry.bamount )
            # data.append(entry.bincreased)
            
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

    else:
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })



def bubble_chart(request):

    print('bubble_chart started ============')

    name = []
    x = []
    y = []
    r = []

        
    if not request.user.is_anonymous:
        

        querysetbubble = MyStocks.objects.filter(author=request.user)



        print('bubble_chart querysetbubble' ,querysetbubble)


        for entry in querysetbubble:

            if entry.iname =='KRW-BTC':
                print('entry : ',entry)
                print('entry.iname : ',entry.iname)
                print('entry.ktotalcurprice : ',entry.ktotalcurprice)
                print('kprofitratio : ',entry.kprofitratio)

            name.append(entry.iname)
            x.append(int(entry.ktotalcurprice))
            y.append(int(entry.kprofitratio))
            # r.append(int(entry.kprofitratio))
            r.append(entry.invst_type) # 투자 유형 용도로 사용


        print('x :',x)
        print('y :',y)
        print('r :',r)
            
        return JsonResponse(data={
            'name':name,
            'x': x,
            'y': y,
            'r': r,
        })

    else:
        return JsonResponse(data={
            'name':name,
            'x': x,
            'y': y,
            'r': r,
        })


def pie_chart(request):
    labels = []
    data = []

    if not request.user.is_anonymous:
        queryset = MyStocks.objects.filter(author=request.user).order_by('-ktotalcurprice')
        for entry in queryset:
            labels.append(entry.iname)
            data.append(entry.ktotalcurprice)

        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })
    else:
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })


def mixed_chart(request):
    labels = []
    dataamount = []
    dataprofit = []
    dataprofitmin = []
    dataprofitmax = []
    dataprofitcolor = []
    dataprofit0 = []

    if not request.user.is_anonymous:
        queryset = MyStocks.objects.filter(author=request.user).order_by('-kprofitratio')
        for entry in queryset:
            labels.append(entry.iname)
            dataamount.append(entry.ktotalcurprice)
            dataprofit.append(entry.kprofitratio)
            dataprofit0.append(0)

            if entry.invst_type == 1:
                dataprofitcolor.append("#3333FF") 
            elif entry.invst_type == 2:
                dataprofitcolor.append("#DC3545") 
            elif entry.invst_type == 3:
                dataprofitcolor.append("#5CB85C") 
     

        # if queryset.reverse()[0].kprofitratio is not None and queryset[0].kprofitratio is not None:
        dataprofitmin = queryset.reverse()[0].kprofitratio
        dataprofitmax = queryset[0].kprofitratio

        print('dataprofitmin :', dataprofitmin)
        print('dataprofitmax :',dataprofitmax)

        
        return JsonResponse(data={
            'labels': labels,
            'dataamount': dataamount,
            'dataprofit':dataprofit,
            'dataprofitmin':dataprofitmin,
            'dataprofitmax':dataprofitmax,
            'dataprofitcolor':dataprofitcolor,
            'dataprofit0':dataprofit0,

        })
    else:
        return JsonResponse(data={
            'labels': labels,
            'dataamount': dataamount,
            'dataprofit':dataprofit,
            'dataprofitmin':dataprofitmin,
            'dataprofitmax':dataprofitmax,
            'dataprofitcolor':dataprofitcolor,
            'dataprofit0':dataprofit0,
        })
    

def kospi_chart(request):
    labels = []
    data = []

    now = datetime.datetime.now()
    now_before_5 = now - datetime.timedelta(days=365)


    #코스피
    ks11 = fdr.DataReader('KS11', now_before_5)
    print(ks11)
    # print(ks11['Close'].tolist())


    df=pd.DataFrame(ks11)
    ts_list = df.index.tolist()  # a list of Timestamp's
    date_list = [ ts.date() for ts in ts_list ]  # a list of datetime.date's
    date_str_list = [ str(date) for date in date_list ]  # a list of strings

    close = df['Close'].apply(np.int64).tolist()


    print(date_str_list)
    print(close)

    # date_str_list = ['1','2','3']
    # close = ['111','222','333']
    # labels.append(date_str_list)
    # data.append(close)


    for date in date_str_list:
        labels.append(date)

    for c in close:
        data.append(c)




    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    







# class Index(generic.ListView):
#     model = MyStocks
#     context_object_name = 'mystocks'
#     template_name = 'index.html'

#     def get_queryset(self):
#         qs = super().get_queryset()

#         # 사용자 인증했을 때만 해당 사용자 데이터만 필터링
#         if self.request.user.is_authenticated:
#             qs = qs.filter(author=self.request.user)

#         if 'type' in self.request.GET:
#             qs = qs.filter(invst_type=int(self.request.GET['type'])).order_by('kprofitratio')

#         print(qs)
#         print('222222222222222222222222222222222222222222')

        # return qs

class Index(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'mystocks'
    model = MyStocks

    def get_queryset(self):

        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            
            qs = MyStocks.objects.filter(author=self.request.user)

        if 'type' in self.request.GET:
            qs = qs.filter(invst_type=int(self.request.GET['type'])).order_by('kprofitratio')

        return qs

    def get_context_data(self, **kwargs):
        
        context = {}
        

        if self.request.user.is_authenticated:
            context = super(Index, self).get_context_data(**kwargs)
            context['balances'] =  Balances.objects.filter(bauthor=self.request.user).order_by('bdate')
            context['bincreased'] =  Balances.objects.filter(bauthor=self.request.user).order_by('bdate')


            finaltotalamounts = 0
            finaltotalamounts_domestic = 0
            finaltotalamounts_overseas = 0
            finaltotalamounts_coin = 0
            
            prevfinaltotalamounts = 0
            prevfinaltotalamounts_domestic = 0
            prevfinaltotalamounts_overseas = 0
            prevfinaltotalamounts_coin = 0

            # 평가금액 추출
            totalamounts =  MyStocks.objects.filter(author=self.request.user).aggregate(Sum('ktotalcurprice'))
            totalamounts_domestic =   MyStocks.objects.filter(author=self.request.user, invst_type=1).aggregate(Sum('ktotalcurprice'))
            totalamounts_overseas =   MyStocks.objects.filter(author=self.request.user, invst_type=2).aggregate(Sum('ktotalcurprice'))
            totalamounts_coin =  MyStocks.objects.filter(author=self.request.user, invst_type=3).aggregate(Sum('ktotalcurprice'))

            prevtotalamounts =  MyStocks.objects.filter(author=self.request.user).aggregate(Sum('ktotalprevprice'))
            prevtotalamounts_domestic =   MyStocks.objects.filter(author=self.request.user, invst_type=1).aggregate(Sum('ktotalprevprice'))
            prevtotalamounts_overseas =   MyStocks.objects.filter(author=self.request.user, invst_type=2).aggregate(Sum('ktotalprevprice'))
            prevtotalamounts_coin =  MyStocks.objects.filter(author=self.request.user, invst_type=3).aggregate(Sum('ktotalprevprice'))

            print('prevtotalamounts : ',prevtotalamounts)


            diff_finaltotalamounts = 0
            diff_finaltotalamounts_domestic = 0
            diff_finaltotalamounts_overseas = 0
            diff_finaltotalamounts_coin = 0

            if totalamounts['ktotalcurprice__sum']  is not None:
                finaltotalamounts = totalamounts['ktotalcurprice__sum']

                if prevtotalamounts['ktotalprevprice__sum'] is not None:
                    prevfinaltotalamounts =  prevtotalamounts['ktotalprevprice__sum']

                    
                print('finaltotalamounts',finaltotalamounts)
                print('prevfinaltotalamounts',prevfinaltotalamounts)

                
                diff_finaltotalamounts = finaltotalamounts - prevfinaltotalamounts

            if totalamounts_domestic['ktotalcurprice__sum']  is not None:
                finaltotalamounts_domestic = totalamounts_domestic['ktotalcurprice__sum']
                if prevtotalamounts_domestic['ktotalprevprice__sum']   is not None:
                    prevfinaltotalamounts_domestic = prevtotalamounts_domestic['ktotalprevprice__sum']   
                diff_finaltotalamounts_domestic= finaltotalamounts_domestic - prevfinaltotalamounts_domestic   

            if totalamounts_overseas['ktotalcurprice__sum']  is not None:
                finaltotalamounts_overseas = totalamounts_overseas['ktotalcurprice__sum']
                if prevtotalamounts_overseas['ktotalprevprice__sum'] is not None:
                    prevfinaltotalamounts_overseas =  prevtotalamounts_overseas['ktotalprevprice__sum']
                diff_finaltotalamounts_overseas = finaltotalamounts_overseas - prevfinaltotalamounts_overseas

            if totalamounts_coin['ktotalcurprice__sum']  is not None:
                finaltotalamounts_coin = totalamounts_coin['ktotalcurprice__sum']
                if prevtotalamounts_coin['ktotalprevprice__sum'] is not None:
                    prevfinaltotalamounts_coin = prevtotalamounts_coin['ktotalprevprice__sum']
                diff_finaltotalamounts_coin = finaltotalamounts_coin - prevfinaltotalamounts_coin

            context['finaltotalamounts'] = finaltotalamounts
            context['finaltotalamounts_domestic'] = finaltotalamounts_domestic
            context['finaltotalamounts_overseas'] = finaltotalamounts_overseas
            context['finaltotalamounts_coin'] =  finaltotalamounts_coin

   
            context['diff_finaltotalamounts'] = diff_finaltotalamounts
            context['diff_finaltotalamounts_domestic'] = diff_finaltotalamounts_domestic
            context['diff_finaltotalamounts_overseas'] = diff_finaltotalamounts_overseas
            context['diff_finaltotalamounts_coin'] =  diff_finaltotalamounts_coin





            # 분야별 카운트
            qrsnumber = MyStocks.objects.filter(author=self.request.user).values('invst_type').order_by('invst_type').annotate(count=Count('invst_type'))

            print('qrsnumber : ',qrsnumber)
            totcount = 0
            for qsnumber in qrsnumber:
                totcount = totcount + qsnumber['count']
                if qsnumber['invst_type'] == 1:
                    context['totalnumbers_domestic'] = qsnumber['count']
                if qsnumber['invst_type'] == 2:
                    context['totalnumbers_overseas'] = qsnumber['count']
                if qsnumber['invst_type'] == 3:
                    context['totalnumbers_coin'] = qsnumber['count']
            if totcount > 0:
                context['totalnumbers'] = totcount


        
             
            # 평생주식 카운트

            forevercount_total = 0
            forevercount_domestic = 0
            forevercount_overseas = 0
            forevercount_coin = 0
            
            # forevercount_total = MyStocks.objects.filter(author=self.request.user).count()
            forevercount_domestic =   MyStocks.objects.filter(author=self.request.user, invst_type=1,kforeverholdyn=True).count()
            forevercount_overseas =   MyStocks.objects.filter(author=self.request.user, invst_type=2,kforeverholdyn=True).count()
            forevercount_coin =  MyStocks.objects.filter(author=self.request.user, invst_type=3,kforeverholdyn=True).count()



            context['forevercount_total'] = forevercount_domestic + forevercount_overseas + forevercount_coin
            context['forevercount_domestic'] =forevercount_domestic
            context['forevercount_overseas'] =forevercount_overseas
            context['forevercount_coin'] =forevercount_coin

            print('forevercount_total :',forevercount_total)
            print('forevercount_domestic :',forevercount_domestic)
            print('forevercount_overseas :',forevercount_overseas)
            print('forevercount_coin :',forevercount_coin)


            # 분야별 합계
            qrssum = MyStocks.objects.filter(author=self.request.user)


            buyprice = 0
            # 매수 금액
            buyprice_domestic = 0
            buyprice_overseas = 0
            buyprice_coin = 0


            for qssum in qrssum:
                # bprice = qssum['iunitbuyprice'] * qssum['iquantity']
                # buyprice = buyprice + bprice

                # if qssum['invst_type'] == 1:
                #     buyprice_domestic = buyprice_domestic + buyprice
                # if qssum['invst_type'] == 2:
                #     buyprice_overseas = buyprice_overseas + buyprice
                # if qssum['invst_type'] == 3:
                #     buyprice_coin = buyprice_coin + buyprice

                # bprice = qssum.iunitbuyprice * qssum.iquantity * qssum.kcurrencyrate # 국내환율은 1, 외화는 환율값으로 
                bprice = qssum.ktotalbuyprice # 종목별 매수금액
                if bprice is not None:
                    buyprice = buyprice + bprice # 누적 매수금액

                    if qssum.invst_type== 1:   
                        buyprice_domestic = buyprice_domestic + bprice
                    if qssum.invst_type == 2:   
                        buyprice_overseas = buyprice_overseas + bprice
                    if qssum.invst_type == 3:   
                        buyprice_coin = buyprice_coin + bprice




    # context['finaltotalamounts'] = finaltotalamounts
    # context['finaltotalamounts_domestic'] = finaltotalamounts_domestic
    # context['finaltotalamounts_overseas'] = finaltotalamounts_overseas
    # context['finaltotalamounts_coin'] =  finaltotalamounts_coin

            # 손익
            print('buyprice_domestic :',buyprice_domestic)
            print('finaltotalamounts_domestic :',finaltotalamounts_domestic)
    
            print('buyprice_overseas :',buyprice_overseas)
            print('finaltotalamounts_overseas :',finaltotalamounts_overseas)

            totprice = 0
            totprice_domestic = 0
            totprice_overseas = 0
            totprice_coin = 0

            prevtotprice = 0
            prevtotprice_domestic = 0
            prevtotprice_overseas = 0
            prevtotprice_coin = 0
        
#prevfinaltotalamounts_coin

            # 손익 금액 구하기
            if buyprice is not None and  finaltotalamounts is not None:
                totprice = int(finaltotalamounts- buyprice)
                prevtotprice = int(prevfinaltotalamounts - buyprice)
            if buyprice_domestic is not None and finaltotalamounts_domestic  is not None:
                totprice_domestic = int(finaltotalamounts_domestic- buyprice_domestic)
                prevtotprice_domestic = int(prevfinaltotalamounts_domestic - buyprice)
            if buyprice_overseas is not None and  finaltotalamounts_overseas is not None:
                totprice_overseas = int(finaltotalamounts_overseas - buyprice_overseas)
                prevtotprice_overseas = int(prevfinaltotalamounts_overseas - buyprice)
            if buyprice_coin is not None and  finaltotalamounts_coin is not None:
                totprice_coin = int(finaltotalamounts_coin - buyprice_coin)
                prevtotprice_coin = int(prevfinaltotalamounts_coin - buyprice)

            print('totprice_domestic : ',totprice_domestic)
            print('totprice_overseas : ',totprice_overseas)

            context['totprice'] = totprice
            context['totprice_domestic'] = totprice_domestic
            context['totprice_overseas'] = totprice_overseas
            context['totprice_coin'] = totprice_coin

            # 수익률

            totratio = 0
            totratio_domestic =0
            totratio_overseas =0
            totratio_coin = 0

            prevtotratio = 0
            prevtotratio_domestic =0
            prevtotratio_overseas =0
            prevtotratio_coin = 0

            print('totprice_overseas : ', totprice_overseas)
            print('buyprice_overseas: ', buyprice_overseas)


                # prevfinaltotalamounts_domestic = prevtotalamounts_domestic['ktotalprevprice__sum']   
                # diff_finaltotalamounts_domestic= finaltotalamounts_domestic - prevfinaltotalamounts_domestic   


            print('diff_finaltotalamounts',diff_finaltotalamounts)
            print('prevfinaltotalamounts',prevfinaltotalamounts)

            

            print('diff_finaltotalamounts_overseas',diff_finaltotalamounts_overseas)
            print('prevfinaltotalamounts_overseas',prevfinaltotalamounts_overseas)

            if buyprice is not None and buyprice != 0:
                totratio = round((totprice/ buyprice) * 100,1)
                if prevfinaltotalamounts > 0:
                    prevtotratio = round((diff_finaltotalamounts/ prevfinaltotalamounts) * 100, 2)
                #   prevtotratio = format((diff_finaltotalamounts/ prevfinaltotalamounts) * 100,".1f")

            if buyprice_domestic is not None and buyprice_domestic != 0:
                totratio_domestic =round((totprice_domestic/ buyprice_domestic) * 100,1)
                if prevfinaltotalamounts_domestic > 0:
                    # prevtotratio_domestic = format((diff_finaltotalamounts_domestic/ prevfinaltotalamounts_domestic) * 100,".1f")
                    prevtotratio_domestic = round((diff_finaltotalamounts_domestic/ prevfinaltotalamounts_domestic) * 100, 2)
    

            if buyprice_overseas is not None and buyprice_overseas != 0:
                totratio_overseas = round((totprice_overseas/ buyprice_overseas) * 100,1)
                if prevfinaltotalamounts_overseas > 0:
                    # prevtotratio_overseas = format((diff_finaltotalamounts_overseas/ prevfinaltotalamounts_overseas) * 100,".4f")
                    prevtotratio_overseas = round((diff_finaltotalamounts_overseas/ prevfinaltotalamounts_overseas) * 100, 2)   

            if buyprice_coin is not None and buyprice_coin != 0:                
                totratio_coin = round((totprice_coin/ buyprice_coin) * 100,1)
                if prevfinaltotalamounts_coin > 0:
                    # prevtotratio_coin = format((diff_finaltotalamounts_coin/ prevfinaltotalamounts_coin) * 100,".1f")
                    prevtotratio_coin = round((diff_finaltotalamounts_coin/ prevfinaltotalamounts_coin) * 100, 2)   

 
            context['totratio'] = totratio
            context['totratio_domestic'] = totratio_domestic
            context['totratio_overseas'] = totratio_overseas
            context['totratio_coin'] = totratio_coin
# totprice_domestic :  1609311
#   buyprice_domestic : 1099989
# prevtotprice_domestic:  -25497555

            context['prevtotratio'] = prevtotratio
            context['prevtotratio_domestic'] = prevtotratio_domestic
            context['prevtotratio_overseas'] = prevtotratio_overseas
            context['prevtotratio_coin'] = prevtotratio_coin


            print('prevtotratio:',prevtotratio)
            print('prevtotratio_domestic:',prevtotratio_domestic)
            print('prevtotratio_overseas:',prevtotratio_overseas)
            print('prevtotratio_coin:',prevtotratio_coin)



            # DB 업데이트 시간 불러오기
            getupdatetime =  MyStocks.objects.filter(author=self.request.user).first()

            print('getupdatetime', getupdatetime)
            # print('getupdatetime.iupdatedate',getupdatetime.iupdatedate)

            try:
                if getupdatetime is not None:
                    print('getupdatetime.iupdatedate: ',getupdatetime.iupdatedate)
                    context['updatetime'] = (getupdatetime.iupdatedate).strftime("%Y/%m/%d %H:%M:%S")
                else:
                    context['updatetime'] = ''
            except:
                context['updatetime'] = ''
            
        return context





class MyStockFilterView(BSModalFormView):
    template_name = 'examples/filter_mystock.html'
    form_class = MyStockFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?type=' + form.cleaned_data['type']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter




class MyStockCreateView(BSModalCreateView):
    template_name = 'examples/create_mystock.html'
    form_class = MyStockModelForm
    success_message = 'Success: MyStocks was created.'
    success_url = reverse_lazy('index')

class BalancesCreateView(BSModalCreateView):
    template_name = 'examples/create_balances.html'
    form_class = BalancesModelForm
    success_message = 'Success: Balances was created.'
    success_url = reverse_lazy('index')

class MyStockUpdateView(BSModalUpdateView):
    model = MyStocks
    template_name = 'examples/update_mystock.html'
    form_class = MyStockModelForm
    success_message = 'Success: MyStocks was updated.'
    success_url = reverse_lazy('index')

class BalancesUpdateView(BSModalUpdateView):
    model = Balances
    template_name = 'examples/update_balances.html'
    form_class = BalancesModelForm
    success_message = 'Success: Balances was updated.'
    success_url = reverse_lazy('index')


class MyStockReadView(BSModalReadView):
    model = MyStocks
    template_name = 'examples/read_mystock.html'


class MyStockDeleteView(BSModalDeleteView):
    model = MyStocks
    template_name = 'examples/delete_mystock.html'
    success_message = 'Success: MyStocks was deleted.'
    success_url = reverse_lazy('index')

class BalancesDeleteView(BSModalDeleteView):
    model = Balances
    template_name = 'examples/delete_balances.html'
    success_message = 'Success: Balances was deleted.'
    success_url = reverse_lazy('index')

class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')

def refresh(request):
    print('refresh started....')

    refresstarttime = datetime.datetime.now()

    if request.user.is_anonymous:
        messages.warning(request, "Please log in or sign up! "  )
        # index 로 돌아가기
        return redirect('index')    
    
    print('-------------------환율 정보-------------------------------------------------------------------------------')

    from bs4 import BeautifulSoup
    import urllib.request as req

    # HTML 가져오기
    url = "http://finance.naver.com/marketindex/"
    res = req.urlopen(url)

    # HTML 분석하기
    soup = BeautifulSoup(res, "html.parser")

    #원하는 데이터 추출하기
    currencyusd = soup.select_one("div.head_info > span.value").string
    
    currencyusd = currencyusd.replace(" ","")
    currencyusd = currencyusd.replace(",","")
    # print(currencyusd)
    print("usd/krw = ",currencyusd)




    # print('request.user :', request.user)

    #  request.user 대한 종목들 가져오기


    try:
        qs = MyStocks.objects.all()

        # 사용자 인증했을 때만 해당 사용자 데이터만 필터링
        if request.user.is_authenticated:
            qs = qs.filter(author=request.user) #.order_by('-kprofitratio')
            print('get qs results')

            cnt = qs.count()
            print('current db count : ', cnt)
            print('request.user : ', request.user)
         

            if request.user.is_superuser:
                print('SUPER USER :',request.user )
            elif not request.user.is_superuser and cnt > 10:
                messages.warning(request, "Stock Items exceeds more than 5, please contact to admin if required." )
                return redirect('index')    


    except :
        qs = None
        print('MyStocks.DoesNotExist')

    yfsearch = []
    upbitsearch = []

    # print(qs)


    # 사용자가 보유한 종목코드 기준으로 기본정보 업데이트
    update_queries_baseinfo = []
    for c in qs:
        # print('code : ', c.icode)
        sqs = StockBaseInfo.objects.filter(code=c.icode)
        if sqs :
            sqs = sqs[0]

            # print(sqs)
            # print(sqs.market)

            # 기존 업데이트문
            # MyStocks.objects.filter(author=request.user, icode=c.icode, pk=c.pk).update(invst_type=sqs.marketindex)
            # MyStocks.objects.filter(author=request.user, icode=c.icode, pk=c.pk).update(iname=sqs.name)
            # # MyStocks.objects.filter(author=request.user, icode=c.icode, pk=c.pk).update(iunitcurprice=sqs.market)
            # MyStocks.objects.filter(author=request.user, icode=c.icode, pk=c.pk).update(business=sqs.business)
            # MyStocks.objects.filter(author=request.user, icode=c.icode, pk=c.pk).update(detail=sqs.detail)
            # MyStocks.objects.filter(author=request.user, icode=c.icode, pk=c.pk).update(discuss_url=sqs.discuss_url)
           
  


            #신규 업데이트 문
            update_query = MyStocks.objects.get(author=request.user, icode=c.icode, pk=c.pk)

            update_query.invst_type=sqs.marketindex
            update_query.iname=sqs.name
            update_query.business=sqs.business
            update_query.detail=sqs.detail
            update_query.discuss_url=sqs.discuss_url

            update_queries_baseinfo.append(update_query) 





            if(sqs.marketindex == 1 ): # 국내 전용: .KS or .KQ
                yfsearch.append(c.icode +'.' + sqs.market )
            elif(sqs.marketindex == 2): # 해외: 나스닥, 
                yfsearch.append(c.icode)
            elif(sqs.marketindex == 3):  # Coin
                upbitsearch.append(c.icode)




        else:
            print('====== NOT Exist info  in StockBaseInfo ======= : ', c.icode)
            messages.warning(request, "====== NOT Exist info  in StockBaseInfo ======= : " + c.icode )


    print('기본정보 한방 업데이트 시작')
    print(datetime.datetime.now())
    if update_queries_baseinfo is not None : # 마지막 행일 때 한방 업데이트
        MyStocks.objects.bulk_update(update_queries_baseinfo, ['invst_type','iname','business','detail','discuss_url'])
        print(datetime.datetime.now())
        print('기본정보 한방 업데이트 종료')
        

    # 야후에서 주식 현재가 가져오기

    now = datetime.datetime.now()
    now_before_5 = now - datetime.timedelta(days=5)
    # print(now_before_5)  # 2021-04-14 21:15:54.891525


    yfsearch = list(set(yfsearch)) # 중복항목 제거
    # print('yfsearch : ',yfsearch)


    if yfsearch :
        getyahooinfostart =  datetime.datetime.now()


        result = list(divide_list(yfsearch, 50)) # 50  개씩 나눈다.
        for rs in result :
            # print('rs size : ', len(rs))
            df = yf.download(rs,start = now_before_5)






            getyahooinfoend =  datetime.datetime.now()
            # print('getyahooinfostart - getyahooinfoend = ', format((getyahooinfoend-getyahooinfostart).total_seconds(),".1f"), ' secs' )

            # print(df)
            # print('-------------------호출-------------------------------------------------------------------------------')

            
            starttime =  datetime.datetime.now()
            # print('starttime', datetime.datetime.now())

            df = df['Close']
            # print(df)
            # print('--------------------바로 위의 데이터값으로 채우기------------------------------------------------------------------------------')


            df = df.fillna(method="ffill") #바로 위의 데이터값으로 채우기(보간)
            # print(df)



            if(len(yfsearch) > 1):
                # print('-------------------- 코드 변경하기 .KS, .KQ  없애기 ----------------------------------------------------------------------------')
                df.columns = df.columns.str.replace('.KS','')
                df.columns = df.columns.str.replace('.KQ','')
                # print(df)

                # 마지막 값만 가져오기
                # print('------------------마지막 값만 가져오기--------------------------------------------------------------------------------')
                df = df.iloc[-1]
                # print(df)
            


                # print(type(df))

                # print(df)



                update_queries = []
                # 현재가, 평가금액,수익률 저장하기 (국내 주식, 해외주식)
                for pinfo in df.index:
                    # print(type(pinfo))
                    # print(pinfo)
                    # print(type(df[pinfo]))
                    # print(df[pinfo])
                    # print('======\n')

                    curcode = pinfo
                    curprice = df[pinfo]
                    # if isNaN(curprice) :
                    #     continue


                    codeinfo = MyStocks.objects.filter(author=request.user, icode=curcode)
                    i = 0
                    for ci in codeinfo: # 종목이 여러개 일 수 있으므로 for 문 구성
                        cinfo = MyStocks.objects.filter(author=request.user, icode=curcode)[i]


                        # print(cinfo)
                        # print('cinfo.iquantity :', cinfo.iquantity)
                        # print('cinfo.iunitbuyprice :', cinfo.iunitbuyprice)
                        totprice = float(cinfo.iquantity) * curprice
                        totbuyprice = float(cinfo.iquantity) * float(cinfo.iunitbuyprice)

                        # 해외주식의 경우 USD 환율 계산
                        fcurrencyusd = float(currencyusd)
                        # print(fcurrencyusd)

                        if cinfo.invst_type == 2 : # 해외주식의 경우 평가금액에 환율을 곱한다.
                            totprice = totprice * fcurrencyusd
                            totbuyprice = totbuyprice * fcurrencyusd
                        
                        gap = float(curprice) - float(cinfo.iunitbuyprice)
                        # print(gap)
                        gapper = gap / float(cinfo.iunitbuyprice)
                        # print(gapper)
                        profitratio = gapper * 100
                        # print(profitratio)


                        if isNaN(curprice) :
                            curprice = 0
                            totprice = 0
                            profitratio = -100








                        
                        # profitratio = (float(curprice) - float(cinfo.iunitbuyprice))/float(cinfo.iunitbuyprice) * 100

                        # 기존 업데이트 문
                        # if cinfo.invst_type == 2 :
                        #     MyStocks.objects.filter(author=request.user, icode=curcode, pk=cinfo.pk).update(kcurrencyrate=float(currencyusd))     
                        # MyStocks.objects.filter(author=request.user, icode=curcode, pk=cinfo.pk).update(iunitcurprice=curprice)
                        # MyStocks.objects.filter(author=request.user, icode=curcode, pk=cinfo.pk).update(ktotalcurprice=totprice)
                        # MyStocks.objects.filter(author=request.user, icode=curcode, pk=cinfo.pk).update(kprofitratio=profitratio)
                        # MyStocks.objects.filter(author=request.user, icode=curcode, pk=cinfo.pk).update(iupdatedate=now)

                        #신규 업데이트 문
                        update_query = MyStocks.objects.get(author=request.user, icode=curcode, pk=cinfo.pk)


                        if cinfo.invst_type == 2 :
                            update_query.kcurrencyrate=float(currencyusd) 
                            print('currencyusd :',currencyusd)
                            print(' cinfo.iunitbuyprice: ', cinfo.iunitbuyprice)
                            update_query.kbuyprice= float(currencyusd) * float(cinfo.iunitbuyprice)
                            update_query.kcurprice= float(currencyusd) * float(cinfo.iunitcurprice)
                        else :
                            update_query.kcurrencyrate= 1 
                            update_query.kbuyprice= cinfo.iunitbuyprice
                            update_query.kcurprice= cinfo.iunitcurprice
                        
                        update_query.iunitcurprice=curprice
                        update_query.ktotalcurprice=totprice
                        update_query.ktotalbuyprice=totbuyprice

                        update_query.kprofitratio=profitratio

                        update_query.ktotalprevbuyprice=cinfo.ktotalbuyprice
                        update_query.ktotalprevprice=cinfo.ktotalcurprice
                        update_query.kprofitpreratio=cinfo.kprofitratio




                        update_query.iupdatedate=now

                        update_queries.append(update_query) 
                    
                        i = i + 1


                print('주식 한방 업데이트 시작')
                print(datetime.datetime.now())
                if update_queries is not None : # 마지막 행일 때 한방 업데이트
                    MyStocks.objects.bulk_update(update_queries, ['kcurrencyrate','kbuyprice','kcurprice','iunitcurprice',
                    'ktotalcurprice','ktotalbuyprice','kprofitratio','ktotalprevbuyprice','ktotalprevprice','kprofitpreratio','iupdatedate'])
                    print(datetime.datetime.now())
                    print('주식 한방 업데이트 종료')
                    

            
            elif(len(yfsearch) == 1) :

                update_queries = []

                print('df.iloc[-1] : ',df.iloc[-1])
                curprice = df.iloc[-1]
                curcode = yfsearch[0]
                curcode = curcode.replace('.KS','')
                curcode = curcode.replace('.KQ','')

                cinfo = MyStocks.objects.filter(author=request.user, icode=curcode)[0]


                # print(cinfo)
                # print('cinfo.iquantity :', cinfo.iquantity)
                # print('cinfo.iunitbuyprice :', cinfo.iunitbuyprice)
                totprice = float(cinfo.iquantity) * curprice
                totbuyprice = float(cinfo.iquantity) * float(cinfo.iunitbuyprice)

                # 해외주식의 경우 USD 환율 계산
                fcurrencyusd = float(currencyusd)
                # print(fcurrencyusd)

                if cinfo.invst_type == 2 : # 해외주식의 경우 평가금액에 환율을 곱한다.
                    totprice = totprice * fcurrencyusd
                    totbuyprice = totbuyprice * fcurrencyusd


                
                gap = float(curprice) - float(cinfo.iunitbuyprice)
                # print(gap)
                gapper = gap / float(cinfo.iunitbuyprice)
                # print(gapper)
                profitratio = gapper * 100
                # print(profitratio)



                update_query = MyStocks.objects.get(author=request.user, icode=curcode)
                
                if cinfo.invst_type == 2 :
                    update_query.kcurrencyrate=float(currencyusd) 
                    update_query.kbuyprice=float(currencyusd) * float(cinfo.iunitbuyprice)
                    update_query.kcurprice= float(currencyusd) * float(cinfo.iunitcurprice)
                else :
                    update_query.kcurrencyrate= 1 
                    update_query.kbuyprice= cinfo.iunitbuyprice
                    update_query.kcurprice= cinfo.iunitcurprice


                

                update_query.iunitcurprice=curprice
                update_query.ktotalcurprice=totprice
                update_query.ktotalbuyprice=totbuyprice
                update_query.kprofitratio=profitratio

                update_query.ktotalprevbuyprice=cinfo.ktotalbuyprice
                update_query.ktotalprevprice=cinfo.ktotalcurprice
                update_query.kprofitpreratio=cinfo.kprofitratio


                update_query.iupdatedate=now

                update_queries.append(update_query) 
                
                print('주식 한방 업데이트 시작')
                print(datetime.datetime.now())
                if update_queries is not None : # 마지막 행일 때 한방 업데이트
                    MyStocks.objects.bulk_update(update_queries, ['kcurrencyrate','kbuyprice','kcurprice','iunitcurprice',
                    'ktotalcurprice','ktotalbuyprice','kprofitratio','ktotalprevbuyprice','ktotalprevprice','kprofitpreratio','iupdatedate'])
                    print(datetime.datetime.now())
                    print('주식 한방 업데이트 종료')

                # MyStocks.objects.filter(author=request.user, icode=curcode).update(iunitcurprice=curprice)
                # MyStocks.objects.filter(author=request.user, icode=curcode).update(ktotalcurprice=totprice)
                # MyStocks.objects.filter(author=request.user, icode=curcode).update(kprofitratio=profitratio)
                # MyStocks.objects.filter(author=request.user, icode=curcode).update(iupdatedate=now)

            
            endtime =  datetime.datetime.now()
            print('endtime', datetime.datetime.now())


            print('end-start time ', endtime - starttime)

        
    # 현재가, 평가금액,수익률 저장하기 (코인)
    update_queries = []
    for code in upbitsearch:
        print('현재가, 평가금액,수익률 저장하기 (코인)')
        curprice = pyupbit.get_current_price(code)
        MyStocks.objects.filter(author=request.user, icode=code).update(iunitcurprice=curprice)


        codeinfo = MyStocks.objects.filter(author=request.user, icode=code)
        i = 0
        for ci in codeinfo:
            cinfo = MyStocks.objects.filter(author=request.user, icode=code)[i]

            if curprice == None:
                messages.error(request, "curprice == None : " + code )     
                continue


            print(cinfo)
            print('cinfo.iquantity :', cinfo.iquantity)
            totprice = float(cinfo.iquantity) * curprice
            print('cinfo.iunitbuyprice :', cinfo.iunitbuyprice)

            totbuyprice = float(cinfo.iquantity) * float(cinfo.iunitbuyprice)

            # 해외주식의 경우 USD 환율 계산
            fcurrencyusd = float(currencyusd)
            # print(fcurrencyusd)



            gap = float(curprice) - float(cinfo.iunitbuyprice)
            print(gap)
            gapper = gap / float(cinfo.iunitbuyprice)
            print(gapper)
            profitratio = (gapper * 100)
            print(profitratio)

            # profitratio = (((float(curprice) - float(cinfo.iunitbuyprice))/float(cinfo.iunitbuyprice)) * 100)

            #기존 업데이트 문
            # MyStocks.objects.filter(author=request.user, icode=code, pk=cinfo.pk).update(iunitcurprice=curprice)
            # MyStocks.objects.filter(author=request.user, icode=code, pk=cinfo.pk).update(ktotalcurprice=totprice)
            # MyStocks.objects.filter(author=request.user, icode=code, pk=cinfo.pk).update(kprofitratio=profitratio)
            # MyStocks.objects.filter(author=request.user, icode=code, pk=cinfo.pk).update(iupdatedate=now)


            #신규 업데이트 문
            update_query_bitcoin = MyStocks.objects.get(author=request.user, icode=code, pk=cinfo.pk)

            update_query_bitcoin.iunitcurprice=curprice
            update_query_bitcoin.kcurrencyrate= 1 
            update_query_bitcoin.kbuyprice= cinfo.iunitbuyprice
            update_query_bitcoin.kcurprice= cinfo.iunitcurprice
            update_query_bitcoin.ktotalcurprice=totprice
            update_query_bitcoin.ktotalbuyprice=totbuyprice
            update_query_bitcoin.kprofitratio=profitratio
            
            update_query_bitcoin.ktotalprevbuyprice=cinfo.ktotalbuyprice
            update_query_bitcoin.ktotalprevprice=cinfo.ktotalcurprice
            update_query_bitcoin.kprofitpreratio=cinfo.kprofitratio

            


            update_query_bitcoin.iupdatedate=now

            update_queries.append(update_query_bitcoin) 

            i = i + 1

    print('Coin 한방 업데이트 시작')
    print(datetime.datetime.now())
    if update_queries is not None : # 마지막 행일 때 한방 업데이트
        MyStocks.objects.bulk_update(update_queries, ['iunitcurprice','kcurrencyrate','kbuyprice','kcurprice','ktotalcurprice',
        'ktotalbuyprice','kprofitratio','ktotalprevbuyprice','ktotalprevprice','kprofitpreratio','iupdatedate'])
        print(datetime.datetime.now())
        print('Coin 한방 업데이트 종료')





    # # 업데이트 안된 종목은 모두 0 으로 처리 (예: 관리종목..)
    # import decimal
    # queryset = MyStocks.objects.filter(author=request.user,iunitcurprice=decimal.Decimal('NaN'))
    # for entry in queryset:
    #     print('No information : ', entry)
    #     entry.iunitcurprice = 0
    #     entry.kprofitratio = -100
    #     entry.ktotalcurprice = 0
    #     entry.save()



    # balances 테이블 업데이트

    updatebalances_queries = []
    balances = Balances.objects.all()
    # 해당 사용자 데이터만 필터링
    balancesforuser = balances.filter(bauthor=request.user).order_by('-bdate')


    for bcforuser in balancesforuser:
        gapamount =  ((float)(bcforuser.bamount) - (float)(bcforuser.bincreased)) 

        if (bcforuser.bincreased is None or gapamount == 0 or isNaN(bcforuser.bincreased)):
            bincreasedratio = 0
        else:
            bincreasedratio = (float)(bcforuser.bincreased)  / gapamount * 100
        
        print('bcforuser.bincreasedratio : ',bcforuser.bincreasedratio)
        # bcforuser.objects.filter(bincreased=bcforuser.bincreased,bamount=bcforuser.bamount,pk = bcforuser.pk).update(bincreasedratio=bincreasedratio)

        update_query_balances = Balances.objects.get(bincreased=bcforuser.bincreased,bamount=bcforuser.bamount,pk = bcforuser.pk)

        update_query_balances.bincreasedratio=bincreasedratio
        updatebalances_queries.append(update_query_balances) 

    
    print('Balances 한방 업데이트 시작')
    print(datetime.datetime.now())
    if updatebalances_queries is not None : # 마지막 행일 때 한방 업데이트
        Balances.objects.bulk_update(updatebalances_queries, ['bincreasedratio'])
        print(datetime.datetime.now())
        print('Balances 한방 업데이트 종료')


    # 현재시간업데이트
    now = datetime.datetime.now()
    timeupdate = MyStocks.objects.filter(author=request.user).update(iupdatedate=now) 



    # 수행 시간 측정
    refrestendtime = datetime.datetime.now()
    runningtime = refrestendtime - refresstarttime
    print('runningtime : ', runningtime)
    runningtimedelta = format(runningtime.total_seconds(),".1f")
    print('runningtimedelta : ', runningtimedelta)
    messages.success(request, "All the data have been updated successfully! (" + runningtimedelta + " seconds)"  )


    # index 로 돌아가기
    return redirect('index')             # view_name 사용


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'examples/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')


def mystocks(request):
    print('def mystocks(request): started.........')
    data = dict()
    if request.method == 'GET':
        # mystocks = MyStocks.objects.all()
        # 해당 사용자 데이터만 필터링
        mystocksforuser = MyStocks.objects.filter(author=request.user).order_by('-kprofitratio')

        print('888888888888888888888888888888888888888888888888888888888')
        data['table'] = render_to_string(
            '_mystocks_table.html',
            {'mystocks': mystocksforuser},
            request=request
        )
        return JsonResponse(data)


def balances(request):
    print('def balances(request): started............')
    data = dict()
    print('8555555555555555555555555')
    if request.method == 'GET':
        # balances = Balances.objects.all()
        # # 해당 사용자 데이터만 필터링
        # balancesforuser = balances.filter(author=request.user).order_by('-bdate')




        # for bcforuser in balancesforuser:
        #     bincreasedratio = (float)(bcforuser.bincreased)  / ((float)(bcforuser.bamount) - (float)(bcforuser.bincreased)) * 100
        #     print('bcforuser.bincreasedratio : ',bcforuser.bincreasedratio)
        #     bcforuser.objects.filter(bincreased=bcforuser.bincreased,bamount=bcforuser.bamount,pk = bcforuser.pk).update(bincreasedratio=bincreasedratio)


        # 수익률 업데이트 후 재 조회
        balancesforuser = balances.filter(author=request.user).order_by('-bdate')

        print('balancesforuser : ',balancesforuser)
        print('888888888888888888888888888888888888888888888888888888888')
        data['table'] = render_to_string(
            '_balances_table.html',
            {'balances': balancesforuser},
            request=request
        )
        return JsonResponse(data)


def isNaN(num):
    return num != num

def divide_list(l, n): 
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(l), n): 
        yield l[i:i + n] 
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm, BSModalModelForm_Balances
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin, CreateUpdateAjaxMixin_Balances
from .models import MyStocks, Balances
from django.conf import settings

class MyStockFilterForm(BSModalForm):
    type = forms.ChoiceField(choices=MyStocks.INVST_TYPES)

    class Meta:
        fields = ['type', 'clear']




class MyStockModelForm(BSModalModelForm):
    # publication_date = forms.DateField(
    #     error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    # )

    print("dddddddddddddddddddddddddddddddddddddddddddddddddd")

    class Meta:
        model = MyStocks
        exclude = ['iname','iunitcurprice','kcurrencyrate','kbuyprice','kcurprice',
        'ktotalcurprice','kprofitratio','ktotalbuyprice','ktotalprevbuyprice','ktotalprevprice','kprofitpreratio',
        'business','detail','discuss_url','kcurrencyrate','timestamp','author']

class BalancesModelForm(BSModalModelForm_Balances):
    # publication_date = forms.DateField(
    #     error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    # )

    bdate = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )


    print("dddddddddddddddddddddddddddddddddddddddddddddddddd")

    
    class Meta:
        model = Balances
        exclude = ['bauthor','bincreasedratio']

class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomUserCreationForm_Balances(PopRequestMixin, CreateUpdateAjaxMixin_Balances, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

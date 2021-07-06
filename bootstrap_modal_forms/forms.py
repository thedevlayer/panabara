from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin,CreateUpdateAjaxMixin_Balances


class BSModalForm(PopRequestMixin, forms.Form):
    print('===============BSModalForm started =================')
    pass

class BSModalForm_Balances(PopRequestMixin, forms.Form):
    print('===============BSModalForm started =================')
    pass

class BSModalModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    print('===============BSModalModelForm started =================')
    pass


class BSModalModelForm_Balances(PopRequestMixin, CreateUpdateAjaxMixin_Balances, forms.ModelForm):

    print('===============BSModalModelForm started =================')
    pass
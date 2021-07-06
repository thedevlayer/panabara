from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect

from examples.models import StockBaseInfo

class PassRequestMixin(object):
    """
    Mixin which puts the request into the form's kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super(PassRequestMixin, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class PopRequestMixin(object):
    """
    Mixin which pops request out of the kwargs and attaches it to the form's
    instance.

    Note: This mixin must precede forms.ModelForm/forms.Form. The form is not
    expecting these kwargs to be passed in, so they must be popped off before
    anything else is done.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PopRequestMixin, self).__init__(*args, **kwargs)


class CreateUpdateAjaxMixin(object):
    """
    Mixin which passes or saves object based on request type.
    """

    def save(self, commit=True):
        # if not self.request.is_ajax() or self.request.POST.get('closeOnSubmit') == 'False':
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            instance.author = self.request.user

            ## 입력된 code 값으로 StockBaseInfo 의 정보 불러와 데이터에 저장한다.
            # qs = StockBaseInfo.objects.all()


            try:
                scode = instance.icode
                c = StockBaseInfo.objects.get(code=scode)
            except :
                c = None
 
            if c : # StockBaseInfo 에 있을 경우는 해당 값으로 업데이트
                instance.iname = c.name
                instance.business = c.business
                instance.detail = c.detail
                instance.discuss_url = c.discuss_url
            else :
                try:
                    instance.iname = '-'
                    instance.business = '-'
                    instance.detail = '-'
                    instance.discuss_url = '-'
                except : # 가입할때도 여기타므로 StockBaseInfo 와는 무관함.
                    pass

            instance.save()
            print('instance.save()...................')
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
        return instance


class CreateUpdateAjaxMixin_Balances(object):
    """
    Mixin which passes or saves object based on request type.
    """

    def save(self, commit=True):

        print('CreateUpdateAjaxMixin_Balances started ===============')
        # if not self.request.is_ajax() or self.request.POST.get('closeOnSubmit') == 'False':
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            instance = super(CreateUpdateAjaxMixin_Balances, self).save(commit=commit)
            print('self.request.user: ',self.request.user)
            print('instance.bamount', instance.bamount)
            

            try:
                c = Balances.objects.get(bauthor=self.request.user, bamount=instance.bamount, bincreased=instance.bincreasedratio)
            except :
                c = None
 
            if (float)(instance.bincreased) > 0 and  (float)(instance.bamount) > 0: # Balances 에 있을 경우는 해당 값으로 업데이트
                instance.bauthor = self.request.user
                instance.bincreasedratio =  (float)(instance.bincreased)  / ((float)(instance.bamount) - (float)(instance.bincreased)) * 100
                print('*********instance.bincreasedratio',instance.bincreasedratio)

            else :
                instance.bauthor = self.request.user
                instance.bincreasedratio = 0
    
            instance.save()
            print('instance.save()...................')
        else:
            instance = super(CreateUpdateAjaxMixin_Balances, self).save(commit=False)
        return instance

class DeleteMessageMixin(object):
    """
    Mixin which adds message to BSModalDeleteView.
    """

    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super(DeleteMessageMixin, self).delete(request, *args, **kwargs)


class LoginAjaxMixin(object):
    """
    Mixin which authenticates user if request is not ajax request.
    """

    def form_valid(self, form):
        if not self.request.is_ajax():
            auth_login(self.request, form.get_user())
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

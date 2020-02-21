from django import forms
from django.contrib.auth.hashers import check_password
from .models import Shopuser

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요'
        },
        max_length=64, label='email'
    )

    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='password'
    )

    re_password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='password confirm'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')



class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요'
        },
        max_length=64, label='email'
    )

    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='password'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                shopuser = Shopuser.objects.get(email=email)
            except Shopuser.DoesnotExist:
                self.add_error('email', '아이디가 없습니다.')
                return
            
            if not check_password(password, shopuser.password):
                self.add_error('password', '비밀번호를 틀렸습니다.')

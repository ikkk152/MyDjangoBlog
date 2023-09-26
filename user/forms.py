from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_redis import get_redis_connection

from user.models import Users


class BootStrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            old_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = '{} form-control'.format(old_class)
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)


class RegisterModelForm(BootStrapForm, UserCreationForm):
    email = forms.EmailField(label='邮箱', required=True)
    code = forms.CharField(label='验证码', max_length=6)

    password1 = forms.CharField(widget=forms.PasswordInput, label='密码',
                                min_length=8, max_length=20,
                                help_text='请输入8到20个字符的密码。')
    password2 = forms.CharField(widget=forms.PasswordInput, label='确认密码',
                                min_length=8, max_length=20,
                                help_text='再次输入密码以确认。')

    class Meta:
        model = Users
        fields = ['username', 'email', 'code', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册!')
        return email

    def clean_code(self):
        email = self.cleaned_data.get('email')
        code = self.cleaned_data.get('code')
        redis_conn = get_redis_connection("default")
        redis_code = redis_conn.get(email).decode()
        if code != redis_code:
            raise forms.ValidationError('验证码错误')
        else:
            redis_conn.delete(email)


class CustomAuthenticationForm(BootStrapForm, AuthenticationForm):
    username = forms.EmailField(label='邮箱', required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not Users.objects.filter(email=username).exists():
            raise forms.ValidationError('账号不存在!')
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        self.user_cache = authenticate(
            self.request, email=username, password=password
        )
        if self.user_cache is None:
            raise forms.ValidationError('账号或密码错误!')
        else:
            self.confirm_login_allowed(self.user_cache)
        return password

    def clean(self):
        return self.cleaned_data

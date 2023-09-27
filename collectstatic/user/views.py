from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django_redis import get_redis_connection

from article.models import Article
from user import forms
from user.forms import CustomAuthenticationForm, RegisterModelForm
from user.models import Users
from utils.random_code import get_random_code
from django.forms import ValidationError
from django.core.mail import send_mail


class RegisterView(CreateView):
    model = Users
    template_name = 'user/register.html'
    form_class = forms.RegisterModelForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    authentication_form = CustomAuthenticationForm
    next_page = 'index'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


def user_logout(request):
    logout(request)
    return redirect('index')


class SendCode(View):
    """
    发送验证码视图，通过ajax发送请求
    随机生成验证码将验证码保存至redis，设置三分钟有效并且视图限流，一分钟内不能再次访问
    """

    def post(self, request):
        form = RegisterModelForm(request.POST)
        form.is_valid()
        if 'email' in form.errors:
            return JsonResponse({'success': False, 'errors': form.errors['email'][0]})
        try:
            email = form.clean_email()
        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': str(e)})

        code = get_random_code()
        redis_conn = get_redis_connection("default")
        redis_conn.setex(email, 60 * settings.CODE_EXPIRE_MINUTE, code)
        content = f'''
        验证您的电子邮件地址
        感谢您注册个人博客账户。为确保当前是您本人操作，请您输入此邮件中提示的验证码以完成账户注册。如您无需注册此账户，请忽略该信息。
        验证码：{code}
        (此验证码将在发送后 {settings.CODE_EXPIRE_MINUTE} 分钟过期。)
        '''
        send_mail('测试发送',
                  content,
                  'ikkk152@163.com',
                  [email, ],  # 这里可以同时发给多个收件人
                  fail_silently=False
                  )
        return JsonResponse({'success': True})


class UserDetail(DetailView):
    model = Users
    template_name = 'user/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        articles = Article.objects.filter(user=user)
        context['articles'] = articles
        return context


class UserProfile(ListView):
    model = Article
    paginate_by = 4
    template_name = 'user/detail.html'

    def get_queryset(self):
        self.user = get_object_or_404(Users, id=self.kwargs['pk'])
        return super().get_queryset().filter(user=self.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['user'] = self.user
        return context

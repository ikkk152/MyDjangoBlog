from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from user import forms
from user.forms import CustomAuthenticationForm
from user.models import Users


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

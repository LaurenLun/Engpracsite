from django.shortcuts import render, redirect
from . import forms
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import FormView, UpdateView
from .forms import RegistForm, UserLoginForm, UserInfoForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, get_user
from django.views import View

# Create your views here.

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class RegistUserView(CreateView):
    template_name = 'accounts/us_regist.html'
    form_class = RegistForm
    success_url = '/accounts/us_login/'
    
    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.save()
            messages.success(self.request, "ユーザー登録に成功しました")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return render(self.request, 'accounts/error_page.html', {'error': str(e)})
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/us_login.html'
    authentication_form = UserLoginForm
    
    def form_valid(self, form):
        # email = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        # remember = form.cleaned_data.get('remember')
        # user = authenticate(self.request, email=email, password=password)
        response = super().form_valid(form)
        messages.success(self.request, "ログインに成功しました。")
        print("Message added:", list(messages.get_messages(self.request)))
        return response
        
        # if remember:
        #     # 如果用戶選擇了"記住我"，將會話設置為更長的過期時間
        #     self.request.session.set_expiry(1209600)  # 2週
        # else:
        #     # 否則使用默認的會話過期時間
        #     self.request.session.set_expiry(0)
        
        # if user is not None and user.is_active:
        #     login(self.request, user)
        #     messages.success(self.request, "ログインに成功しました。")
        #     print(f"User {user.email} logged in successfully")
        #     return super().form_valid(form)
        # elif user is not None and not user.is_active:
        #     messages.error(self.request, 'アカウントがアクティブではありません。')
        #     print(f"User {user.email} is not active")
        #     return self.form_invalid(form)
        # else:
        #     messages.error(self.request, 'ログインに失敗しました。メールアドレスとパスワードを確認してください。')
        #     print("Authentication failed")
        #     return self.form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, "ログインに失敗しました。メールアドレスとパスワードを確認してください。")
        return super().form_invalid(form)
    
    def get_success_url(self):
        # 確保消息在重定向後仍然存在
        # return self.get_redirect_url() or self.get_default_redirect_url()
        return reverse_lazy('boards:list_themes')
  

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print(f"Form fields: {self.get_form().fields}")
    return context



class UserLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "ログアウトしました。")
        return redirect('boards:list_themes')

class UserInfoView(LoginRequiredMixin, FormView):
    template_name = 'accounts/us_info.html'
    form_class = UserInfoForm
    success_url = reverse_lazy('accounts:us_info')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        kwargs['initial'] = {
            'usname' : self.request.user.usname,
            'email' : self.request.user.email,
        }
        return kwargs
    
    def us_login(request):
        userlogin_form = UserLoginForm(request.POST or None)
        if userlogin_form.is_valid():
            email = userlogin_form.cleaned_data.get('username')  # 这里是email
            password = userlogin_form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
    
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        messages.success(self.request, "ユーザー情報を更新しました")
        return super().form_valid(form)

class UpdateUserInfoView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserInfoForm
    template_name = 'accounts/update_us_info.html'
    success_url = reverse_lazy('accounts:us_info')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # form.update(user=self.request.user)
        user = form.save(commit=False)
        password_changed = False
        if form.cleaned_data['password']:
            print("Password is being changed")
            user.set_password(form.cleaned_data['password'])
            password_changed = True
        user.save()
        
        if password_changed:
            print("Updating session auth hash")
            update_session_auth_hash(self.request, user)
        
        # from django.contrib.auth import get_user
        current_user = get_user(self.request)
        print(f"Is user authenticated after password change: {current_user.is_authenticated}")
    
        messages.success(self.request, 'ユーザー情報が更新されました。')
        return HttpResponseRedirect(reverse('accounts:us_info'))
        # return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                if field != '__all__': 
                    messages.error(self.request, f"{form.fields[field].label}: {error}")
                else:
                    messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))
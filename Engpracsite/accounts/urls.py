from django.urls import path
from django.contrib.auth import views as auth_views
from .views import(
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserInfoView,  UpdateUserInfoView,
    )

app_name = 'accounts'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('us_regist/', RegistUserView.as_view(), name='us_regist'),
    path('us_login/', auth_views.LoginView.as_view(template_name='accounts/us_login.html'), name='us_login'),
    path('us_logout/', UserLogoutView.as_view(), name='us_logout'),
    path('us_info/', UserInfoView.as_view(), name='us_info'),
    path('update_us_info/', UpdateUserInfoView.as_view(), name='update_us_info'),
]
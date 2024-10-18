from django import forms
from .models import Users
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
import re


class RegistForm(forms.ModelForm):
    usname = forms.CharField(label='名前', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput(attrs={'class': 'form-control'}))    
    
    class Meta():
        model = Users
        fields = ('usname', 'email', 'password', 'confirm_password')
        
        labels = {
            'usname': '名前', 
            'email': 'メールアドレス',
            'password': 'パスワード', 
            'confirm_password': '確認用パスワード',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")        
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("パスワードが一致しません")
        
        if password:
            try:
                validate_password(password, self)
            except ValidationError as e:
                self.add_error('password', e)
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')        
        user.set_password(password)
        user.is_active = True
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス', max_length=150, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember = forms.BooleanField(label='ログイン状態を保持する', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # self.fields['username'].label = 'メールアドレス'
        # self.fields['password'].label = 'パスワード'
        # self.fields['remember'].label = 'ログイン状態を保持する'
        # super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update({'autofocus': True})
    
    def clean_username(self):
        email = self.cleaned_data.get('username')
        if email:
            try:
                user = User.objects.get(email=email)
                return email
            except User.DoesNotExist:
                raise forms.ValidationError("このメールアドレスに関連付けられたユーザーが見つかりません。")
        return email

User = get_user_model() 


class UserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = User
        fields = (
            'usname',
            'email',
        )
        labels = {
            'usname': '名前', 
            'email': 'メールアドレス',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 設置必填欄位
        self.fields['usname'].required = True
        self.fields['email'].required = True
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['email'].label = 'メールアドレス'
        self.fields['password'].label = 'パスワード'
        self.fields['confirm_password'].label = '確認用パスワード'
        
        # self.fields['email'].widget.attrs['placeholder'] = '変更する場合のみ入力してください'
        self.fields['password'].widget.attrs['placeholder'] = '変更する場合のみ入力してください'
        self.fields['confirm_password'].widget.attrs['placeholder'] = '変更する場合のみ入力してください'

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password
    
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error('email', 'このメールアドレスは既に使用されています。')

        if password and not confirm_password:
            raise ValidationError("確認用パスワードを入力してください。")
        elif password and password != confirm_password:
            raise ValidationError("パスワードと確認用パスワードが一致しません。")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['email']:
            user.email = self.cleaned_data['email']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
        
    def update(self, user):
        user.usname = self.cleaned_data['usname']
        # user.email = self.cleaned_data['email']
        user.save()

   

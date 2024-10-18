from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, Comments
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
# Create your views here.

def create_theme(request):
    
    if not request.user.is_authenticated:
        return render(request, 'boards/create_theme_login_required.html')
    
    # if request.user.is_authenticated:
    if request.method == 'POST':
        create_theme_form = forms.CreateThemeForm(request.POST)
        if create_theme_form.is_valid():
            create_theme_form.instance.user = request.user
            create_theme_form.save()
            messages.success(request, '掲示板作成しました')
            return redirect('boards:list_themes')
    
    else:
        create_theme_form = forms.CreateThemeForm()
        
    return render(
        request, 'boards/create_theme.html', context={
            'create_theme_form': create_theme_form
        }
    )
    # else:
    #     return render(request, 'boards/create_theme_login_required.html')
    
    
def list_themes(request):
    themes = Themes.objects.fetch_all_themes()
    return render(
        request, 'boards/list_themes.html', {'themes': themes}
    )


def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )


def custom_permission_denied_view(request, exception):
    return render(request, 'errors_403.html', status=403)


@login_required
def delete_theme(request, theme_id):
    theme = get_object_or_404(Themes, id=theme_id)
    if theme.user != request.user:
        raise PermissionDenied("削除権限を持ってないやで")
    
    if request.method == 'POST':
        theme.delete()
        messages.success(request, '掲示板を削除しました')
        return redirect('boards:list_themes')
    
    return render(request, 'boards/delete_theme.html', {'theme': theme})



def view_comments(request, theme_id):
    theme = get_object_or_404(Themes, id=theme_id)
    comments = Comments.objects.fetch_by_theme_id(theme_id)
    
    paginator = Paginator(comments, 10)  # 每頁顯示10條評論
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    post_comment_form = forms.PostCommentForm()
    
    return render(
        request, 'boards/post_comments.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )


@login_required
def post_comment(request, theme_id):
    if request.method == 'POST':
        post_comment_form = forms.PostCommentForm(request.POST)
        theme = get_object_or_404(Themes, id=theme_id)
        
        if post_comment_form.is_valid():
            comment = post_comment_form.save(commit=False)
            comment.theme = theme
            comment.user = request.user
            comment.save()
            messages.success(request, 'コメントが投稿されました。')
        else:
            messages.error(request, 'コメントの投稿に失敗しました。')
    
    return redirect('boards:view_comments', theme_id=theme_id)


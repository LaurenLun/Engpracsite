from django import forms
from .models import Themes, Comments

class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    
    class Meta:
        model = Themes
        fields = ('title',)
        

class DeleteThemeForm(forms.ModelForm):
    
    class Meta:
        model = Themes
        fields = []
        

class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='コメント', 
        widget=forms.Textarea(attrs={'rows':5, 'class': 'form-control'}), 
        max_length=1000,
        )
    
    class Meta:
        model = Comments
        fields = ('comment',)
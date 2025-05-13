from django import forms

from blog.models import Blog, Comment
from django_summernote.widgets import SummernoteWidget


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('category', 'title', 'image', 'content', )
        widgets ={
            'content':SummernoteWidget()
        }
            #'__all__'



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = { # 댓글창
            'content': forms.TextInput(attrs={'class':'form-control', 'a':'b'})
        }
        labels = {
            'content' : '댓글'
        }
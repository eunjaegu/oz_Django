from django import forms

from blog.models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content')
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
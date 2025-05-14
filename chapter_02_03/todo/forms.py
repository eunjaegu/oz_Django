from django import forms
from todo.models import Todo, Comment
from django_summernote.widgets import SummernoteWidget


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'thumbnail','description', 'start_date', 'end_date', ]
        labels = {
            'title': '할 일 제목',
            'thumbnail': '이미지',
            'description': '상세 내용',
            'start_date': '시작 날짜',
            'end_date': '마감 날짜',
        }
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'})
        }


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'thumbnail', 'description', 'start_date', 'end_date', 'is_complete']
        labels = {
            'title': '할 일 제목',
            'thumbnail': '이미지',
            'description': '상세 내용',
            'start_date': '시작일',
            'end_date': '종료일',
            'is_complete': '완료 여부',
        }
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', ]
        labels = {
            'message': '내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3, 'cols': 40, 'class': 'form-control', 'placeholder': '댓글 내용을 입력해주세요.'
            }),
        }

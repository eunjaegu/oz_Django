from django import forms

from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date', 'is_complete']
        labels = {
            'title': '할 일 제목',
            'description': '상세 내용',
            'start_date': '시작 날짜',
            'end_date': '마감 날짜',
            'is_complete': '완료 여부',
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date', 'is_complete']
        labels = {
            'title': '할 일 제목',
            'description': '상세 내용',
            'start_date': '시작일',
            'end_date': '종료일',
            'is_complete': '완료 여부',
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

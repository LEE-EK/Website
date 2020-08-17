from django import forms
from board.models import Post
from board.models import Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }

  
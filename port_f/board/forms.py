from django import forms
from board.models import Notice,From_mark,To_mark,Freetalk,Auth,Question,Inquiry,Report
from board.models import Notice_Comment,From_mark_Comment,To_mark_Comment,\
                            Freetalk_Comment,Auth_Comment,Question_Comment,Inquiry_Comment,Report_Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }
   
class Notice_CommentForm(forms.ModelForm):
    class Meta:
        model = Notice_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }

#######################################################################################################

class From_markForm(forms.ModelForm):
    class Meta:
        model = From_mark
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }
      
class From_mark_CommentForm(forms.ModelForm):
    class Meta:
        model = From_mark_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }
        
#######################################################################################################

class To_markForm(forms.ModelForm):
    class Meta:
        model = To_mark
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }
      
class To_mark_CommentForm(forms.ModelForm):
    class Meta:
        model = To_mark_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }

#######################################################################################################

class FreetalkForm(forms.ModelForm):
    class Meta:
        model = Freetalk
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }
      
class Freetalk_CommentForm(forms.ModelForm):
    class Meta:
        model = Freetalk_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }

#######################################################################################################

class AuthForm(forms.ModelForm):
    class Meta:
        model = Auth
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }
      
class Auth_CommentForm(forms.ModelForm):
    class Meta:
        model = Auth_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }

#######################################################################################################

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        
        fields= ['subject', 'memo']

        labels = {
            'subject': '제목',
            'memo': False
        }        

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':'게시글 제목을 입력하세요.'}),
            'memo': SummernoteWidget(attrs={'class':'memo'})
        }
      
class Question_CommentForm(forms.ModelForm):
    class Meta:
        model = Question_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'placeholder':'댓글을 작성해 주세요.','class':'form-control','rows':5}),
        }

#######################################################################################################

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'class':'form-control','rows':5}),
        }

class Inquiry_CommentForm(forms.ModelForm):
    class Meta:
        model = Inquiry_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'class':'form-control','rows':5}),
        }        

#######################################################################################################

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'class':'form-control','rows':5}),
        }


class Report_CommentForm(forms.ModelForm):
    class Meta:
        model = Report_Comment

        fields = ['text',]

        labels = {
            "text" : False
        }

        widgets = {
            "text":forms.Textarea(attrs={'class':'form-control','rows':5}),
        }         
from django import forms
from member.models import Member

# 로그인 폼
class LoginForm(forms.Form):
    member_id = forms.CharField(label=False, max_length = 50, widget=forms.TextInput(attrs={'class':'fadeIn second','placeholder':'ID'}))
    member_pw = forms.CharField(label=False, max_length = 100, widget=forms.PasswordInput(attrs={'class':'fadeIn thrid', 'placeholder':'password'}))

# 회원가입 폼
class SignupForm(forms.Form):
    member_id = forms.CharField(label = '아이디 ', min_length= 4, max_length = 16, widget=forms.TextInput(attrs={'class':'form-input','placeholder':'영문 소문자/숫자, 4~16자'}))
    member_pw = forms.CharField(label = '비밀번호 ', min_length= 4, max_length = 16, widget=forms.PasswordInput(attrs={'class':'form-input','placeholder':'영문 대소문자/숫자, 4~16자'}))
    member_pw_r = forms.CharField(label = '비밀번호 확인 ', min_length= 4, max_length = 16, widget=forms.PasswordInput(attrs={'class':'form-input'}))
    nickname = forms.CharField(label = '닉네임' , max_length = 50, widget=forms.TextInput(attrs={'class':'form-input'}))
    member_name = forms.CharField(label = '이름 ', max_length =50, widget=forms.TextInput(attrs={'class':'form-input'}))
    address = forms.CharField(label = '주소 ', max_length=200, required=False, widget=forms.TextInput(attrs={'class':'form-input','readonly':'readonly'}))
    address_in = forms.CharField(label = '상세주소 ', max_length=200, required=False, widget=forms.TextInput(attrs={'class':'form-input'}))
    phone_no = forms.CharField(label = '휴대전화 ', required=False, widget=forms.TextInput(attrs={'class':'form-input','placeholder':'ex) 010-1234-5678'}))
    email = forms.EmailField(label = '이메일주소 ', widget=forms.EmailInput(attrs={'class':'form-input','placeholder':'ex) mark123@gmail.com'}))

# 아이디찾기 폼
class FindIdForm(forms.Form):
    member_name = forms.CharField(label =False, max_length =50, widget=forms.TextInput(attrs={'class':'fadeIn second','placeholder':'이름'}))
    email = forms.EmailField(label =False, widget=forms.EmailInput(attrs={'class':'fadeIn thrid','placeholder':'이메일 주소'}))

# 비밀번호찾기 폼
class FindPasswdForm(forms.Form):
    member_id = forms.CharField(label=False, max_length = 50, widget=forms.TextInput(attrs={'class':'fadeIn second','placeholder':'아이디'}))
    member_name = forms.CharField(label =False, max_length =50, widget=forms.TextInput(attrs={'class':'fadeIn second','placeholder':'이름'}))
    email = forms.EmailField(label =False, widget=forms.EmailInput(attrs={'class':'fadeIn thrid','placeholder':'이메일 주소'}))

# 비밀번호 변경 폼
class PasswdUpForm(forms.Form):
    member_pw = forms.CharField(label =False, max_length = 200, widget=forms.PasswordInput(attrs={'class':'fadeIn second','placeholder':'새 비밀번호'}))
    member_pw_r = forms.CharField(label =False, max_length = 200, widget=forms.PasswordInput(attrs={'class':'fadeIn thrid','placeholder':'새 비밀번호 확인'}))
    

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from .forms import LoginForm
from .forms import SignupForm
from .forms import FindIdForm
from .forms import FindPasswdForm
from .forms import PasswdUpForm

from member.models import Member

from django.http import HttpResponse
from django.urls import reverse


# 이용약관
class Agreement(TemplateView):
    template_name = 'member/agreement.html'

# 개인정보처리방침
class Privacy(TemplateView):
    template_name = 'member/privacy.html'

# 회원가입완료화면
class SiResultView(DetailView):
    model = Member
    template_name = 'member/signup_result.html'
    context_object_name = "result"

# 로그인 폼 처리
def loginform(request):
    # POST 방식이면, 데이터가 담긴 제출된 폼으로 간주합니다.
    if request.method == 'POST':
        # request에 담긴 데이터로, 클래스 폼을 생성합니다.
        form = LoginForm(request.POST)
        # 폼에 담긴 데이터가 유효한지 체크한다
        if form.is_valid():
           member_id = request.POST['member_id']
           member_pw = request.POST['member_pw']
           save_session(request, member_id)

           if Member.objects.filter(member_id = member_id, member_pw = member_pw):
               # 세션으로 로그인 정보 저장시키기
               # obj = Member.objects.get(member_id = member_id)
               save_session(request, member_id)
               return redirect('index')

           else:
               # 로그인 실패이유 (유효성검사)
               message="실패"
               return render(request, 'member/login.html', {'form':form, 'message':message})
           
    else: # GET 방식
        form = LoginForm()
        return render(request, 'member/login.html', {'form':form})

# 로그아웃
def logout(request):
    try:
        del request.session['member_id']
    except:
        pass
    return redirect('index')

# 세션 정보
def save_session(request, member_id):
    request.session['member_id'] = member_id       

# 회원가입 폼처리
def signupform(request):
    # POST 방식이면, 데이터가 담긴 제출된 폼으로 간주합니다.
    if request.method == 'POST':
        # request에 담긴 데이터로, 클래스 폼을 생성합니다.
        form = SignupForm(request.POST)
        # 폼에 담긴 데이터가 유효한지 체크한다
        if form.is_valid():
            # (1)비밀번호와 비밀번호확인이 일치하는지 비교한다
            if request.POST['member_pw'] == request.POST['member_pw_r']:
                 # (2)아이디중복인지 확인하기   
                if Member.objects.filter(member_id = request.POST['member_id']):
                    form = SignupForm()
                    message="아이디중복"
                    return render(request, 'member/signup.html', {
                        'form':form,
                        'message':message,
                        'member_id':request.POST['member_id'],
                        'member_pw':request.POST['member_pw'],
                        'member_pw_r':request.POST['member_pw_r'],
                        'nickname':request.POST['nickname'],
                        'member_name':request.POST['member_name'],
                        'address':request.POST['address'],
                        'address_in':request.POST['address_in'],
                        'phone_no':request.POST['phone_no'],
                        'email':request.POST['email'],
                    })

                # (2)else문
                else:
                    # (3)아이디, 비밀번호 글자 제한 (영문자, 숫자만 가능)
                    id_check=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
                    pw_check=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a',\
                                'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1',\
                                '2','3','4','5','6','7','8','9']            
                    id_value=""
                    pw_value=""            

                    # 아이디 검사
                    for i in list(request.POST['member_id']):
                        if i in id_check:
                            id_value+=i
                        else:
                            continue

                    if(request.POST['member_id']!=id_value):
                        #영소문자,숫자가 아니니 에러메시지를 띄운다.
                        form = SignupForm()
                        message="아이디글자제한"
                        return render(request, 'member/signup.html', {
                            'form':form,
                            'message':message,
                            'member_id':request.POST['member_id'],
                            'member_pw':request.POST['member_pw'],
                            'member_pw_r':request.POST['member_pw_r'],
                            'nickname':request.POST['nickname'],
                            'member_name':request.POST['member_name'],
                            'address':request.POST['address'],
                            'address_in':request.POST['address_in'],
                            'phone_no':request.POST['phone_no'],
                            'email':request.POST['email'],
                        })

                    # 비밀번호 검사
                    for i in list(request.POST['member_pw']):
                        if i in pw_check:
                            pw_value+=i
                        else:
                            continue

                    if(request.POST['member_pw']!=pw_value):
                        #영대소문자,숫자가 아니니 에러메시지를 띄운다.
                        form = SignupForm()
                        message="비밀번호글자제한"
                        return render(request, 'member/signup.html', {
                            'form':form,
                            'message':message,
                            'member_id':request.POST['member_id'],
                            'member_pw':request.POST['member_pw'],
                            'member_pw_r':request.POST['member_pw_r'],
                            'nickname':request.POST['nickname'],
                            'member_name':request.POST['member_name'],
                            'address':request.POST['address'],
                            'address_in':request.POST['address_in'],
                            'phone_no':request.POST['phone_no'],
                            'email':request.POST['email'],
                        })

                    #(추가)닉네임중복인지 확인하기
                    if Member.objects.filter(nickname = request.POST['nickname']):
                        form = SignupForm()
                        message="닉네임중복"
                        return render(request, 'member/signup.html', {
                            'form':form,
                            'message':message,
                            'member_id':request.POST['member_id'],
                            'member_pw':request.POST['member_pw'],
                            'member_pw_r':request.POST['member_pw_r'],
                            'nickname':request.POST['nickname'],
                            'member_name':request.POST['member_name'],
                            'address':request.POST['address'],
                            'address_in':request.POST['address_in'],
                            'phone_no':request.POST['phone_no'],
                            'email':request.POST['email'],
                         })
                                
                              
                    # 모든 에러검사를 넘겨 회원가입을 완료한다.
                    obj = Member( member_id=request.POST['member_id'], member_pw=request.POST['member_pw'],
                    nickname=request.POST['nickname'], member_name=request.POST['member_name'], address=request.POST['address'],
                    address_in=request.POST['address_in'],phone_no=request.POST['phone_no'], email=request.POST['email'])
                    obj.save()
                    # 회원가입 완료시 완료화면으로 이동한다.
                    return redirect('member:signup_result', pk=obj.pk)

            #(1)else문
            # 비밀번호와 비밀번호확인 일치 실패시 '비밀번호' 문구를보낸다.
            # 현재까지 입력된 form값을 모두 다같이 담아 보낸다.
            # 받은 form값을 input.value로 넣어준다.
            else:
                form = SignupForm()
                message="비밀번호일치"
                return render(request, 'member/signup.html', {
                    'form':form,
                    'message':message,
                    'member_id':request.POST['member_id'],
                    'member_pw':request.POST['member_pw'],
                    'member_pw_r':request.POST['member_pw_r'],
                    'nickname':request.POST['nickname'],
                    'member_name':request.POST['member_name'],
                    'address':request.POST['address'],
                    'address_in':request.POST['address_in'],
                    'phone_no':request.POST['phone_no'],
                    'email':request.POST['email'],
                    })
                

    else: # GET 방식
        form = SignupForm()
        message="GET"
        return render(request, 'member/signup.html', {'form':form, 'message':message})

# 아이디찾기
def findidform(request):
    if request.method == 'POST':
        form = FindIdForm(request.POST)
        if form.is_valid():
                member_name = request.POST['member_name']
                email = request.POST['email']

                if Member.objects.filter(member_name = member_name, email = email):
                    obj = Member.objects.get(member_name = member_name)
                    return render(request, 'member/find_id_result.html', {'obj':obj})
                else:
                    message="실패"
                    return render(request, 'member/find_id.html', {'form':form, 'message':message})
    else: # GET 방식
        form = FindIdForm()
        return render(request, 'member/find_id.html', {'form':form})

# 비밀번호찾기
def findpasswdform(request):
    if request.method == 'POST':
        form = FindPasswdForm(request.POST)
        if form.is_valid():
                member_id = request.POST['member_id']
                member_name = request.POST['member_name']
                email = request.POST['email']

                if Member.objects.filter(member_id = member_id, member_name = member_name, email = email):
                    obj = Member.objects.get(member_id = member_id)
                    return redirect('member:passwdup', pk=obj.pk)
                else:
                    message="실패"
                    return render(request, 'member/find_passwd.html', {'form':form, 'message':message})
    else: # GET 방식
        form = FindPasswdForm()
        return render(request, 'member/find_passwd.html', {'form':form})

# 비밀번호 변경
def passwdupform(request,pk):
    if request.method == 'POST':
        form = PasswdUpForm(request.POST)
        if form.is_valid():
            # 비밀번호와 비밀번호확인이 일치하는지 비교한다
            if request.POST['member_pw'] == request.POST['member_pw_r']:
                # 입력받은 비밀번호 값
                member_pw = request.POST['member_pw']
                # pk에 적합한 table
                obj = Member.objects.get(pk=pk)
                obj.member_pw = member_pw
                obj.save()
                return render(request, 'member/find_passwd_result.html', {'form':form})
            else:
                return HttpResponse('비밀번호변경 실패했습니다')      
    else:
        form = PasswdUpForm()
        return render(request, 'member/passwd_update.html', {'form':form, 'obj':pk})

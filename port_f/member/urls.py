from django.urls import path
from . import views

app_name = 'member'
urlpatterns = [
    # /agreement - 이용약관
    path('agreement/', views.Agreement.as_view(), name='agreement'),

    # /privacy - 개인정보처리방침
    path('privacy/', views.Privacy.as_view(), name='privacy'),
    
    # /login - 로그인화면
    path('login/', views.loginform, name ='login'),
    
    # /logout - 로그아웃
    path('logout/', views.logout, name='logout'),

    # /signup - 회원가입화면
    path('signup/', views.signupform, name ='signup'),

    # /signup/<pk>/result - 회원가입완료화면
    path('signup/<int:pk>/result/', views.SiResultView.as_view(), name='signup_result'),

    # /find_id - 아이디찾기
    path('find_id/', views.findidform, name='find_id'),

    # /find_passwd - 비밀번호찾기
    path('find_passwd/', views.findpasswdform, name='find_passwd'),

    # /find_passwd/<pk> - 비밀번호 변경
    path('find_passwd/<int:pk>/', views.passwdupform, name='passwdup'),


]
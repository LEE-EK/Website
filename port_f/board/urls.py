from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [

    # /index - 커뮤니티 메인홈
    path('index/', views.IndexView.as_view(), name='index'),

    #######################################################################################################

    # /notice_list - 공지사항 목록
    path('notice_list/', views.notice_list, name='notice_list'),

    # /notice_detail - 공지사항 상세
    path('notice_detail/<int:pk>/', views.notice_detail, name='notice_detail'),

    # /notice_create - 공지사항 작성
    path('notice_create/', views.notice_create, name='notice_create'),

    # /notice_update - 공지사항 수정
    path('notice_update/<int:pk>', views.notice_update, name='notice_update'),

    # /notice_delete - 공지사항 삭제
    path('notice_delete/<int:pk>', views.notice_delete, name='notice_delete'),

    # /notice_search - 공지사항 검색
    path('notice_search/', views.notice_search, name='notice_search'),

    # /notice_comment_delete - 공지사항 댓글 삭제
    path('notice_list/<int:pk>/comment/<int:cpk>/delete', views.notice_comment_delete, name='notice_comment_delete'),

    #######################################################################################################

    # /from_mark_list - FROM_MARK 목록
    path('from_mark_list/', views.from_mark_list, name='from_mark_list'),

    # /from_mark_detail - FROM_MARK 상세
    path('from_mark_detail/<int:pk>/', views.from_mark_detail, name='from_mark_detail'),

    # /from_mark_create - FROM_MARK 작성
    path('from_mark_create/', views.from_mark_create, name='from_mark_create'),

    # /from_mark_update - FROM_MARK 수정
    path('from_mark_update/<int:pk>', views.from_mark_update, name='from_mark_update'),

    # /from_mark_delete - FROM_MARK 삭제
    path('from_mark_delete/<int:pk>', views.from_mark_delete, name='from_mark_delete'),

    # /from_mark_search - FROM_MARK 검색
    path('from_mark_search/', views.from_mark_search, name='from_mark_search'),

    # /from_mark_comment_delete - FROM_MARK 댓글 삭제
    path('from_mark_list/<int:pk>/comment/<int:cpk>/delete', views.from_mark_comment_delete, name='from_mark_comment_delete'),

    #######################################################################################################

    # /to_mark_list - TO_MARK 목록
    path('to_mark_list/', views.to_mark_list, name='to_mark_list'),

    # /to_mark_detail - TO_MARK 상세
    path('to_mark_detail/<int:pk>/', views.to_mark_detail, name='to_mark_detail'),

    # /to_mark_create - TO_MARK 작성
    path('to_mark_create/', views.to_mark_create, name='to_mark_create'),

    # /to_mark_update - TO_MARK 수정
    path('to_mark_update/<int:pk>', views.to_mark_update, name='to_mark_update'),

    # /to_mark_delete - TO_MARK 삭제
    path('to_mark_delete/<int:pk>', views.to_mark_delete, name='to_mark_delete'),

    # /to_mark_search - TO_MARK 검색
    path('to_mark_search/', views.to_mark_search, name='to_mark_search'),

    # /to_mark_comment_delete - TO_MARK 댓글 삭제
    path('to_mark_list/<int:pk>/comment/<int:cpk>/delete', views.to_mark_comment_delete, name='to_mark_comment_delete'),

    #######################################################################################################

    # /freetalk_list - Freetalk 목록
    path('freetalk_list/', views.freetalk_list, name='freetalk_list'),

    # /freetalk_detail - Freetalk 상세
    path('freetalk_detail/<int:pk>/', views.freetalk_detail, name='freetalk_detail'),

    # /freetalk_create - Freetalk 작성
    path('freetalk_create/', views.freetalk_create, name='freetalk_create'),

    # /freetalk_update - Freetalk 수정
    path('freetalk_update/<int:pk>', views.freetalk_update, name='freetalk_update'),

    # /freetalk_delete - Freetalk 삭제
    path('freetalk_delete/<int:pk>', views.freetalk_delete, name='freetalk_delete'),

    # /freetalk_search - Freetalk 검색
    path('freetalk_search/', views.freetalk_search, name='freetalk_search'),

    # /freetalk_comment_delete - Freetalk 댓글 삭제
    path('freetalk_list/<int:pk>/comment/<int:cpk>/delete', views.freetalk_comment_delete, name='freetalk_comment_delete'),

    #######################################################################################################

    # /auth_list - Auth 목록
    path('auth_list/', views.auth_list, name='auth_list'),

    # /auth_detail - Auth 상세
    path('auth_detail/<int:pk>/', views.auth_detail, name='auth_detail'),

    # /auth_create - Auth 작성
    path('auth_create/', views.auth_create, name='auth_create'),

    # /auth_update - Auth 수정
    path('auth_update/<int:pk>', views.auth_update, name='auth_update'),

    # /auth_delete - Auth 삭제
    path('auth_delete/<int:pk>', views.auth_delete, name='auth_delete'),

    # /auth_search - Auth 검색
    path('auth_search/', views.auth_search, name='auth_search'),

    # /auth_comment_delete - Auth 댓글 삭제
    path('auth_list/<int:pk>/comment/<int:cpk>/delete', views.auth_comment_delete, name='auth_comment_delete'),


    #######################################################################################################

    # /question_list - Question 목록
    path('question_list/', views.question_list, name='question_list'),

    # /question_detail - Question 상세
    path('question_detail/<int:pk>/', views.question_detail, name='question_detail'),

    # /question_create - Question 작성
    path('question_create/', views.question_create, name='question_create'),

    # /question_update - Question 수정
    path('question_update/<int:pk>', views.question_update, name='question_update'),

    # /question_delete - Question 삭제
    path('question_delete/<int:pk>', views.question_delete, name='question_delete'),

    # /question_search - Question 검색
    path('question_search/', views.question_search, name='question_search'),

    # /question_comment_delete - Question 댓글 삭제
    path('question_list/<int:pk>/comment/<int:cpk>/delete', views.question_comment_delete, name='question_comment_delete'),      
]
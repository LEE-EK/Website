from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    # /index - 커뮤니티 메인홈
    path('index/', views.IndexView.as_view(), name='index'),

    # /notice - 예비 공지사항
    path('notice/', views.notice, name='notice'),

    # /list - 예비 게시글 목록
    path('list/<int:pk>/', views.list, name='list'),

    # /create - 예비 게시글 작성
    path('create/', views.create, name='create'),

    # /update - 예비 게시글 수정
    path('update/<int:pk>', views.update, name='update'),

    # /dalete - 예비 게시글 삭제
    path('delete/<int:pk>', views.delete, name='delete'),

    # /search - 예비 검색 페이지
    path('search/', views.search, name='search'),

    # /comment_delete - 댓글 삭제
    path('list/<int:pk>/comment/<int:cpk>/delete', views.comment_delete, name='comment_delete'),



]
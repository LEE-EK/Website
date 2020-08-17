from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from .forms import PostForm
from .forms import CommentForm

from member.models import Member
from board.models import Post
from board.models import Comment

import math


# 커뮤니티 메인화면
class IndexView(TemplateView):
    template_name = 'board/board_index.html'

# 목록 페이지 (공지사항)
def notice(request):
    restaurants = Post.objects.all()
    pagenator = Paginator(restaurants, 10)
    page = request.GET.get('page')
    if page is None:
        page = 1

    # 시작페이지 끝페이지 구하기
    page_F = float(page)
    if page_F <= 10:
        beginPage = 1
    else:
        beginPage = (math.trunc(page_F / 10)) * 10 + 1

    if (beginPage + 10) > pagenator.num_pages:
        lastPage = pagenator.num_pages
    else:
        lastPage = beginPage + 9
    nextRangeStartPage = lastPage + 1

    pageRange = []
    for num in range(beginPage, lastPage+1):
        pageRange.append(num)

    items = pagenator.get_page(page)
    context = {
        'restaurants': items,
        'lastPage': lastPage,
        'pageRange': pageRange,
        'nextRangeStartPage': nextRangeStartPage,
    }
    return render(request, 'board/notice.html', context)


# 게시글 상세페이지
def list(request, pk):
    # 게시글 번호
    obj = Post.objects.get(pk=pk)
    # 게시글 작성자 회원정보 보내기 'create'
    create = Member.objects.get(nickname=obj.name)

    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()


    # 댓글 페이징
    restaurants = Comment.objects.filter(post=obj).order_by("created_date").reverse()
    pagenator = Paginator(restaurants, 4)
    page = request.GET.get('page')
    if page is None:
        page = 1

    # 댓글 시작페이지 끝페이지 구하기
    page_F = float(page)
    if page_F <= 10:
        beginPage = 1
    else:
        beginPage = (math.trunc(page_F / 10)) * 10 + 1

    if (beginPage + 10) > pagenator.num_pages:
        lastPage = pagenator.num_pages
    else:
        lastPage = beginPage + 9
    nextRangeStartPage = lastPage + 1

    pageRange = []
    for num in range(beginPage, lastPage+1):
        pageRange.append(num)

    items = pagenator.get_page(page)

    # 댓글 form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 댓글 등록하기 누른 후 
            # 로그인한 아이디 정보가져오기
            member_id = request.session.get('member_id')
            login = Member.objects.get(member_id=member_id)
            comment = form.save(commit=False)
            comment.author = login
            comment.post = obj
            comment.text = form.cleaned_data['text']
            comment.save()

            # 댓글 페이징
            restaurants = Comment.objects.filter(post=obj).order_by("created_date").reverse()
            pagenator = Paginator(restaurants, 4)
            page = request.GET.get('page')
            if page is None:
                page = 1

            # 댓글 시작페이지 끝페이지 구하기 <한번 더 댓글 조회>
            page_F = float(page)
            if page_F <= 10:
                beginPage = 1
            else:
                beginPage = (math.trunc(page_F / 10)) * 10 + 1

            if (beginPage + 10) > pagenator.num_pages:
                lastPage = pagenator.num_pages
            else:
                lastPage = beginPage + 9
            nextRangeStartPage = lastPage + 1

            pageRange = []
            for num in range(beginPage, lastPage+1):
                pageRange.append(num)

            items = pagenator.get_page(page)


            # 댓글을 등록했으니 내용 초기화하시오.
            message="댓글등록"

            return render(request, 'board/list.html', {
                'form':form,
                'obj':obj,
                'create':create,
                'restaurants': items,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage,
                'message': message })
    else:
        form = CommentForm()
        return render(request, 'board/list.html', {
            'form':form,
            'obj':obj,
            'create':create,
            'restaurants': items,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage, })

# 게시글 작성페이지
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = Post(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:notice')
        else:    
            message="한계초과"
            form = PostForm()
            return render(request, 'board/create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = PostForm()
            return render(request, 'board/create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = PostForm()
            return render(request, 'board/create.html', {'form':form, 'message':message})

# 게시글 수정페이지
def update(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            obj = Post.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:notice')

        else:
            obj = Post.objects.get(pk=pk)
            form = PostForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = Post.objects.get(pk=pk)
        form = PostForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# 게시글 삭제페이지
def delete(request, pk):
    obj = Post.objects.get(pk=pk)
    obj.delete()
    return redirect('board:notice')


# 게시글 검색페이지
def search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = Post.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = Post.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = Post.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/search.html', {'message':message})  

        pagenator = Paginator(restaurants, 10)
        page = request.GET.get('page')
        if page is None:
            page = 1

        # 시작페이지 끝페이지 구하기
        page_F = float(page)
        if page_F <= 10:
            beginPage = 1
        else:
            beginPage = (math.trunc(page_F / 10)) * 10 + 1

        if (beginPage + 10) > pagenator.num_pages:
            lastPage = pagenator.num_pages
        else:
            lastPage = beginPage + 9
        nextRangeStartPage = lastPage + 1

        pageRange = []
        for num in range(beginPage, lastPage+1):
            pageRange.append(num)

        items = pagenator.get_page(page)
        context = {
            'restaurants': items,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage,
            'select': select,
            'b': b,
        }
        return render(request, 'board/search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/search.html', {'message':message})

# 댓글 삭제
def comment_delete(request, pk, cpk):
    comment = Comment.objects.get(pk=cpk)

    if not comment.author.member_id == request.session.get('member_id'):
        return redirect('board:list', pk)
    else:
        comment.delete()
        return redirect('board:list', pk)


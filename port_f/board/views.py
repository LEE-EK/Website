from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from member.models import Member

from board.models import Notice,From_mark,To_mark,Freetalk,Auth,Question,Inquiry,Report
from board.models import To_mark_Comment,Freetalk_Comment,Auth_Comment,Question_Comment,Inquiry_Comment,Report_Comment

from .forms import NoticeForm,From_markForm,To_markForm,FreetalkForm,AuthForm,QuestionForm,InquiryForm,ReportForm
from .forms import To_mark_CommentForm,Freetalk_CommentForm,Auth_CommentForm,Question_CommentForm,Inquiry_CommentForm,Report_CommentForm

import math

####################################################################################################### MAIN

# 커뮤니티 메인화면
class IndexView(TemplateView):
    template_name = 'board/board_index.html'

####################################################################################################### NOTICE

# 공지사항 목록
def notice_list(request):
    restaurants = Notice.objects.all()
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
    return render(request, 'board/notice_list.html', context)


# 공지사항 상세페이지
def notice_detail(request, pk):
    # 게시글 번호
    obj = Notice.objects.get(pk=pk) 
    
    # 게시글 작성자 회원정보 보내기 'create'
    # 회원이 존재하지 않을시 삭제하기
    try:
        create = Member.objects.get(nickname=obj.name)
    except:
        obj.delete()
        return redirect('board:notice_list')

    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()

    return render(request, 'board/notice_detail.html', {
        'obj':obj,
        'create':create
    })

# 공지사항 작성페이지
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = Notice(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:notice_list')
        else:    
            message="한계초과"
            form = NoticeForm()
            return render(request, 'board/notice_create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = NoticeForm()
            return render(request, 'board/notice_create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = NoticeForm()
            return render(request, 'board/notice_create.html', {'form':form, 'message':message})

# 공지사항 수정페이지
def notice_update(request, pk):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            obj = Notice.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:notice_list')

        else:
            obj = Notice.objects.get(pk=pk)
            form = NoticeForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/notice_update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = Notice.objects.get(pk=pk)
        form = NoticeForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/notice_update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# 공지사항 삭제페이지
def notice_delete(request, pk):
    obj = Notice.objects.get(pk=pk)
    obj.delete()
    return redirect('board:notice_list')


# 공지사항 검색페이지
def notice_search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = Notice.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = Notice.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = Notice.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/notice_search.html', {'message':message})  

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
        return render(request, 'board/notice_search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/notice_search.html', {'message':message})

# 스케쥴 페이지
class ScheduleView(TemplateView):
    template_name = 'board/schedule.html'  

####################################################################################################### ARTIST

# 프로필 페이지
class ProfileView(TemplateView):
    template_name = 'board/profile.html'

# 앨범 페이지
class AlbumView(TemplateView):
    template_name = 'board/album.html' 

# FROM_MARK 목록
def from_mark_list(request):
    restaurants = From_mark.objects.all()
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
    return render(request, 'board/from_mark_list.html', context)


# FROM_MARK 상세페이지
def from_mark_detail(request, pk):
    # 게시글 번호
    obj = From_mark.objects.get(pk=pk) 
    # 게시글 작성자 회원정보 보내기 'create'
    # 회원이 존재하지 않을시 삭제하기
    try:
        create = Member.objects.get(nickname=obj.name)
    except:
        obj.delete()
        return redirect('board:from_mark_list')

    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()
    
    
    return render(request, 'board/from_mark_detail.html', {
        'obj':obj,
        'create':create
    })

# FROM_MARK 작성페이지
def from_mark_create(request):
    if request.method == 'POST':
        form = From_markForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = From_mark(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:from_mark_list')
        else:    
            message="한계초과"
            form = From_markForm()
            return render(request, 'board/from_mark_create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = From_markForm()
            return render(request, 'board/from_mark_create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = From_markForm()
            return render(request, 'board/from_mark_create.html', {'form':form, 'message':message})

# FROM_MARK 수정페이지
def from_mark_update(request, pk):
    if request.method == 'POST':
        form = From_markForm(request.POST)
        if form.is_valid():
            obj = From_mark.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:from_mark_list')

        else:
            obj = From_mark.objects.get(pk=pk)
            form = From_markForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/from_mark_update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = From_mark.objects.get(pk=pk)
        form = From_markForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/from_mark_update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# FROM_MARK 삭제페이지
def from_mark_delete(request, pk):
    obj = From_mark.objects.get(pk=pk)
    obj.delete()
    return redirect('board:from_mark_list')


# FROM_MARK 검색페이지
def from_mark_search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = From_mark.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = From_mark.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = From_mark.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/from_mark_search.html', {'message':message})  

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
        return render(request, 'board/from_mark_search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/from_mark_search.html', {'message':message})

# FROM_MARK 댓글 삭제
def from_mark_comment_delete(request, pk, cpk):
    comment = From_mark_Comment.objects.get(pk=cpk)

    if not comment.author.member_id == request.session.get('member_id'):
        return redirect('board:from_mark_detail', pk)
    else:
        comment.delete()
        return redirect('board:from_mark_detail', pk)


# TO_MARK 목록
def to_mark_list(request):
    restaurants = To_mark.objects.all()
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
    return render(request, 'board/to_mark_list.html', context)


# TO_MARK 상세페이지
def to_mark_detail(request, pk):
    # 게시글 번호
    obj = To_mark.objects.get(pk=pk) 
    # 게시글 작성자 회원정보 보내기 'create'
    # 회원이 존재하지 않을시 삭제하기
    try:
        create = Member.objects.get(nickname=obj.name)
    except:
        obj.delete()
        return redirect('board:to_mark_list')

    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()
    
    
    # 댓글 페이징
    restaurants = To_mark_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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
        form = To_mark_CommentForm(request.POST)
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

            # 댓글 페이징 (중복이지만 필요한것)
            restaurants = To_mark_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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

            # 댓글을 등록했으니 내용 초기화하시오.
            message="댓글등록"

            return render(request, 'board/to_mark_detail.html', {
                'form':form,
                'obj':obj,
                'create':create,
                'restaurants': items,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage,
                'message': message })
    else:
        form = To_mark_CommentForm()   
        return render(request, 'board/to_mark_detail.html', {
            'form':form,
            'obj':obj,
            'create':create,
            'restaurants': items,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage,
             })

# TO_MARK 작성페이지
def to_mark_create(request):
    if request.method == 'POST':
        form = To_markForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = To_mark(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:to_mark_list')
        else:    
            message="한계초과"
            form = To_markForm()
            return render(request, 'board/to_mark_create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = To_markForm()
            return render(request, 'board/to_mark_create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = To_markForm()
            return render(request, 'board/to_mark_create.html', {'form':form, 'message':message})

# TO_MARK 수정페이지
def to_mark_update(request, pk):
    if request.method == 'POST':
        form = To_markForm(request.POST)
        if form.is_valid():
            obj = To_mark.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:to_mark_list')

        else:
            obj = To_mark.objects.get(pk=pk)
            form = To_markForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/to_mark_update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = To_mark.objects.get(pk=pk)
        form = To_markForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/to_mark_update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# TO_MARK 삭제페이지
def to_mark_delete(request, pk):
    obj = To_mark.objects.get(pk=pk)
    obj.delete()
    return redirect('board:to_mark_list')


# TO_MARK 검색페이지
def to_mark_search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = To_mark.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = To_mark.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = To_mark.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/to_mark_search.html', {'message':message})  

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
        return render(request, 'board/to_mark_search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/to_mark_search.html', {'message':message})

# TO_MARK 댓글 삭제
def to_mark_comment_delete(request, pk, cpk):
    comment = To_mark_Comment.objects.get(pk=cpk)

    if not comment.author.member_id == request.session.get('member_id'):
        return redirect('board:to_mark_detail', pk)
    else:
        comment.delete()
        return redirect('board:to_mark_detail', pk)



####################################################################################################### BOARD

# Freetalk 목록
def freetalk_list(request):
    restaurants = Freetalk.objects.all()
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
    return render(request, 'board/freetalk_list.html', context)


# Freetalk 상세페이지
def freetalk_detail(request, pk):
    # 게시글 번호
    obj = Freetalk.objects.get(pk=pk) 
    # 게시글 작성자 회원정보 보내기 'create'
    # 회원이 존재하지 않을시 삭제하기
    try:
        create = Member.objects.get(nickname=obj.name)
    except:
        obj.delete()
        return redirect('board:freetalk_list')

    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()
    
    
    # 댓글 페이징
    restaurants = Freetalk_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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
        form = Freetalk_CommentForm(request.POST)
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

            # 댓글 페이징 (중복이지만 필요한것)
            restaurants = Freetalk_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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

            # 댓글을 등록했으니 내용 초기화하시오.
            message="댓글등록"

            return render(request, 'board/freetalk_detail.html', {
                'form':form,
                'obj':obj,
                'create':create,
                'restaurants': items,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage,
                'message': message })
    else:
        form = Freetalk_CommentForm()   
        return render(request, 'board/freetalk_detail.html', {
            'form':form,
            'obj':obj,
            'create':create,
            'restaurants': items,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage,
             })

# Freetalk 작성페이지
def freetalk_create(request):
    if request.method == 'POST':
        form = FreetalkForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = Freetalk(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:freetalk_list')
        else:    
            message="한계초과"
            form = FreetalkForm()
            return render(request, 'board/freetalk_create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = FreetalkForm()
            return render(request, 'board/freetalk_create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = FreetalkForm()
            return render(request, 'board/freetalk_create.html', {'form':form, 'message':message})

# Freetalk 수정페이지
def freetalk_update(request, pk):
    if request.method == 'POST':
        form = FreetalkForm(request.POST)
        if form.is_valid():
            obj = Freetalk.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:freetalk_list')

        else:
            obj = Freetalk.objects.get(pk=pk)
            form = FreetalkForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/freetalk_update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = Freetalk.objects.get(pk=pk)
        form = FreetalkForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/freetalk_update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# Freetalk 삭제페이지
def freetalk_delete(request, pk):
    obj = Freetalk.objects.get(pk=pk)
    obj.delete()
    return redirect('board:freetalk_list')


# Freetalk 검색페이지
def freetalk_search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = Freetalk.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = Freetalk.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = Freetalk.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/freetalk_search.html', {'message':message})  

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
        return render(request, 'board/freetalk_search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/freetalk_search.html', {'message':message})

# Freetalk댓글 삭제
def freetalk_comment_delete(request, pk, cpk):
    comment = Freetalk_Comment.objects.get(pk=cpk)

    if not comment.author.member_id == request.session.get('member_id'):
        return redirect('board:freetalk_detail', pk)
    else:
        comment.delete()
        return redirect('board:freetalk_detail', pk)


# AUTH 목록
def auth_list(request):
    restaurants = Auth.objects.all()
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
    return render(request, 'board/auth_list.html', context)


# AUTH 상세페이지
def auth_detail(request, pk):
    # 게시글 번호
    obj = Auth.objects.get(pk=pk) 
    # 게시글 작성자 회원정보 보내기 'create'
    # 회원이 존재하지 않을시 삭제하기
    try:
        create = Member.objects.get(nickname=obj.name)
    except:
        obj.delete()
        return redirect('board:auth_list')

    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()
    
    
    # 댓글 페이징
    restaurants = Auth_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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
        form = Auth_CommentForm(request.POST)
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

            # 댓글 페이징 (중복이지만 필요한것)
            restaurants = Auth_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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

            # 댓글을 등록했으니 내용 초기화하시오.
            message="댓글등록"

            return render(request, 'board/auth_detail.html', {
                'form':form,
                'obj':obj,
                'create':create,
                'restaurants': items,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage,
                'message': message })
    else:
        form = Auth_CommentForm()   
        return render(request, 'board/auth_detail.html', {
            'form':form,
            'obj':obj,
            'create':create,
            'restaurants': items,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage,
             })

# AUTH 작성페이지
def auth_create(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = Auth(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:auth_list')
        else:    
            message="한계초과"
            form = AuthForm()
            return render(request, 'board/auth_create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = AuthForm()
            return render(request, 'board/auth_create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = AuthForm()
            return render(request, 'board/auth_create.html', {'form':form, 'message':message})

# AUTH 수정페이지
def auth_update(request, pk):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            obj = Auth.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:auth_list')

        else:
            obj = Auth.objects.get(pk=pk)
            form = AuthForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/auth_update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = Auth.objects.get(pk=pk)
        form = AuthForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/auth_update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# AUTH 삭제페이지
def auth_delete(request, pk):
    obj = Auth.objects.get(pk=pk)
    obj.delete()
    return redirect('board:auth_list')


# AUTH 검색페이지
def auth_search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = Auth.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = Auth.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = Auth.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/auth_search.html', {'message':message})  

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
        return render(request, 'board/auth_search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/auth_search.html', {'message':message})

# AUTH댓글 삭제
def auth_comment_delete(request, pk, cpk):
    comment = Auth_Comment.objects.get(pk=cpk)

    if not comment.author.member_id == request.session.get('member_id'):
        return redirect('board:auth_detail', pk)
    else:
        comment.delete()
        return redirect('board:auth_detail', pk)


# QUESTION 목록
def question_list(request):
    restaurants = Question.objects.all()
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
    return render(request, 'board/question_list.html', context)


# QUESTION 상세페이지
def question_detail(request, pk):
    # 게시글 번호
    obj = Question.objects.get(pk=pk) 
    # 게시글 작성자 회원정보 보내기 'create'
    # 회원이 존재하지 않을시 삭제하기
    try:
        create = Member.objects.get(nickname=obj.name)
    except:
        obj.delete()
        return redirect('board:question_list')
    # 방문할때 마다 게시글 조회수 증가
    obj.hits=obj.hits+1
    obj.save()
    
    
    # 댓글 페이징
    restaurants = Question_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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
        form = Question_CommentForm(request.POST)
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

            # 댓글 페이징 (중복이지만 필요한것)
            restaurants = Question_Comment.objects.filter(post=obj).order_by("created_date").reverse()
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

            # 댓글을 등록했으니 내용 초기화하시오.
            message="댓글등록"

            return render(request, 'board/question_detail.html', {
                'form':form,
                'obj':obj,
                'create':create,
                'restaurants': items,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage,
                'message': message })
    else:
        form = Question_CommentForm()   
        return render(request, 'board/question_detail.html', {
            'form':form,
            'obj':obj,
            'create':create,
            'restaurants': items,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage,
             })

# QUESTION 작성페이지
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 로그인한경우
            member_id = request.session.get('member_id')
            obj = Member.objects.get(member_id=member_id)
            name = obj.nickname

            # Board Model에 제목, 작성자, 내용을 등록시킨다.
            obj = Question(subject=request.POST['subject'], name=name, memo=request.POST['memo'])
            obj.save()
            return redirect('board:question_list')
        else:    
            message="한계초과"
            form = QuestionForm()
            return render(request, 'board/question_create.html', {'form':form, 'message':message})
    else:
        if request.session.get('member_id'):
            form = QuestionForm()
            return render(request, 'board/question_create.html', {'form':form})
        # 로그인안한경우    
        else:
            message="비로그인"
            form = QuestionForm()
            return render(request, 'board/question_create.html', {'form':form, 'message':message})

# QUESTION 수정페이지
def question_update(request, pk):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            obj = Question.objects.get(pk=pk)
            obj.subject = request.POST['subject']
            obj.memo = request.POST['memo']
            obj.save()
            return redirect('board:question_list')

        else:
            obj = Question.objects.get(pk=pk)
            form = QuestionForm(instance = obj)    
            message="한계초과"
            return render(request, 'board/question_update.html', {'form':form, 'obj':obj, 'message':message})
    else:
        obj = Question.objects.get(pk=pk)
        form = QuestionForm(instance = obj)
        create = Member.objects.get(nickname=obj.name)
        return render(request, 'board/question_update.html', {
            'obj':obj,
            'form':form,
            'subject':obj.subject,
            'memo':obj.memo,
            'create':create,
        })


# QUESTION 삭제페이지
def question_delete(request, pk):
    obj = Question.objects.get(pk=pk)
    obj.delete()
    return redirect('board:question_list')


# QUESTION 검색페이지
def question_search(request):
    # b는 넘겨 받은 검색어
    b = request.GET.get('b','')
    # select는 넘겨 받은 카테고리
    select = request.GET.get('findType','')

    # 입력된 검색어가 있을 경우
    if b:
        # 카테고리 값에따라 조회결과 출력
        if select=="title":
            restaurants = Question.objects.filter(subject__contains=b)
            
        elif select=="name":
            restaurants = Question.objects.filter(name__contains=b)
            
        elif select=="content":
            restaurants = Question.objects.filter(memo__contains=b) 
        else:
            message = "새로고침"
            return render(request, 'board/question_search.html', {'message':message})  

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
        return render(request, 'board/question_search.html', context)
        # 카테고리 값이 없을 경우 <새로고침>       
               
    # 입력된 검색어가 없을 경우 <새로고침>       
    else:
        message = "새로고침"
        return render(request, 'board/question_search.html', {'message':message})

# QUESTION댓글 삭제
def question_comment_delete(request, pk, cpk):
    comment = Question_Comment.objects.get(pk=cpk)

    if not comment.author.member_id == request.session.get('member_id'):
        return redirect('board:question_detail', pk)
    else:
        comment.delete()
        return redirect('board:question_detail', pk)                                            



####################################################################################################### Q&A

# 문의하기
def inquiry(request):
    # 페이징
    restaurants = Inquiry.objects.all().order_by("created_date").reverse() #문의글
    restaurants_co = Inquiry_Comment.objects.all().order_by("created_date").reverse() #문의댓글글
    pagenator = Paginator(restaurants, 4)
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


    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # 문의 등록하기 누른 후 
            # 로그인한 아이디 정보가져오기
            member_id = request.session.get('member_id')
            login = Member.objects.get(member_id=member_id)
            inquiry = form.save(commit=False)
            inquiry.author = login
            inquiry.text = form.cleaned_data['text']
            inquiry.save()

            # 페이징 (중복이지만 필요한것)
            restaurants = Inquiry.objects.all().order_by("created_date").reverse()
            pagenator = Paginator(restaurants, 4)
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

            # 문의를 등록했으니 내용 초기화하시오.
            message="문의등록"

            return render(request, 'board/inquiry.html', {
                'form':form,
                'message':message,
                'restaurants': items,
                'restaurants_co':restaurants_co,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage
                })
    else:
        form = InquiryForm()
        return render(request, 'board/inquiry.html', {
            'form':form,
            'restaurants': items,
            'restaurants_co':restaurants_co,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage
            })


# 문의하기 삭제
def inquiry_delete(request, pk):
    inquiry = Inquiry.objects.get(pk=pk)

    if not inquiry.author.member_id == request.session.get('member_id'):
        return redirect('board:inquiry')
    else:
        inquiry.delete()
        return redirect('board:inquiry')   


# 문의하기 댓글
def inquiry_comment(request, pk):
    obj = Inquiry.objects.get(pk=pk) 
    if request.method == 'POST':
        form = Inquiry_CommentForm(request.POST)

        if form.is_valid():
            # 문의 댓글등록하기 누른 후 
            # 로그인한 아이디 정보가져오기
            member_id = request.session.get('member_id')
            login = Member.objects.get(member_id=member_id)
            inquiry_comment = form.save(commit=False)
            inquiry_comment.author = login
            inquiry_comment.post = obj
            inquiry_comment.text = form.cleaned_data['text']
            inquiry_comment.save()
            return redirect('board:inquiry')
    else:
        return redirect('board:inquiry') 


# 문의댓글 삭제
def inquiry_comment_delete(request, pk):
    inquiry_comment = Inquiry_Comment.objects.get(pk=pk)

    if not inquiry_comment.author.member_id == request.session.get('member_id'):
        return redirect('board:inquiry')
    else:
        inquiry_comment.delete()
        return redirect('board:inquiry')   


# 신고하기
def report(request):
    # 페이징
    restaurants = Report.objects.all().order_by("created_date").reverse() #문의글
    restaurants_co = Report_Comment.objects.all().order_by("created_date").reverse() #문의댓글글
    pagenator = Paginator(restaurants, 4)
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


    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # 신고 등록하기 누른 후 
            # 로그인한 아이디 정보가져오기
            member_id = request.session.get('member_id')
            login = Member.objects.get(member_id=member_id)
            report = form.save(commit=False)
            report.author = login
            report.text = form.cleaned_data['text']
            report.save()

            # 페이징 (중복이지만 필요한것)
            restaurants = Report.objects.all().order_by("created_date").reverse()
            pagenator = Paginator(restaurants, 4)
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

            # 신고를 등록했으니 내용 초기화하시오.
            message="신고등록"

            return render(request, 'board/report.html', {
                'form':form,
                'message':message,
                'restaurants': items,
                'restaurants_co':restaurants_co,
                'lastPage': lastPage,
                'pageRange': pageRange,
                'nextRangeStartPage': nextRangeStartPage
                })
    else:
        form = ReportForm()
        return render(request, 'board/report.html', {
            'form':form,
            'restaurants': items,
            'restaurants_co':restaurants_co,
            'lastPage': lastPage,
            'pageRange': pageRange,
            'nextRangeStartPage': nextRangeStartPage
            })


# 신고하기 삭제
def report_delete(request, pk):
    report = Report.objects.get(pk=pk)

    if not report.author.member_id == request.session.get('member_id'):
        return redirect('board:report')
    else:
        report.delete()
        return redirect('board:report')   


# 신고하기 댓글
def report_comment(request, pk):
    obj = Report.objects.get(pk=pk) 
    if request.method == 'POST':
        form = Report_CommentForm(request.POST)

        if form.is_valid():
            # 신고 댓글등록하기 누른 후 
            # 로그인한 아이디 정보가져오기
            member_id = request.session.get('member_id')
            login = Member.objects.get(member_id=member_id)
            report_comment = form.save(commit=False)
            report_comment.author = login
            report_comment.post = obj
            report_comment.text = form.cleaned_data['text']
            report_comment.save()
            return redirect('board:report')
    else:
        return redirect('board:report') 


# 신고댓글 삭제
def report_comment_delete(request, pk):
    report_comment = Report_Comment.objects.get(pk=pk)

    if not report_comment.author.member_id == request.session.get('member_id'):
        return redirect('board:report')
    else:
        report_comment.delete()
        return redirect('board:report')           
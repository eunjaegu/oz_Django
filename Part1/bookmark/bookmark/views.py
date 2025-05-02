from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from bookmark.models import Bookmark

# DB에서 전체 조회
def bookmark_list(request):
    # SELECT * FROM bookmark
    bookmarks = Bookmark.objects.all()

    # 50개 이상 출력 Gt 초과, Gte 이상
    # bookmarks = Bookmark.objects.filter(id__gte=50)

    context = {
        'bookmarks': bookmarks
    }

    #return HttpResponse('<h1>북마크 리스트 페이지입니다.</h>')
    return render(request, 'bookmark_list.html', context)

#DB에서 pk(id)로 조회
def bookmark_detail(request, pk):
    #1번 방법
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404

    #2번 방법
    bookmark = get_object_or_404(Bookmark, pk=pk)

    context = {'bookmark':bookmark}
    #return HttpResponse('<h1>북마크 디테일 페이지입니다.</h>')
    return render(request, 'bookmark_detail.html', context)

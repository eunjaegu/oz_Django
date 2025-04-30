"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render
from django.shortcuts import redirect

movie_list = [
    {'title': '파묘', 'Director': '장재현'},
    {'title': '윙카', 'Director': '폴 킴'},
    {'title': '듄: 파트2', 'Director': '드니 빌뇌브'},
    {'title': '시민덕희', 'Director': '박영주'}
]

def index(request):
    return HttpResponse('<h1>hello2</h1>')

def book_list(request):
    book_text = ''

    # for i in range(0, 10):
    #     book_text += f'book {i}<br>'
    # return HttpResponse(book_text)
    return render(request, 'book_list.html', {'range':range(1, 10)})
def book(request, num):
    # book_text = f'book {num}번 페이지입니다.'
    # return HttpResponse(book_text)
    return render(request, 'book_detail.html', {'num': num})

def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다.')

def python(request):
    return HttpResponse('python 페이지 입니다.')

def movies(request):
    # movie_titles = [movie['title'] for movie in movie_list]
    # 리스트 내포 방식
    # movie_titles = [
    #     f'<a href="/movie/{index}/">{movie["title"]}</a><br>'
    #     for index, movie in enumerate(movie_list)
    # ]
    #
    # # movie_titles = []
    # # 일반for문방식
    # # for movie in movie_list:
    # #     movie_titles.append(movie['title'])
    #
    # response_text = '<br>'.join(movie_titles)
    # # response_text = ''
    # # for index, title in enumerate(movie_titles):
    # #     response_text += f'<a href="/movie/{index}/">{title}</a><br>'
    # return HttpResponse(response_text)
    return render(request, 'movies.html', {'movie_list': movie_list})

# 리스트니까 인덱스를 받으면 좋겠죠
def movie_detail(request, index):
    if index > len(movie_list) -1:
        from django.http import Http404
        raise Http404

    movie = movie_list[index]
    # 템플릿이 없을 경우 아래 코드 사용
    #response_text = f"<h1>{movie['title']}</h1> <p>감독: {movie['Director']}</p>"
    #return HttpResponse(response_text)
    # 템플릿이 있을경우 아래코드 사용
    from django.shortcuts import render
    context = {'movie_list': movie_list, 'index': index}
    return render(request, 'movie.html', context)

def gugudan(request, num):
    if num < 2:
        return redirect('/gugudan/2/')

    context = {
        'num': num,
        'results': [num * i for i in range(1, 10)]
        #'results': [(i, num * i) for i in range(1, 10)]
        # 'range': range(1, 10)
    }

    return render(request, 'gugudan.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/python/', python),
    path('language/<str:lang>/', language),
    path('movie/', movies),
    path('movie/<int:index>/', movie_detail),
    path('gugudan/<int:num>/', gugudan),



]

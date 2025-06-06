"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlp atterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from blog import views
from member import views as member_views
from blog import cb_views

# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# class TestView(TemplateView):
#     def get(self, request):
#         return render(request, 'test_get.html')
#
#     def post(self, request):
#         return render(request, 'test_post.html')
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),

    #auth
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),


    # test
    #path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    #path('about/', AboutView.as_view(), name='about'),
    #path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    #path('test/', TestView.as_view(), name='test),
    #path('redirect2/', lambda req: redirect(reverse('about'))), # 익명함수 lambda

    #summernote
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

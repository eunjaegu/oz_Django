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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # CBV 연결
    path('', include('todo.urls')),

    # FBV 연결
    path('fb/', include('todo.fbv_urls')),

    # 인증 시스템
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', users_views.login, name='users_login'),
    path('accounts/signup/', users_views.sign_up, name='users_signup'),

    #summernote
    path('summernote/', include('django_summernote.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

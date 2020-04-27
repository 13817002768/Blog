"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('app1.urls')),
    path('', views.index,name='index'),
    path('login/',views.login, name='login'),
    path('register/', views.register, name='register'),
    path('base/', views.base, name='base'),
    path('message/', views.message, name='message'),
    path('home/', views.home, name='home'),
    path('find_by_category/<category>', views.find_by_category, name='find_by_category'),
    path('blog_detail/<blog_id>', views.blog_detail, name='blog_detail'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('my_blog/<username>', views.my_blog, name='my_blog'),
    path('del_blog/<blog_id>', views.del_blog, name='del_blog'),
    path('add_blog/', views.add_blog, name = 'add_blog'),
    path('update_blog/<blog_id>', views.update_blog, name='update_blog'),
    path('update_password/', views.update_password, name='update_password'),
    path('find_by_title/<title>', views.find_by_title, name='find_by_title'),
]

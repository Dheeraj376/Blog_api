"""
URL configuration for blog_api project.

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

from django.urls import path
from api_manage.views import * 

urlpatterns = [

   
    path('user_auth/' , user_auth , name='user_auth'),
    path('create/', create_blog , name='create' ),
    path('register/' , register , name='register'),
    path('manage/' , manage , name="manage"),
    path('update/', update_blog, name='update_blog'),
    path('delete/', delete_blog, name='delete_blog'),
    path('filter/', filter , name="filter"),
    path('logout/', logout_view, name='logout'),
    path('home/' , home_page , name='home_page')

]

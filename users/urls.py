
from django.contrib import admin
from django.urls import path

from .views import (
    index_view, get_tokens, 
    remote_login, logout_user
    )


urlpatterns = [
    path('', index_view, name='index'),
    path('get_tokens/', get_tokens, name='get_tokens'),
    path('remote_login/', remote_login, name='remote_login'),
    path('get_tokens', get_tokens, name='get_tokens'),
    
    path('logout/', logout_user, name='logout_user')
]

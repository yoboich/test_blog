import os
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


from .services import (
    get_auth_token, get_remote_user_data,
    get_or_create_user, get_access_token,
    get_or_create_token, revoke_token,
)

from dotenv import load_dotenv
load_dotenv()



def index_view(request):
    return render(request, 'index.html')


def get_tokens(request):
    
    access_token = get_access_token(request)

    user_data = get_remote_user_data(access_token) 
    user = get_or_create_user(user_data)
    token = get_or_create_token(access_token, user)
    login(request, user)
    
    return redirect(reverse_lazy('users:index'))
    
    
def remote_login(request):

    response_type = 'code'

    code_challenge = os.getenv('code_challenge')

    code_challenge_method = 'S256'

    client_id = os.getenv('client_id')

    redirect_uri = 'http://127.0.0.1:8001/get_tokens'
    
    url = f'http://127.0.0.1:8000/o/authorize/?response_type={response_type}&code_challenge={code_challenge}&code_challenge_method={code_challenge_method}&client_id={client_id}&redirect_uri={redirect_uri}'

    return HttpResponseRedirect(url)


def logout_user(request):
    # logout(request)
    revoke_token(request)
    return redirect(reverse_lazy('users:index'))
    

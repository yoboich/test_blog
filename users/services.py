import os
import requests
from django.http import HttpResponseRedirect

from .models import CustomUser as User, AccessToken

def get_auth_token(access_token):
    url = 'http://127.0.0.1:8000/get_auth_token/'
    data = {
        'access_token': access_token
    }
    r = requests.post(url, data=data)

    return r.json()


def get_remote_user_data(access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    url = 'http://127.0.0.1:8000/get_user_data/'
    
    r = requests.get(url, headers=headers)

    user_data = r.json()
    return user_data


def get_or_create_user(user_data):
    user = User.objects.get_or_create(
        email=user_data['email']
    )[0]
    
    return user
    
    
def get_access_token(request):
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    code = request.GET.get('code')
    code_verifier = os.getenv('code_verifier')
    
    # URI used when code was saved.
    redirect_uri = 'http://127.0.0.1:8001/get_tokens'
        
    url = "http://127.0.0.1:8000/o/token/"
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    
    r = requests.post(url, headers=headers, data=data)
    
    return r.json()['access_token']


def get_or_create_token(access_token, user):
    token = AccessToken.objects.get_or_create(
        token=access_token,
        user=user
    )
    
    return token

def revoke_token(request):
    token = AccessToken.objects.filter(
        user=request.user
    )[0].token
    
    url = 'http://127.0.0.1:8000/o/revoke-token/'
    headers = {
        'Authorization': token
    }
    
    r = requests.get(url, headers=headers)
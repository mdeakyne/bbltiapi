import justpy as jp
from os import getenv as ge
from dotenv import load_dotenv
import requests

load_dotenv()
session_data={}
app = jp.app

@jp.SetRoute('/hello')
async def hello(request):
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    wp.add(jp.P(text=f"APP ID is {ge('appid')}"))
    return wp

@jp.SetRoute('/launch')
async def launch(request):
    wp = jp.WebPage()
    if len(request.query_params) > 0:
        for key, value in request.query_params.items():
            jp.P(text=f'{key}: {value}', a=wp, classes='text-xl m-2 p-1')

    login_hint = request.query_params['login_hint']
    lti_message_hint = request.query_params['lti_message_hint']
    target_link_uri = request.query_params['target_link_uri']
    
    url = requests.get(
        ge('auth_endpoint'), 
        params={'login_hint':login_hint, 
                'lti_message_hint':lti_message_hint,
                'client_id':ge('appid'),
                'nonce':"fc5fdc6d-5dd6-47f4-b2c9-5d1216e9b771",
                'redirect_uri':target_link_uri+'api/launch',
                'response_type':'id_token',
                'scope':'openid',
                'state':'a unique value '}).url
    
    wp.add(jp.P(text=f"URL is {url}"))
    return wp
   

@jp.SetRoute('/')
async def main(request):
    print(request)
    wp = jp.WebPage()
    wp.add(jp.P(text='This is the main page'))
    return wp

jp.justpy(start_server=False)
    

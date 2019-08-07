import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urlparse
from urllib.parse import urlencode

CLIENT_ID = 'df46fbf1-cbda-42a9-b7c9-2193b450b168'
CLIENT_SECRET = 'K0nA4lW3bH5qI7cO0tW7gW3bC2fP7rF1wC1pP4bK4kF2mO1aQ4'
REDIRECT_URI = 'https://localhost:443'
# CLIENT_ID = '08301c59-870b-4c52-a802-e0643977eba2'
# CLIENT_SECRET = 'L5vM3sR0rQ8qC8nN2iM8oY6gP6gT7nW4wK3gK4sP4cO2sC6hK4'
# REDIRECT_URI = 'https://localhost'

def get_access_token():
    auth_url = "https://sso.digikey.com/as/authorization.oauth2"        #fromation url to request authorization code
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI
    }
    auth_url = auth_url + '?' + urlencode(params)

    driver = webdriver.Firefox()                                        #authorization using Firefox
    driver.get(auth_url)
    WebDriverWait(driver, 6000).until(EC.url_contains(r'https://localhost'))
    code_url = driver.current_url
    driver.close()
    code = urlparse(code_url).query[5:]

    api_url = "https://sso.digikey.com/as/token.oauth2"                 #access token request
    params = {
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    res = requests.post(api_url, params=params, data=data)
    try:                                                                #error checking
        access_token = res.json()['access_token']
        refresh_token = res.json()['refresh_token']
        return {'access_token': access_token, 'refresh_token' : refresh_token}
    except KeyError:
        error = res.json()
        return error

def refresh_access_token(refresh_token):
    api_url = "https://sso.digikey.com/as/token.oauth2"  # access token request
    params = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    res = requests.post(api_url, params=params, data=data)
    try:                                                                #error checking
        access_token = res.json()['access_token']
        refresh_token = res.json()['refresh_token']
        return {'access_token': access_token, 'refresh_token' : refresh_token}
    except KeyError:
        error = res.json()
        return error

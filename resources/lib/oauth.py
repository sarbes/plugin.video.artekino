# -*- coding: utf-8 -*-

import json
import base64
import urllib
import requests

baseOAuth = 'http://www.artekinofestival.com/oauth/v2'
client_id = '2_m0y683G7FiLUrOsRfYOX4U7EKS3LEYNQSytOfm2Q5AuNSvdsgz'
client_secret = '2XSnNvc6QpIiFlQZVb3qJeLAjcdE5HRTj2dxF9iB155Ck09D'

def getPlaylist(username,password,id):
  jar = requests.cookies.RequestsCookieJar()
  header = {'Accept-Encoding':'gzip, deflate',
  'User-Agent':'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 7 Build/NMF26V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.105 Safari/537.36',
  'Content-Type':'application/x-www-form-urlencoded',
  'Referer':'https://www.artekinofestival.com/login',
  'Origin':'https://www.artekinofestival.com',
  'Pragma':'no-cache',
  'Cache-Control':'no-cache',
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'X-Requested-With':'fr.artefrance.artekino'}

  url = f'{baseOAuth}/auth?client_id={client_id}&client_secret={client_secret}&grant_type=clients_credentials&response_type=code&redirect_uri=artekino://api/foobar&locale=de_DE'
  response = requests.get(url, cookies=jar,headers=header)
  jar = response.cookies
  
  response = requests.get('https://www.artekinofestival.com/login', cookies=jar)
  jar = response.cookies
  
  post = {'_username':username,'_password':password,'_remember_me':'1'}
  response = requests.post('https://www.artekinofestival.com/check',headers=header,data=post,allow_redirects=False, cookies=jar)
  jar = response.cookies
  
  response = requests.get('https://www.artekinofestival.com/media/'+id+'.json',headers=header,allow_redirects=False, cookies=jar).text
  return response

def getToken(redirect_uri,username,password):
  usernamepassword = f'{username}:{password}'
  up = usernamepassword.encode('ascii')
  auth = 'Basic '+str(base64.b64encode(up))
  header = {'Authorization':auth,'Content-Type':'application/x-www-form-urlencoded','User-Agent':'okhttp/3.10.0','Host':'www.artekinofestival.com'}
  j = requests.get(f'{baseOAuth}/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&locale=en').json()
  return j['access_token']

def getRefresh(redirect_uri,token):
  header = {'User-Agent':'okhttp/3.10.0'}
  j = requests.get(f'{baseOAuth}/token?grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={token}&redirect_uri={redirect_uri}&locale=en',header).json()
  return j['access_token']

def getAuthorization(redirect_uri,code,username,password):
  usernamepassword = username+':'+password
  auth = 'Basic '+base64.b64encode(usernamepassword.encode('ISO_8859_1'))
  auth = 'Basic 0g=='
  header = {'Authorization':auth,'Content-Type':'application/x-www-form-urlencoded','User-Agent':'okhttp/3.10.0','Host':'www.artekinofestival.com'}
  j = requests.get(f'{baseOAuth}/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}&locale=en',header).json()
  return j['access_token']
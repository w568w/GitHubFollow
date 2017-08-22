#-*- coding:utf-8 -*-  
import sys
import requests
import json
import traceback
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
reload(sys)
NAME="w568w"
PASSWORD="xxxxxx"

GITNAME="w568w"
GITPASSWORD="xxxxxx"
AUTH = HTTPBasicAuth(GITNAME, GITPASSWORD)
sys.setdefaultencoding('utf-8')
def loginGitStar():
	global NAME
	global PASSWORD
	r=requests.post("http://gitstar.top:88/api/user/login",params={'username':NAME,'password':PASSWORD})
	return r.headers['Set-Cookie']
def getGitFollowList():
	global NAME
	cookie=loginGitStar()
	url="http://gitstar.top:88/follow"
	response = requests.get(url,headers={'Accept': 'application/json','Cookie':cookie})
	bs=BeautifulSoup(response.text,"html.parser")
	jsn=bs.find_all("div",class_="media")
	list=[]
	for obj in jsn:
		try:
			list.append(obj.find('a')['href'].replace("https://github.com/",""))
		except Exception as e:
			pass
	return list
def follow(url):
	global AUTH
	requests.put("https://api.github.com/user/following/"+url
		,headers={'Content-Length': '0'}
		,auth=AUTH)

FollowList=getGitFollowList()
for url in FollowList:
	follow(url)
	print "Followed! -->{}".format(url)

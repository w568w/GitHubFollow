#-*- coding:utf-8 -*-  
import sys
import requests
import json
from requests.auth import HTTPBasicAuth
import settings

reload(sys)
sys.setdefaultencoding('utf-8')
COOKIE = None

class Gitstar():
	def __init__(self):
		self.cookie = None
	def loginGitStar(self):
		r=requests.post("http://gitstar.top:88/api/user/login",params={'username':settings.NAME,'password':settings.PASSWORD})
		self.cookie = r.headers['Set-Cookie']
	def getGitFollowList(self):
		self.loginGitStar()
		url = "http://gitstar.top:88/api/users/%s/status/follow-recommend"%settings.NAME
		response = requests.get(url,headers={'Accept': 'application/json','Cookie':self.cookie})
		jsn=response.json()
		list=[]
		for obj in jsn:
			list.append(obj['User'])
		return list
	def follow(self,url):
		AUTH = HTTPBasicAuth(settings.GITNAME, settings.GITPASSWORD)
		requests.put("https://api.github.com/user/following/"+url
			,headers={'Content-Length': '0'}
			,auth=AUTH)

	def update_gitstar(self):
		url = "http://gitstar.top:88/follow_update"
		res = requests.get(url,headers={'Accept': 'application/json','Cookie' : self.cookie})
		print "update:" + str(res.status_code == 200)

G = Gitstar()
FollowList = G.getGitFollowList()
t = len(FollowList)
print "need follow : %d" % t
i = 1
for url in FollowList:
	G.follow(url)
	print "[%d/%d]Followed! -->%s"%(i,t,url)
	i = i + 1

if t > 0:
	G.update_gitstar()

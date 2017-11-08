#-*- coding:utf-8 -*-  
import sys
import requests
import json
from pyquery import PyQuery as pyq
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
		print self.cookie
	def getGitFollowList(self):
		self.loginGitStar()
		url="http://gitstar.top:88/follow"
		response = requests.get(url,headers={'Accept': 'application/json','Cookie':self.cookie})
		d = pyq(response.text)
		jsn = d('.title a')
		print response
		list=[]
		for obj in jsn:
			print d(obj).attr('href')
			try:
				list.append(d(obj).attr('href').replace("https://github.com/",""))
			except Exception as e:
				pass
		return list
	def follow(self,url):
		AUTH = HTTPBasicAuth(settings.GITNAME, settings.GITPASSWORD)
		requests.put("https://api.github.com/user/following/"+url
			,headers={'Content-Length': '0'}
			,auth=AUTH)

	def update_gitstar():
		url = "http://gitstar.top:88/update"
		res = requests.get(url,headers={'Accept': 'application/json','Cookie' : self.cookie})
		print "update:" + str(res.status_code == 200)

G = Gitstar()
FollowList = G.getGitFollowList()
print "follow : %d" % len(FollowList)
i = 1
for url in FollowList:
	G.follow(url)
	print "[%d]Followed! -->%s"%(i,url)
	i = i + 1

if len(FollowList) > 0:
	G.update_gitstar()

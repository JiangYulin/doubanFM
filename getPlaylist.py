#!/usr/bin/env python2
#--coding:UTF-8
from urllib2 import urlopen,URLError
import sys


REQUEST_URL = "http://douban.fm/j/mine/playlist"
false = False

def require_data(request_url=REQUEST_URL):
	#__url = "http://douban.fm/j/mine/playlist"
	source_data = urlopen(request_url)
	data = source_data.read()
	dict_data = eval(data)
	if dict_data['r']!=0:
		raise Exception
	list_songs = dict_data['song']
	for song_temp in list_songs:
		song_temp['url']=song_temp['url'].replace('\\','')
		song_temp['picture']=song_temp['picture'].replace('\\','')
		song_temp['picture']=song_temp['picture'].replace('mpic','lpic')
		song_temp['album']=song_temp['album'].replace('\\','')
		yield song_temp
		songs_temp = None

class Playlist():
	def __init__(self):
		self.list = require_data()

	def next(self):
		try:
			return self.list.next()
		except StopIteration,e:
			self.list = require_data()
			return self.list.next()
		except URLError,e:
			print "network error:",e
			sys.exit()

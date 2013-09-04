#!/usr/bin/env python2
#--coding:UTF-8
import download
import getPlaylist
import thread
from time import sleep
import os
TEMP_PATH = "/tmp/doubanFM/"
if not os.path.isdir(TEMP_PATH):
	os.mkdir(TEMP_PATH)
class DLManager:
	def __init__(self):
		self.songs = []
		self.playlist = getPlaylist.Playlist()

	def dl(self):
		lock1 = thread.allocate_lock()
		flag1 = thread.allocate_lock()
		flag2 = thread.allocate_lock()
		songinfo = ''
		picpath = ''
		while True:
			if len(self.songs)>2 or lock1.locked():
				#print "self.song:",len(self.songs)
				#print "lock1.locked():",lock1.locked()
				sleep(1)
			else:
				if flag1.locked() and songinfo != '':
					if flag2.locked():
						songinfo['picture']=picpath
					self.songs.append(songinfo)
					print "new song"
				songinfo = self.playlist.next()
				musicname = songinfo['url'].split("/")[-1]
				picname = songinfo['picture'].split("/")[-1]
				picpath = TEMP_PATH+picname
				savepath = TEMP_PATH+musicname
				lock1.acquire()
				if flag1.locked():
					flag1.release()
				if flag2.locked():
					flag2.release()
				flag1.acquire()
				flag2.acquire()
				print songinfo['picture']
				thread.start_new_thread(download.download,(lock1,flag1,songinfo['url'],savepath,flag2,songinfo['picture'],picpath))
				songinfo['path']=savepath
	def getSong(self):
		if len(self.songs) == 0:
			return -1
		else:
			return self.songs.pop(0)
		

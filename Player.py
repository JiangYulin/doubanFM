#!/usr/bin/env python2
import pygst
pygst.require("0.10")
import gst
import glib,gobject
import thread
import time
import thread
import DLManager
import pynotify
import exceptions

class player:
	nowPlaying = None
	def __init__(self):
		self.player = gst.element_factory_make("playbin2","player")
		fakesink = gst.element_factory_make("fakesink","fakesink")
		self.player.set_property("video-sink", fakesink)
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message",self.on_message)
		self.a = DLManager.DLManager()
		pynotify.init("doubanFM")

	def on_message(self,bus,message):
		t = message.type
		#	print t
		if t==gst.MESSAGE_EOS:
			self.nextSong()
		elif t==gst.MESSAGE_ERROR:
			err,debug = message.parse_error()
			print "Error: %s" % err, debug
	def notify(self,songinfo):
		n = pynotify.Notification(" Now Playing"," "+songinfo['title']+"\n by "+songinfo['artist']+"\n from "+songinfo['albumtitle'])
		n.set_property('icon-name',songinfo['picture'])
		n.show()
	def nextSong(self):
		self.player.set_state(gst.STATE_NULL)
		songinfo = self.a.getSong()
		while songinfo == -1:
			time.sleep(1)
			songinfo = self.a.getSong()
		self.player.set_property("uri","file://"+songinfo['path'])
		self.nowPlaying = songinfo
		self.player.set_state(gst.STATE_PLAYING)
		try:
			self.notify(songinfo)
		except Exception,e:
			print e
	def pause(self):
		state = self.player.get_state()
		print(state[1])
		print(gst.STATE_PLAYING)
		if state[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_PAUSED)
		elif state[1] == gst.STATE_PAUSED:
			self.player.set_state(gst.STATE_PLAYING)
	def __ToPlay(self):
		self.player.set_state(gst.STATE_PLAYING)

	def setSong(self):
		thread.start_new_thread(self.a.dl,())
		self.nextSong()
		
	def getNowPlaying(self):
			return self.nowPlaying



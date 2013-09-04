from urllib2 import urlopen
from urllib2 import URLError
import os
import socket

READ_SIZE = 10240

def download(lock,flag,url,savepath,flag2,pictures,picpath):
	try:
		tempfile = open(savepath,"wb")
		socket.setdefaulttimeout(10)
		music = urlopen(url)
		data = music.read(READ_SIZE)
		while data:
			tempfile.write(data)
			data = music.read(READ_SIZE)
		tempfile.close()	
		
	except IOError, e:
		print 'could not open file:',e
		flag.release()
		os.remove(savepath)
	except URLError,e:
		print 'could not download file:',e
		flag.release()
		tempfile.close()
		os.remove(savepath)
		print "os.remove():",savepath
	try:
		picfile = open(picpath,"wb")
		picture = urlopen(pictures)
		data = picture.read(READ_SIZE)
		while data:
			picfile.write(data)
			data = picture.read(READ_SIZE)
		picfile.close()
	except Exception:
		flag2.release()
	finally:
		lock.release()

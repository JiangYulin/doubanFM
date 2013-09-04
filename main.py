#!/usr/bin/env python2
#--coding:UTF-8
import gobject
import glib
import Player
import thread
from time import sleep
import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt

class SystemTray(QtGui.QSystemTrayIcon):
    def __init__(self,parent=None):
        QtGui.QSystemTrayIcon.__init__(self,parent)
        self.setIcon(QtGui.QIcon("icon.png"))
        self.front = UI()
        self.front.show()
        self.Menu = QtGui.QMenu(parent)
        self.pauseaction = self.Menu.addAction("pause")
        self.exitaction = self.Menu.addAction("Exit")
        self.connect(self.exitaction, QtCore.SIGNAL("triggered()"),sys.exit)
        self.connect(self.pauseaction, QtCore.SIGNAL("triggered()"),self.pause) 
        self.activated.connect(self.windowHide)
        self.setContextMenu(self.Menu)
        
    def pause(self):
        self.front.player.pause()
        
    def windowHide(self,e):
        if e == QtGui.QSystemTrayIcon.Trigger:
            if self.front.isVisible():
                self.front.hide()
            else:
                self.front.show()
        

class UI(QtGui.QWidget):
    player = Player.player()
    nowPlaying = None
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUi()
        gobject.threads_init()
        self.loop = glib.MainLoop()
        
    def initUi(self):
        self.setWindowTitle('doubanFM')
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow )
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        grid = QtGui.QGridLayout()
        self.label = QtGui.QLabel()
        grid.addWidget(self.label)
        self.setLayout(grid)
        #绑定信号到foo函数
        self.connect(self, QtCore.SIGNAL('asdf()'),self.foo)
        self.startPlay()
        
    def sPixmap(self):
        flag = True
        while flag:
            if self.player.getNowPlaying() == None:
                sleep(1)
            elif self.player.getNowPlaying() == self.nowPlaying:
                sleep(1)
            else:
                self.nowPlaying = self.player.getNowPlaying()
                self.emit(QtCore.SIGNAL('asdf()'))
    #设置专辑图片，调整窗口大小 
    def foo(self):
        print "run foo"
        self.label.setPixmap(QtGui.QPixmap(self.nowPlaying['picture']).scaledToHeight(250))
        print self.label.size()
        self.label.adjustSize()
        print self.label.size()
        self.adjustSize()
        
    def nextSong(self):
        thread.start_new_thread(self.player.nextSong,())
        
    def startPlay(self):
            thread.start_new_thread(self.player.setSong,())
            thread.start_new_thread(self.sPixmap,())
            
    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos()-self.dragPos)
            e.accept()
            
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.dragPos=e.globalPos()-self.frameGeometry().topLeft()
            e.accept()
        if e.button() == Qt.RightButton:
            self.nextSong()            
            


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    e = SystemTray()
    e.show()
    #front.sPixmap()
    sys.exit(app.exec_())
    #front.loop.run()
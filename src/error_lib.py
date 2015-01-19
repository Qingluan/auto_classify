import os
import sys
from time import *
class QFilePathError(OSError):
	def __init__(self,path,*args):
		self.message = "path error : " + path+"\nother info :"  +"\n".join(args)
		self.args = (path,args,)
		
		try:
			self.filename = __file__
		except NameError:
			pass

	def __str__(self):
		return self.message


class progress(object):
	"""
		style can select "simple" or "default"

	"""
	status = {
		0 : '-> \\',
		1 : '-> |',
		2 : '-> /',
		3 : '-> -',
	}
	Style = {
		'default' : '#',
		'simple' : '',
	}
	def __init__(self,tag = 0,style="default"):
		self.tag = tag
		self.style = progress.Style[style]
		self.status = progress.status[self.tag]
		self.string = self.status + "\b\b\b\b\b"

	def _load(self,i):
		sys.stdout.write(self.string)
		sys.stdout.flush()
		self._count(i)
		
	def _count(self,i):
		self.tag = (self.tag + 1) %4
		if (i!= 100):
			self.string = self.style +progress.status[self.tag] +"%2d%s\b\b\b\b\b\b\b"%(i,'%')
		else:
			self.string = "\r ok "
	def __call__(self):
		for i in range(102):
			self._load(i)
			yield

	@classmethod
	def loading(cls,sty):
		print sty
		progresser = cls(tag=0,style=sty)
		# iteration = iterable_func(*args,**karg)
		# for step in progresser():
		# 	iteration.next()
		return progresser()
	@staticmethod
	def log(calls,all,now):
		_all = 0
		_now = now
		_count = 0
		if type(all) == type(0):
			_all = all
		else:
			_all = len(all)
		def _cal(all,now):
			return round(now* 100.0 /all )
		_pro = _cal(_all,_now)
		for i in calls:
			_count += 1
			if _count >= _pro:
				break
		return calls
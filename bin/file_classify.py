#!/usr/local/bin/python
import os


from pandas import DataFrame,Series
import argparse
from  time import sleep
import sys
class QFile(object):

	def __init__(self,file_or_dir,walk=False,level=0,debug = False,filter_type=[]):
		"""
			this file will provide some easy way to handle file or dir
		"""

		if os.path.exists(file_or_dir):
			self.top_name = file_or_dir
		else :
			raise QFilePathError(file_or_dir)
			sys.exit(0)

		self.bak_file_path = "/Users/darkh/.auto_classify.bak"
		self.bak_dir_path ="/Users/darkh/.auto_classify_dir.bak"
		self.bak_type = "bak"
		self.mkdir_path = {}
		self.debug = debug
		self.walk =walk
		self.type = "dir"
		self.Dictionary = {}
		self.sub_file = []
		self.sub_types = []
		self.moved_path = []
		self.rm_counter = {}

		# signal 
		self.ignore_type = None

		## counter area
		self._mkdir_counter = 0
		self._mkdir_all = 0
		self._mkdir_call = progress.loading("simple")
		self._move_counter = 0
		self._move_all = 0
		self._move_call = progress.loading("simple")
		self._rm_counter = 0
		self._rm_all = 0
		self._rm_call = progress.loading("simple")
		## 
		if os.path.isfile(self.top_name) :
			self.type = "file"

		if self.type == "dir":
			self._get_sub_info(walk=walk,level=level)
		self.dirs = [path for path in self.sub_file if os.path.isdir(path)]
		self.files = [path for path in self.sub_file if os.path.isfile(path) ]
		self._check()

	def _check(self):
		for f in self.dirs:

			name = os.path.basename(f)
			if name.lower() in self.sub_types:
				self.sub_file.remove(f)
				self.log("{} already exist ".format(f))
				self.log(self.sub_types)
			else:
				self.log("+{}  ".format(f))




	def _get_file_name(self,file_path):
		return os.path.dirname(file_path)

	def _get_sub_info(self,walk=False,level=0):
		if  self.type == "file":
			return None
		if not walk:
			self.sub_file = map(lambda x: os.path.join(self.top_name,x) ,os.listdir(self.top_name))
		else:
			self._walk(self.top_name,level)

		def __get_subtypes(files):
			return set(map(QFile.get_file_type, files))
		
		self.sub_types = __get_subtypes(self.sub_file)

		map(self._init_build_path, self.sub_types)
		#classify 
		self._classify()

	def _init_build_path(self,tp):
		self.mkdir_path[tp] =[] 


	def _classify(self):
		if not self.sub_types:
			return None
		res  = map(self._load, self.sub_file)
		return res

	def _load(self,file):
		type_f = QFile.get_file_type(file)
		if type_f in self.Dictionary:
			self.Dictionary[type_f].append(file)
			return "load"
		else:
			self.Dictionary[type_f] = [file]
			return "init"

	# def _walk_sub(self,callable):
		# os.path.walk(self.top_name, func, arg)


	#get info from instance
	#
	# magic method
	def __getitem__(self,key):
		index =None
		tp = None
		
		if type(key) ==type(""):
			tp = key

		else:
			tp,index = key

		if tp in self.Dictionary:
			if index:
				return self.Dictionary[tp][index]
			else :
				return self.Dictionary[tp]

	def __call__(self):
		return self.Dictionary


	def _walk(self,file,level=0):
		def _path(path,file):
			self.sub_file.append(os.path.join(path,file))

		level_count = 0 
		for  path,sub_finder,files in   os.walk(file):
			level_count += 1
			files_path_list = [path for i in files]
			dir_path_list = [path for i in sub_finder]

			#add file to sub_file
			map(_path,files_path_list,files)
			
			#add finder to sub_file
			map(_path, dir_path_list,sub_finder)

			if level != 0 and level_count >= level:
				break



	def bak_position(self):
		"""
			backup a position to file 
		"""
		# position = os.path.abspath(self.top_name)
		abso = lambda x: os.path.abspath(x)
		def _para(one_tuple):
			return [abso(one_tuple[0]),abso(one_tuple[1])]
		old = map(abso, self.sub_file)

		old_files = [file for file in old if os.path.isfile(file)]
		old_dir = map(abso, self.Dictionary['dir'])



		new_path = map(_para, self.moved_path)
		ser = DataFrame(new_path)
		ser = ser.T

		ser.to_csv(self.bak_file_path)
		ser_dir = Series(old_dir)
		ser_dir.to_csv(self.bak_dir_path)
		return ser
		print old_files
		print old_dir

	def backup(self):
		def _exist(path):
			if os.path.exists(path): return True
			return False

		def _check_dir(dir_p):
			if os.path.exists(dir_p): 
				return 0
			else:
				return 1
		
		if _exist(self.bak_dir_path) and _exist(self.bak_file_path) :


			new_path = DataFrame.from_csv(self.bak_file_path)
			dir_path = Series.from_csv(self.bak_dir_path)

			def _mo(one_tuple):
				f ,t = one_tuple
				try:
					os.rename(f, t)
				except OSError,e:
					print e
					print f,t
				self.log( "{} => {} ".format(f,t))

			for each_dir in dir_path:
				command = "mkdir -p {}".format(each_dir)
				os.popen(command)
			
			# res = 1
			# while res:
			# 	res = sum(map(_check_dir,dir_path))
			# 	sleep(0.5)
			# 	print "file not created ok wait ... 0.5 sec"

			for each in new_path.columns.tolist():

				one_row = new_path[each]
				_mo(one_row)


		else:
			print "no bak file"


	def keys(self):
		return self.sub_types

	def _ignore(self,type_key):
		def __remove_file_by_ignore(file_name):
			file_gender  = QFile.get_file_type(file_name)
			if type_key == file_gender: self.sub_file.remove(file_name)
			return file_name

		if type_key in self.sub_types:
			self.sub_types.remove(type_key)
			self.ignore_type = type_key

			self.ignore_files = map(__remove_file_by_ignore , self.sub_file )


	def auto_classify(self,ignore=None):
		def _check_dir(dir_p):
			if os.path.exists(dir_p): 
				return 0
			else:
				return 1
		if ignore in self.sub_types:
			self._ignore(ignore)

		self._mkdir_all = len(self.sub_types)
		mkdir_dirs =  map(self._mkdir,self.sub_types)
		self._mkdir_counter = 0
		self._mkdir_call = progress.loading("simple")
		res = 1
		while res:
			res = sum(map(_check_dir,mkdir_dirs))
			sleep(1)
			print "file not created ok wait ... 1 sec"

		self._move_all = len(self.sub_file)
		map(self._move, self.sub_file)
		
		#remove a temp signal 
		del self.ignore_type

		self._move_counter = 0
		self._move_call = progress.loading("simple")

		self.bak_position()
		self.check_empty(self.top_name)

	def check_empty(self,path,walk=False):
		"""
			this function is for rm empty dir ,
			when optional arg  "walk=True" ,this will do recursively

		"""
		absolute =  os.path.abspath
		if os.path.isdir(path) and os.path.exists(path):
			if not os.listdir(path):
				self.log("rm empty finder {} ".format(path))
				os.rmdir(path)
				return True
		if walk:
			self.rm_counter[path] = 0
			for sub_path ,dirs,files in os.walk(path):

				if files:

					self.rm_counter[absolute(sub_path)] = 0
				
					pass

				for dir in dirs:
					pth = os.path.join(sub_path,dir)

					self.rm_counter[absolute(pth)] = 1

				if dirs:
					map(self.check_empty, dirs)
				else:
					self.check_empty(sub_path)

		
			self.rm_dirs = [key for key in self.rm_counter if self.rm_counter[key]]
			self.rm_dirs.sort()
			self.rm_dirs.reverse()
			map(self.check_empty, self.rm_dirs)

	def _mkdir(self,type_f):
		
		dir_name = os.path.join(self.top_name,type_f)
		self.mkdir_path[type_f] = dir_name
		command  ="mkdir -p {}".format(dir_name)
		self.log(command)
		os.popen(command)
		self.progress_log("mkdir")
		return dir_name

	def progress_log(self,types):
		"""
		for display progress
		"""
		if types =="mkdir":
			self._mkdir_counter +=1
			progress.log(self._mkdir_call, self._mkdir_all, self._mkdir_counter)
		elif types == "move":
			self._move_counter +=1
			progress.log(self._move_call, self._move_all, self._move_counter)
 
	def _move(self,file):
		
		type_f = QFile.get_file_type(file)

		# reutrn None if type is ignord by user
		if type_f == self.ignore_type: return None

		if type_f in self.mkdir_path: 
			if self.walk  and type_f != "dir":
				pass
				self.log(file)
			else:

				file_name = os.path.basename(file)
				new_path = os.path.join(self.mkdir_path[type_f],file_name)
				try:
					os.rename(file, new_path)
				except OSError,e:
					print e 
					print "\n-- file : {} => {}\n".format(file,new_path) 
					print "try again : "
					
					dir_path = "/".join(new_path.split("/")[:-1])
					os.mkdir(dir_path)
					print "mkdir : ",new_path
					if os.path.exists(dir_path):
						print "re-mkdir : ok"
					print "try move ...",
					try:
						os.rename(file, new_path)
					except OSError ,e:
						print e 
						print "try failed .. ,given up !!"

				self.log( "{} => {}".format(file,new_path))
				self.moved_path.append([new_path,file])
		self.progress_log("move")

	################################
	###   static area  #############
	################################
	@staticmethod
	def get_file_type(file):
		res = os.path.basename(file).split(".")
		if os.path.isfile(file):

			if  len(res) >= 2 and res[0] :
				return res[-1]
			else:
				return "No_type_or_hide"
		elif os.path.isdir(file):
			return "dir"
		else:
			raise QFilePathError(file)


	def log(self,msg):
		if self.debug:
			print msg


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
def handle_args():

	desc = """
this is a assistant for write web html
weite by Qingluan
github : http://github.com/Qingluan
	"""
	parser = argparse.ArgumentParser(usage='it is usage for auto classify  ', description=desc)
	parser.add_argument('-a','--name_path',help="this argu is represent dir name",default="False")
	parser.add_argument("-b",'--backup',action='store_true',help="if -a and -b ,will back to position before classified",default=False)
	parser.add_argument('-c','--clear_path',default=None)
	parser.add_argument('-r','--recursion',action="store_true",default=False)
	parser.add_argument('-d','--debug',action="store_true",default=False)
	parser.add_argument('-i','--ignore',default=None)
	# args,remind = parser.parse_known_args(args)
	args = parser.parse_args()


	return args



if __name__ == "__main__":
	args = handle_args()
	path = args.name_path
	if os.path.exists(path) and path != "False":
		
		f = QFile(path)
		if  args.debug:
			f.debug= True
		if args.backup:
			print "remove empty finder ...",
			f.check_empty(path,walk=True)
			print "ok"
			print "start back to ",
			f.backup()
			print "ok"
			print "remove empty finder ...",
			f.check_empty(path,walk=True)
			print "ok"
		else:
			print "remove empty finder ...",
			f.check_empty(path,walk=True)
			print "ok"
			print "start classify ...\n"
			print "ignore type : {}".format(args.ignore)
			f.auto_classify(ignore=args.ignore)	
			print "ok"	
			print "remove empty finder ...",
			f.check_empty(path,walk=True)
			print "ok"
	
	if args.clear_path:
		clear_path = args.clear_path
		f = QFile(clear_path)
		f.debug =True
		if args.recursion:
			print 'recursively {}'.format(clear_path)
			f.check_empty(clear_path,walk=True)	
		else:
			print 'not recursively'
			f.check_empty(clear_path)

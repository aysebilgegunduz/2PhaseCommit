import xmlrpclib
import random
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from multiprocessing import Lock


class Coordinator:

	def __init__(self):
		self.replicas = []
		self.replica_add = []
		self.lock = threading.Lock()
		self.file = open("Coor.log", "a+")
		self.tran_id = 0
		self.isRecover = 0
		# self.recover()

	def recover(self):
		last_line = ""
		self.file = open("Coor.log", "r+")

		for line in self.file:
			last_line = line

		para = last_line.split(" ")
		print para
		
		if(str(para[-1]) == "Commit\n" or str(para[-1]) == "Abort\n"):
			return True
		# 	self.replica_add = para[1].split(",")
		# 	for add in self.replica_add:
		# 		self.replicas.append(xmlrpclib.ServerProxy(add))
		
		action = para[0]
		self.isRecover = 1

		if action == "put":
			print "recover"
			self.co_put(para[1], para[2])
		elif action == "get":
			self.co_get(para[1])
		elif action == "del":
			self.co_del(para[1])

		self.isRecover = 0


	def co_put(self, key, value):
		print "co_put"

		self.lock.acquire()
		self.file = open("Coor.log", "a+")

		print "isRecover" + str(self.isRecover)
		if not self.isRecover:
			self.file.write("put" + " " + key + " " + value)

		flag = ""

		for item in self.replicas:
			print item
			try:
				flag = item.rep_put(key, value)
				print "flag: " + str(flag)
			except Exception, e:
				print e.args
			if(flag == False):
				self.co_abort()
				self.file.write(" " + "Abort\n")
				return false

		self.co_commit()
		self.file.write(" " + "Commit\n")
		self.file.close()
		self.lock.release()
		

	def co_get(self, key):
		print "co_get"
		self.file = open("Coor.log", "a+")
		self.file.write("get " + key)

		random_num = random.randrange(0, len(self.replicas), 1);
		value = self.replicas[random_num].rep_get(key)
		print "Get value %s" % value

		self.file.write(" Commit\n")

	def co_del(self):
		pass

	def co_commit(self):

		for item in self.replicas:
			item.rep_commit()

	def co_abort(self):
		for item in self.replicas:
			item.rep_abort()

def main():
	coor = Coordinator()
	replica_add = ["http://localhost:8000"]#, "http://192.168.22.141:8001"]
	for add in replica_add:
		client = xmlrpclib.ServerProxy(add)
		coor.replicas.append(client)

	# coor.co_put("3", "this")
	# coor.recover()
 	# coor.co_put("2", "hi")
 	# modify the last transaction to not commit or abort

 	# coor.co_get("2")
 	# coor = Coordinator()
 	coor.recover()


if __name__ == '__main__':
	main()
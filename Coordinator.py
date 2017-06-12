import xmlrpclib
import random
import threading
import sys

class Coordinator:

	def __init__(self):
		self.participants = []
		self.participant_add = []
		self.lock = threading.Lock()
		self.file = open("Coor.log", "a+")
		self.tran_id = 0
		self.isRecover = 0
		# self.recover()
	flag = False
	def recover(self):
		last_line = ""
		self.file = open("Coor.log", "r+")

		for line in self.file:
			last_line = line

		param = last_line.split(" ")
		print param
		
		if(str(param[-1]) == "Commit\n" or str(param[-1]) == "Abort\n"):
			print "Do not need to recover"
			return True
		
		action = param[0]
		self.isRecover = 1

		if action == "put":
			print "recover put func"
			self.co_put(param[1], param[2])
		elif action == "get":
			print "recover get func"
			self.co_get(param[1])
		elif action == "del":
			print "recover del func"
			self.co_del(param[1])

		self.isRecover = 0


	def co_put(self, key, value):
		print "co_put"

		self.lock.acquire()
		self.file = open("Coor.log", "a+")

		print "isRecover" + str(self.isRecover)
		if not self.isRecover:
			self.file.write(" put" + " " + key + " " + value)



		for item in self.participants:
			print item
			try:
				flag = item.rep_put(key, value)
				print "flag: " + str(flag)
			except Exception, e:
				print e.args
			if(flag == False):
				self.co_abort()
				self.file.write(" " + "Abort\n")
				return False

		self.co_commit()
		self.file.write(" " + "Commit\n")
		self.file.close()
		self.lock.release()
		

	def co_get(self, key):
		print "co_get"
		self.file = open("Coor.log", "a+")
		self.file.write(" get " + key)

		random_num = random.randrange(0, len(self.participants), 1);
		value = self.participants[random_num].rep_get(key)
		print "Get value %s" % value

		self.file.write(" Commit\n")
		self.co_commit()

	def co_del(self, key):
		print "co_del"
		self.file = open("Coor.log", "a+")
		self.file.write(" del "+key)

		self.lock.acquire
		for item in self.participants:
			print item
			flag = False
			try:
				flag = item.rep_del(key)
				print "flag: "+str(flag)
			except Exception,e:
				print e.args
			if flag==False :
				self.co_abort()
				self.file.write(" "+"Abort\n")
				return False
		self.co_commit()
		self.file.write(" " + "Commit\n")
		self.file.close()
		self.lock.release

	def co_commit(self):
		print "Calling all replicas to commit"
		for item in self.participants:
			item.rep_commit()


	def co_abort(self):
		print "Calling all replicas to abort"
		for item in self.participants:
			item.rep_abort()

def main():
	coor = Coordinator()
	participant_add = ["http://localhost:5001","http://localhost:5002" ]
	for add in participant_add:
		try:
			client = xmlrpclib.ServerProxy(add)
			print client
		except:
			print "Wrong one"

		coor.participants.append(client)

	# coor.recover()
	#coor.co_put("2", "Testcase2")
	#coor.co_put("3", "Testcase3")
	coor.co_del("2")
	coor.co_get("2")
	coor.recover()
	coor.co_put("2", "hi")
	# modify the last transaction to not commit or abort

	coor.co_get("2")
	# coor = Coordinator()


if __name__ == '__main__':
	main()
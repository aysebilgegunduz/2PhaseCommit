import xmlrpclib 
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sqlite3 as lite

class Replica:
	def __init__(self, name):
		self.name = name
		self.log = file(self.name + '.log', 'a+')

		try:
			self.conn = lite.connect(self.name + '.db')
			self.cur = self.conn.cursor()
			self.cur.execute('CREATE TABLE IF NOT EXISTS Info(key INT PRIMARY KEY, value TEXT)')
			self.conn.commit()
		except lite.Error, e:
			print "Error %s" % e.args[0]
			sys.exit(1)
		# finally:
		# 	if(self.conn):
		# 		self.conn.close()


	def rep_get(self, key):
		ret = ""
		print self.name
		try:
			self.cur.execute('SELECT value FROM Info WHERE key = ?', key)
			ret = self.cur.fetchone()
			# print  type(ret)
		except Exception, e:
			print e.args
		return str(ret)

	def rep_put(self, key, value):
		try:
			self.cur.execute('INSERT OR REPLACE INTO Info VALUES(?, ?)', (key, value))
		except lite.Error, e:
			print e.args
		return True
	
	def rep_decide(self):
		line = self.log.readline()
		params = line.split(" ")
		if(params[0]):
			rep_recover()
			return False
		else:
			return True

	def rep_commit(self):
		try:
			self.conn.commit()
		except lite.Error, e:
			print e.args
		return True		

	def rep_abort(self):
		try: 
			self.conn.abort()
		except lite.Error, e:
			print e.args
		return True

def main():
	try:
		server = SimpleXMLRPCServer(("localhost", 8000))
		# server2 = SimpleXMLRPCServer(("localhost", 8001))
		print "Listen"
		replica = Replica('Bob')
		# relica2 = Replica('Anne')
		server.register_instance(replica)
		server.serve_forever()


	except Exception,e:
		print e.args

	# replica = Replica('Bob')
	# print replica.rep_get('1')

if __name__ == '__main__':
	main()

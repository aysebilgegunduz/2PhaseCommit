import xmlrpclib
import random
import threading
import sys

class Leader:
    def __init__(self):
        self.participants = []
        self.participant_add = []
        self.lock = threading.Lock()
        self.file = open("Lead.log", "a+")
        self.tran_id = 0
        self.isRecover = 0

    # self.recover()
    flag = False

    def recover(self):
        last_line = ""
        self.file = open("Lead.log", "r+")

        for line in self.file:
            last_line = line

        param = last_line.split(" ")
        print param

        if (str(param[-1]) == "Commit\n" or str(param[-1]) == "Abort\n"):
            print "Do not need to recover"
            return True

        action = param[0]
        self.isRecover = 1

        if action == "put":
            print "recover put func"
            self.lead_put(param[1], param[2])
        elif action == "get":
            print "recover get func"
            self.lead_get(param[1])
        elif action == "del":
            print "recover del func"
            self.lead_del(param[1])

        self.isRecover = 0

    def p_recover(self, key):
        for item in self.participants:
            item.par_recover()

    def lead_put(self, key, value):
        print "lead_put"
        self.lock.acquire()
        self.file = open("Lead.log", "a+")

        print "isRecover " + str(self.isRecover)
        if not self.isRecover:
            self.file.write(" put" + " " + key + " " + value)
        for item in self.participants:
            print item
            try:
                flag = item.par_put(key, value)
                print "flag: " + str(flag)
            except Exception, e:
                print e.args
            if (flag == False):
                self.lead_abort()
                self.file.write(" " + "Abort\n")
                return False
        if int(key) != 4:
            self.lead_commit()
            self.file.write(" " + "Commit\n")
            self.file.close()
            self.lock.release()
        else:
            print "Leader said yes then vanish, participants blocked"

    def lead_get(self, key):
        print "lead_get"
        self.file = open("Lead.log", "a+")
        self.file.write(" get " + key)

        random_num = random.randrange(0, len(self.participants), 1);
        value = self.participants[random_num].par_get(key)
        print "Get value %s" % value

        self.file.write(" Commit\n")
        self.lead_commit()

    def lead_del(self, key):
        print "lead_del"
        self.file = open("Lead.log", "a+")
        self.file.write(" del " + key)

        self.lock.acquire
        for item in self.participants:
            print item
            flag = False
            try:
                flag = item.par_del(key)
                print "flag: " + str(flag)
            except Exception, e:
                print e.args
            if flag == False:
                self.lead_abort()
                self.file.write(" " + "Abort\n")
                return False
        self.lead_commit()
        self.file.write(" " + "Commit\n")
        self.file.close()
        self.lock.release

    def lead_decide(self, key):
        flag = False
        for item in self.participants:
            flag ^= item.par_decide(key)  # logical and
        return flag

    def lead_commit(self):
        print "Calling all participants to commit"
        for item in self.participants:
            item.par_commit()

    def lead_abort(self):
        print "Calling all participants to abort"
        for item in self.participants:
            item.par_abort()


def main():
    leader = Leader()
    participant_add = ["http://localhost:5001"]#, "http://localhost:5002"]
    for add in participant_add:
        try:
            client = xmlrpclib.ServerProxy(add)
            print client
        except:
            print "Wrong one"

        leader.participants.append(client)

    # leader.recover()
    leader.lead_put("4", "Testcase4")
    leader.lead_put("3", "Testcase3")
    leader.lead_del("1")
    # leader.lead_get("2")
    # leader.lead_abort()
    # leader.recover()

    # one of them will died so false will come back but then it will recover.
    leader.lead_put("2", "hi")
    leader.p_recover()
    # leader.lead_put("1", "Test")

    # leader.lead_get("2")

if __name__ == '__main__':
    main()
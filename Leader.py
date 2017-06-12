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

        action = param[1]
        self.isRecover = 1
        self.lock.acquire()
        if action == "put":
            print "recover put func"
            self.lead_commit()
            self.file.write(" " + "Commit\n")
        elif action == "get":
            print "recover get func"
            self.lead_get(param[2])
        elif action == "del":
            print "recover del func"
            self.lead_del(param[2])
        self.file.close()
        self.lock.release()
        self.isRecover = 0

    def lead_put(self, key, value):
        print "lead_put"
        self.lock.acquire()
        self.file = open("Lead.log", "a+")
        for item in self.participants:
            print item
            try:
                flag = item.par_put(key, value)
                print "flag: " + str(flag)
            except Exception, e:
                print e.args
            if flag == False:
                self.lead_abort()
                self.file.write(" " + "Abort\n")
                return False
            elif int(key) == 2:
                self.file.write(" put" + " " + key + " " + value)
        if int(key) !=2:
            if int(key) != 4:
                self.lead_commit()
                self.file.write(" " + "Commit\n")
            else:
                print "Leader said yes then vanish, participants blocked"
        self.file.close()
        self.lock.release()

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

    def p_recover(self):
        for item in self.participants:
            item.par_recover()


def main():
    leader = Leader()
    participant_add = ["http://localhost:5001", "http://localhost:5002"]
    for add in participant_add:
        try:
            client = xmlrpclib.ServerProxy(add)
            print client
        except:
            print "Wrong one"

        leader.participants.append(client)

    # leader.recover()

    print "Happy Path: "
    leader.lead_put("3", "Testcase3") #3 means happy path
    print"\n"

    print "Leader vanish : "
    leader.lead_put("4", "Testcase4") #4 means leader will fail
    print"\n"

    print "Participants fail before voting: "
    leader.lead_del("1") #1 means participant fail before voting
    print"\n"

    print "Participants fail after yes voting: "
    leader.lead_put("2", "hi") #2 means participant will fail after yes voting
    print"\n"

    print "Recover participants and go on where they left: "
    leader.p_recover() #to recover participant
    leader.recover() #to recover leader
if __name__ == '__main__':
    main()
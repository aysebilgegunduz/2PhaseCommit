from multiprocessing import Pool


def write_file():
    f = open('test.txt', "r+")
    # f.write("123 " + "test " )
    # f.write("123 " + "test " )
    # f.write("123 " + "test " + "commit\n" )
    # f.write("123 " + "test " + "commit2\n" )

    # f.seek(0)
    pos = 0
    # print f.readline()
    for line in f:
        f.seek(pos)
        print pos
        f.write("new")
        f.flush()
        pos += len(line) + len("new")



if __name__ == '__main__':
    write_file()
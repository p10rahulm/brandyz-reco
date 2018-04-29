
def openfile_returnlist(csvfilename):
    with open(csvfilename) as f:
        x=[]
        for line in f:
            # last character is a \n
            x.append(line[:-1].split("\t"))
    return x

if __name__ == "__main__":
    mylist = openfile_returnlist("data/brands_filtered.txt")
    print(mylist[0:2])

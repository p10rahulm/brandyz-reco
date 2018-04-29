import csv

def openfile_returnlist(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines,len(lines)

def lines_to_df(list_of_lines):
    for line in list_of_lines:
        g = line.split("\t")

if __name__ == "__main__":
    (mylist,listlength) = openfile_returnlist("data/brands_filtered.txt")
    print(mylist[0:2])
    print(listlength)

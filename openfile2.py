import numpy as np

def openfile_returnlist(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines,len(lines)

def lines_operations(list_of_lines,list_length):
    shopping_profile_id = np.zeros((list_length), dtype=int)
    brand_id = np.zeros((list_length), dtype=int)
    for line in list_of_lines:
        g = line.split("\t")

if __name__ == "__main__":
    (mylist,listlength) = openfile_returnlist("data/brands_filtered.txt")
    print(mylist[0:2])
    print(listlength)

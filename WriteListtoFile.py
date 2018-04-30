
def write_file(filename,outlist):
    outfile = open(filename, 'w')
    for list_item in outlist:
        outfile.write(str(list_item))
        outfile.write('\n')
    outfile.close()
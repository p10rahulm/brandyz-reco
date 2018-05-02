# for windows download sed from here: http://gnuwin32.sourceforge.net/packages/sed.htm
# on second thoughts: https://stackoverflow.com/questions/1823591/sed-creates-un-deleteable-files-in-windows/25407238
# Use the following: https://github.com/mbuilov/sed-windows/blob/master/sed-4.4-x64.exe

import subprocess


def tail(filename, numlines):
    # get last line from tail subprocess
    # - note for windows had to download gnu unixutils from https://sourceforge.net/projects/unxutils/reviews/
    # - add it to path, etc
    numlines_str = '-'+str(numlines)
    # object returned is bytes-like. Need to convert to str.
    return str(subprocess.check_output(['tail', numlines_str, filename]))[1:]


def replace_line_number(filename,linenumber,newline_string):
    # below is a sample conversion which targets the first line on file.txt
    # sed - i "1s/.*/$var/" file.txt
    sed_command = str(linenumber) +  "s/.*/" + newline_string + "/"
    # calling subprocess function to oursource replacement to sed. This is much faster than any python based solution
    subprocess.call(["sed", "-i", sed_command, filename])

if __name__=="__main__":
    print(tail("SedOperations.py",1))
    with open("output/test/some_sed_test.txt") as f:
        new_first_line = str(int(f.readline())+1)
    replace_line_number("output/test/some_sed_test.txt",1,new_first_line)
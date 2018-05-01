# We will use this to add a new file to our simple database, found in the output folder

import SedOperations

def add_new_user(users_db_filename):
    replace_first_line(users_db_filename)
    add_last_line(users_db_filename)

def add_last_line(users_db_filename):
    outfile = open(users_db_filename, 'r')
    size_var = int(outfile.readline().split(":")[1])
    outfile.close()
    # get last line from tail subprocess
    # Moved to SedOperations

    # last_line = str(subprocess.check_output(['tail', '-1', users_db_filename]))
    last_line = SedOperations.tail(users_db_filename,1)
    total_lines = str(last_line.split(",")[3])
    created_line = str(size_var-1) + ",0," + total_lines + "," + total_lines + ",[]"
    outfile = open(users_db_filename, 'a')
    print(created_line,file=outfile)
    outfile.close()


def replace_first_line(users_db_filename):
    # replace first line in file using sed
    outfile = open(users_db_filename, 'r')
    size_var = outfile.readline()
    outfile.close()
    size_list = size_var.split(":")
    size_list[1] = str(int(size_list[1]) + 1)
    size_var = ": ".join(size_list)
    SedOperations.replace_line_number(users_db_filename, 1, size_var)


if __name__== "__main__":
    add_new_user("output/writedf_test.txt")

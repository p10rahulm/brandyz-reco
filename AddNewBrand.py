# We will use this to add a new brand to our simple database, found in the output folder

import SedOperations

def add_new_brand(brand_db_filename,brand_category,brand_scale):
    df_size = replace_first_line(brand_db_filename)
    add_last_line(brand_db_filename,brand_category,brand_scale,df_size)


def replace_first_line(brand_db_filename):
    # replace first line in file using sed
    outfile = open(brand_db_filename, 'r')
    size_var = outfile.readline()
    outfile.close()
    size_list = size_var.split(":")
    size_list[1] = str(int(size_list[1]) + 1)
    size_var = ": ".join(size_list)
    SedOperations.replace_line_number(brand_db_filename, 1, size_var)
    return int(size_list[1])-1


def add_last_line(brand_db_filename,brand_category,brand_scale,df_size):
    size_var = df_size
    created_line = str(size_var) + ",0,[],"+str(brand_category)+","+str(brand_scale)+",0,0"
    outfile = open(brand_db_filename, 'a')
    print(created_line,file=outfile)
    outfile.close()




if __name__== "__main__":
    add_new_brand("output/writebrand_df_test.txt",0,2)

# We'll use this module to read from the simple database we created earlier.


import numpy as np,re

def read_simple_db(db_filename):
    db_txt = open(db_filename, 'r')
    rows = int(db_txt.readline().split(": ")[1])
    columns = int(db_txt.readline().split(": ")[1])
    print(rows,columns)
    # Let one line go
    db_txt.readline()
    # initialize column_names and column_classes
    col_names = []
    col_classes = []

    for i in range(columns):
        col_detail = db_txt.readline().rstrip("\n").split(",")
        col_names.append(str(col_detail[0]))
        col_classes.append(col_detail[1])
    # Initialize the output dictionary
    db = {}
    db["meta"] = {}
    db["meta"]["size"] = rows
    db["meta"]["num_columns"] = columns
    db["meta"]["column_type_list"] = []
    for i in range(columns):
        # unless it is a list, we are going to initialize to np.zeros of appropriate class
        if(col_classes[i]!="list"):
            db[col_names[i]] = np.zeros(rows,dtype=np.dtype(col_classes[i]))
        elif(col_classes[i]=="list"):
            db[col_names[i]] = [None] * rows
        db["meta"]["column_type_list"].append((col_names[i],col_classes[i]))
    # let one line go
    db_txt.readline()
    for i in range(rows):
        dataline = db_txt.readline()
        list_removed = re.sub("[\(\[].*?[\)\]]", "", dataline)
        column_values = list_removed.split(",")
        list_in_dataline = dataline[dataline.find("[")+1:dataline.find("]")]
        list_values = [int(i) for i in list_in_dataline.split(",")]
        '''
        print("---")
        print("dataline")
        print(dataline)
        print("lista")
        print(list_in_dataline)
        print("lists_removed")
        print(list_removed)
        '''
        for j in range(columns):
            # unless it is a list, we are going to initialize to np.zeros of appropriate class
            if (col_classes[j] != "list"):
                db[col_names[j]][i] = column_values[j]
            elif (col_classes[j] == "list"):
                db[col_names[j]][i] = []
                for k in range(len(list_values)):
                    db[col_names[j]][i].append(list_values[k])
    return db




if __name__ =="__main__":
    db = read_simple_db("output/brand_details.txt")
    import WritetoFile
    WritetoFile.write_df_to_file("output/df_reader_test.txt", db)

    db = read_simple_db("output/user_details.txt")
    import WritetoFile
    WritetoFile.write_df_to_file("output/df_reader_test_user.txt", db)

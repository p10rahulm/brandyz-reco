import numpy as np,re

def openfile_returnlist(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines

def data_operations(list_of_lines):
    list_length = len(list_of_lines)
    shopping_profile_id = np.zeros((list_length-1), dtype=int)
    brand_id = np.zeros((list_length-1), dtype=int)
    id_brand_mapping = {}
    for line_number in range(1,list_length):
        g = list_of_lines[line_number].split('\t')
        shopping_profile_id[line_number-1] = int(g[0])
        brand_id[line_number-1] = int(g[1])
        # I'm using re.sub to remove all non ascii stuff. This is for easier usage later.
        # id_brand_mapping[brand_id[line_number-1]]=re.sub(r'[^\x00-\x7f]',r' ',g[2]).rstrip('\n')
        # Making even more stringent
        id_brand_mapping[brand_id[line_number - 1]] = re.sub(r'[^A-Za-z0-9\s]', r'', g[2]).rstrip('\n')
    return (shopping_profile_id,brand_id,id_brand_mapping)

if __name__ == "__main__":
    brands_preference_lines = openfile_returnlist("data/brands_filtered.txt")
    print(brands_preference_lines[0:2])
    print(len(brands_preference_lines))
    (shopping_profile_id, brand_id, id_brand_mapping) = data_operations(brands_preference_lines)
    print(shopping_profile_id[0:3])
    print(brand_id[0:3])
    print(id_brand_mapping[51])

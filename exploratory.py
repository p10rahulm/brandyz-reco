import openfile,numpy as np
from collections import defaultdict


def get_data(filename):
    brands_preference_lines = openfile.openfile_returnlist(filename)
    (shopping_profile_id, brand_id, id_brand_mapping) = openfile.data_operations(brands_preference_lines)
    return (shopping_profile_id, brand_id, id_brand_mapping)


def get_encoder_dict(column):
    encodings = defaultdict(int)
    unique_col = np.unique(column)
    print(len(unique_col))
    code = 0;
    for num in unique_col:
        encodings[num] = code;
        code+=1;
    return (encodings,code)


def encode_column(column,encodings):
    new_column = np.zeros(len(column),dtype=np.int)
    for i in range(len(column)):
        new_column[i] = encodings[column[i]]
    return new_column


def encode(column):
    (encoded_dict,num_unique) = get_encoder_dict(column)
    new_column = encode_column(column,encoded_dict)
    return (new_column,encoded_dict,num_unique)


def encode_shoppers_brands(shopper_ids, brand_ids):
    (shoppers, shopper_code_dictionary,num_shoppers) = encode(shopper_ids)
    (brands, brands_dictionary,num_brands) = encode(brand_ids)
    print(num_brands,num_shoppers)
    print(shoppers[1:10])
    print(brands[1:10])
    return (shoppers,shopper_code_dictionary,num_shoppers,brands,brands_dictionary,num_brands)

def get_user_purchase_matrix(shoppers,numshoppers, brands,num_brands):
    # numpy zeros is sparse, so size is ok.
    shopper_brand_matrix = np.zeros((numshoppers,num_brands),dtype = np.int8)
    for i in range(num_shoppers):
        shopper_brand_matrix[shoppers[i],brands[i]]+=1
    return shopper_brand_matrix


def get_user_purchase_deets(shoppers,brands,):
    num_shoppers = len(shoppers)
    num_brands = len(brands)
    shopper_brand_matrix = np.zeros((num_shoppers,num_brands),dtype = np.int8)
    for i in range(num_shoppers):
        shopper_brand_matrix[shoppers[i],brands[i]]+=1
    return shopper_brand_matrix


def get_product_co_purchase_matrix(shoppers,numshoppers, brands,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.int8)
    i=0;
    while i < len(shoppers):
        j = 1
        while shoppers[i+j] == shoppers[i]:
            brand_copurchase_matrix[brands[i],brands[i+j]] +=1
            j+=1
        i+=1
    return brand_copurchase_matrix

if __name__ == "__main__":
    (shopping_profile_id, brand_id, id_brand_mapping) = get_data("data/brands_filtered.txt")
    print(shopping_profile_id[0:100])
    print(brand_id[0:100])
    print(id_brand_mapping[51])
    (shoppers,shopper_code_dictionary,num_shoppers,brands,brands_dictionary,num_brands) =\
        encode_shoppers_brands(shopping_profile_id, brand_id)
    print("encoding done")
    shopper_brand_matrix = get_user_purchase_matrix(shoppers,num_shoppers, brands,num_brands)
    print("shopper brand matrix")
    print(shopper_brand_matrix[0])
    del shopper_brand_matrix
    brand_copurchase_matrix = get_product_co_purchase_matrix(shoppers,num_shoppers,brands,num_brands)
    print("brand_copurchase_matrix[0]")
    print(brand_copurchase_matrix[0])

    # np.savetxt("output/shopper_brand_matrix.txt",shopper_brand_matrix)




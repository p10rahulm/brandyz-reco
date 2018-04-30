import Openfile,ConverttoFactor,WriteListtoFile,UserBrandPurchaseMatrix,ProductCopurchase,UserDetails
import numpy as np
import time


def get_data(filename):
    brands_preference_lines = Openfile.openfile_returnlist(filename)
    (shopping_profile_id, brand_id, id_brand_mapping) = Openfile.data_operations(brands_preference_lines)
    return (shopping_profile_id, brand_id, id_brand_mapping)


def encode_transactions(shopper_ids, brand_ids):
    (shoppers, shopper_code_dictionary,unique_shoppers) = ConverttoFactor.convert_to_factor(shopper_ids)
    (brands, brands_dictionary,unique_brands) = ConverttoFactor.convert_to_factor(brand_ids)
    return (shoppers,shopper_code_dictionary,unique_shoppers,brands,brands_dictionary,unique_brands)


'''
#below is damn slow. reworking
def get_product_co_purchase_matrix_old(shoppers,brands,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.int8)
    i=0;
    while i < len(shoppers):
        j = 1
        while shoppers[i+j] == shoppers[i]:
            brand_copurchase_matrix[brands[i],brands[i+j]] +=1
            j+=1
        i+=1
        if(i%10000==0):
            print(i)
    return brand_copurchase_matrix
'''

if __name__ == "__main__":
    timestart = time.time()
    print("getting data")
    (shopping_profile_id, brand_id, id_brand_mapping) = get_data("data/brands_filtered.txt")
    print("data obtained: sample results below:- ")
    print("first 100 shopper details : ",shopping_profile_id[0:100])
    print("first 100 brand 1ds: ",brand_id[0:100])
    print("brand_id_mapping : ",id_brand_mapping[51])
    print("---------------------")


    (shoppers,shopper_code_dictionary,num_uniq_shoppers,brands,brands_dictionary,num_uniq_brands) =\
        encode_transactions(shopping_profile_id, brand_id)
    print("encoding done: encoded results below:- ")
    print("first 100 shopper details : ", shoppers[0:100])
    print("first 100 brand 1ds: ", brands[0:100])
    print("brand_code_mapping[51] : ", brands_dictionary[51])
    print("---------------------")


    print("getting brand matrix")
    shopper_brand_matrix = UserBrandPurchaseMatrix.get_user_purchase_matrix(shoppers, num_uniq_shoppers, brands, num_uniq_brands)
    print("sparse purchase matrix obtained: first row below:- ")
    print(shopper_brand_matrix[0])
    shopper_brand_matrix


    print("getting user_wise details")
    user_deets = UserDetails.get_user_purchase_deets(shoppers, num_uniq_shoppers, brands)
    print("write userdetails to file")
    WriteListtoFile.write_file('output/user_details.txt',user_deets)
    print("user_deets[0:5]")
    print(user_deets[0:5])

    print("getting brand_wise details")
    brand_deets = get_brand_purchase_deets(shoppers, brands,num_uniq_brands)
    print("write brand_details to file")
    WriteListtoFile.write_file('output/user_details.txt', user_deets)
    print("user_deets[0:5]")
    print(user_deets[0:5])

    print("get_copurchase list")
    copurchase_list = ProductCopurchase.get_copurchase_list(user_deets)
    print("len(copurchase_list)=",len(copurchase_list))

    print("get_copurchase matrix")
    copurchase_matrix = ProductCopurchase.get_product_co_purchase_matrix(copurchase_list, num_uniq_brands)

    print("save to file")
    np.savetxt("output/copurchase_matrix.csv",copurchase_matrix, delimiter=",", fmt="%6d")

    print("Done! Time taken = ", time.time() - timestart)






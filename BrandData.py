import Openfile,ConverttoFactor,WritetoFile,UserBrandPurchaseMatrix,ProductCopurchase,UserDetails, BrandDetails,AddBrandTags,AddUserTags
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



if __name__ == "__main__":
    timestart = time.time()
    print("getting data")
    (shopping_profile_id, brand_id, id_brand_mapping) = get_data("data/brands_filtered.txt")
    print("data obtained: sample results below:- ")
    print("first 100 shopper details : ",shopping_profile_id[0:100])
    print("first 100 brand 1ds: ",brand_id[0:100])
    print("brand_id_mapping : ",id_brand_mapping[51])
    print("---------------------")


    (shoppers,shopper_code_dictionary,num_uniq_shoppers,brands,brand_id_code_dictionary,num_uniq_brands) =\
        encode_transactions(shopping_profile_id, brand_id)
    print("encoding done: encoded results below:- ")
    print("first 100 shopper details : ", shoppers[0:100])
    print("first 100 brand 1ds: ", brands[0:100])
    print("brand_id_code_mapping[51] : ", brand_id_code_dictionary[51])
    # we need to reverse this dictionary to get the brand id from code
    brand_code_id_dictionary = {code: id for id, code in brand_id_code_dictionary.items()}
    brand_code_name_dictionary = {code: id_brand_mapping[id] for code, id in brand_code_id_dictionary.items()}
    print("brand_code_id_mapping[38] : ", brand_code_id_dictionary[38])
    print("brand_code_name_mapping[38] : ", id_brand_mapping[brand_code_id_dictionary[38]])
    print("brand_code_name_mapping[38] : ", brand_code_name_dictionary[38])
    print("---------------------")

    '''
    print("getting brand matrix")
    shopper_brand_matrix = UserBrandPurchaseMatrix.get_user_purchase_matrix(shoppers, num_uniq_shoppers, brands, num_uniq_brands)
    print("sparse purchase matrix obtained: first row below:- ")
    print(shopper_brand_matrix[0])
    '''
    
    print("getting user_wise details")
    user_deets = UserDetails.get_user_purchase_deets(shoppers, brands)
    print("Add user tags to user details")
    user_deets = AddUserTags.get_percentile_tags(user_deets)
    print("write userdetails to file")
    WritetoFile.write_df_to_file('output/user_details.txt', user_deets)
    print("user_deets[meta]")
    print(user_deets["meta"])

    '''
    print("getting brand_wise details")
    brand_deets = BrandDetails.get_brand_purchase_deets(shoppers, brands)
    brand_deets = AddBrandTags.add_names(brand_deets,brand_code_name_dictionary)
    print("Add brand tags to brand details")
    # Add categories
    brand_deets = AddBrandTags.add_random_categories(brand_deets)
    # Add some ordinal scale
    brand_deets = AddBrandTags.add_random_ordinal_scale(brand_deets)
    # Add percentile tag
    brand_deets = AddBrandTags.get_percentile_tags(brand_deets)
    # Even though it has not been mentioned whether the data has been ordered time-stamp wise, if we assume it has been,
    # we can add a value tag - how many times has this brand been the first purchase of user
    brand_deets = AddBrandTags.first_purchase(brand_deets,shoppers, brands)
    print("write brand_details to file")
    WritetoFile.write_df_to_file('output/brand_details.txt', brand_deets)
    print("brand_deets[meta]")
    print(brand_deets["meta"])

    '''
    print("get_copurchase list")
    copurchase_list = ProductCopurchase.get_copurchase_list(user_deets)
    print("len(copurchase_list)=",len(copurchase_list))

    print("get_copurchase matrix")
    copurchase_matrix = ProductCopurchase.get_product_co_purchase_matrix(copurchase_list, num_uniq_brands)

    print("save to file")
    np.save("output/copurchase_matrix.txt",copurchase_matrix,allow_pickle=True)
    # np.savetxt("output/copurchase_matrix.txt",copurchase_matrix, delimiter=",", fmt="%6d")



    print("Done! Time taken = ", time.time() - timestart)








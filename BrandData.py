import Openfile,ConverttoFactor,WritetoFile,UserBrandPurchaseMatrix,ProductCopurchase,UserDetails, BrandDetails,AddBrandTags,AddUserTags
import numpy as np
import time,pickle


def get_data(filename):
    brands_preference_lines = Openfile.openfile_returnlist(filename)
    (shopping_profile_id, brand_id, id_brand_mapping) = Openfile.data_operations(brands_preference_lines)
    return (shopping_profile_id, brand_id, id_brand_mapping)


def encode_transactions(shopper_ids, brand_ids):
    (shoppers, shopper_code_dictionary,unique_shoppers) = ConverttoFactor.convert_to_factor(shopper_ids)
    (brands, brands_dictionary,unique_brands) = ConverttoFactor.convert_to_factor(brand_ids)
    return (shoppers,shopper_code_dictionary,unique_shoppers,brands,brands_dictionary,unique_brands)


def get_intermediate_files_from_raw_data(filename):
    # Get raw data from file
    (shopping_profile_id, brand_id, id_brand_mapping) = get_data(filename)
    # Encode data
    (shoppers, shopper_code_dictionary, num_uniq_shoppers, brands, brand_id_code_dictionary, num_uniq_brands) = \
        encode_transactions(shopping_profile_id, brand_id)
    # Get dictionary mappings
    brand_code_id_dictionary = {code: id for id, code in brand_id_code_dictionary.items()}
    brand_code_name_dictionary = {code: id_brand_mapping[id] for code, id in brand_code_id_dictionary.items()}
    # Output Dictionaries to file
    with open('output/code_to_id_dict.pkl', 'wb') as file:
        pickle.dump(brand_code_id_dictionary, file)
    with open('output/code_to_name_dict.pkl', 'wb') as file:
        pickle.dump(brand_code_name_dictionary, file)
    with open('output/id_to_code_dict.pkl', 'wb') as file:
        pickle.dump(brand_id_code_dictionary, file)

    # Get user wise details
    user_deets = UserDetails.get_user_purchase_deets(shoppers, brands)
    user_deets = AddUserTags.get_percentile_tags(user_deets)
    # Write user details to file
    WritetoFile.write_df_to_file('output/user_details.txt', user_deets)
    # Get brand wise details
    brand_deets = BrandDetails.get_brand_purchase_deets(shoppers, brands)
    brand_deets = AddBrandTags.add_names(brand_deets, brand_code_name_dictionary)
    brand_deets = AddBrandTags.add_random_categories(brand_deets)
    brand_deets = AddBrandTags.add_random_ordinal_scale(brand_deets)
    brand_deets = AddBrandTags.get_percentile_tags(brand_deets)
    brand_deets = AddBrandTags.first_purchase(brand_deets, shoppers, brands)
    # Write brand_details to file
    WritetoFile.write_df_to_file('output/brand_details.txt', brand_deets)
    # Get copurchase dictionary (this is faster than list. see ProductCopurchase script for details
    copurchase_dictionary = ProductCopurchase.get_copurchase_dictionary(user_deets)
    # Get copurchase matrix from dictionary
    copurchase_matrix = ProductCopurchase.get_product_co_purchase_matrix(copurchase_dictionary,
                                                                         brand_deets["meta"]["size"])
    # Save matrix to file
    np.save("output/copurchase_matrix.npy", copurchase_matrix, allow_pickle=True)


def get_intermediate_files_from_raw_data_timed(filename):
    timestart = time.time()
    (shopping_profile_id, brand_id, id_brand_mapping) = get_data(filename)
    print("Finished reading raw data. Time taken = ", time.time() - timestart)
    # print("data obtained: sample results below:- ")
    # print("first 10 shopper details : ",shopping_profile_id[0:10])
    # print("first 10 brand 1ds: ",brand_id[0:10])
    # print("brand_id_mapping : ",id_brand_mapping[51])
    # print("---------------------")

    (shoppers, shopper_code_dictionary, num_uniq_shoppers, brands, brand_id_code_dictionary, num_uniq_brands) = \
        encode_transactions(shopping_profile_id, brand_id)
    print("Finished encoding data. Time taken = ", time.time() - timestart)
    # print("encoding done: encoded results below:- ")
    # print("first 100 shopper details : ", shoppers[0:100])
    # print("first 100 brand 1ds: ", brands[0:100])
    # print("brand_id_code_mapping[51] : ", brand_id_code_dictionary[51])
    # we need to reverse this dictionary to get the brand id from code
    brand_code_id_dictionary = {code: id for id, code in brand_id_code_dictionary.items()}
    brand_code_name_dictionary = {code: id_brand_mapping[id] for code, id in brand_code_id_dictionary.items()}
    with open('output/code_to_id_dict.pkl', 'wb') as file:
        pickle.dump(brand_code_id_dictionary, file)
    with open('output/code_to_name_dict.pkl', 'wb') as file:
        pickle.dump(brand_code_name_dictionary, file)
    with open('output/id_to_code_dict.pkl', 'wb') as file:
        pickle.dump(brand_id_code_dictionary, file)
    print("Created and saved reverse dictionaries. Time taken = ", time.time() - timestart)

    # print("brand_code_id_mapping[38] : ", brand_code_id_dictionary[38])
    # print("brand_code_name_mapping[38] : ", id_brand_mapping[brand_code_id_dictionary[38]])
    # print("brand_code_name_mapping[38] : ", brand_code_name_dictionary[38])
    # print("---------------------")

    # print("getting brand matrix")
    # # Below is already there in user deets
    # shopper_brand_matrix = UserBrandPurchaseMatrix.get_user_purchase_matrix(shoppers, num_uniq_shoppers, brands, num_uniq_brands)
    # # print("sparse purchase matrix obtained: first row below:- ")
    # # print(shopper_brand_matrix[0])
    # print("Obtained User purchase matrix dictionaries. Time taken = ", time.time() - timestart)

    # print("getting user_wise details")
    user_deets = UserDetails.get_user_purchase_deets(shoppers, brands)
    # print("Add user tags to user details")
    user_deets = AddUserTags.get_percentile_tags(user_deets)
    # print("write userdetails to file")
    print("Obtained User purchase details. Time taken = ", time.time() - timestart)
    WritetoFile.write_df_to_file('output/user_details.txt', user_deets)
    # print("user_deets[meta]")
    # print(user_deets["meta"])
    print("Wrote user purchase details to file. Time taken = ", time.time() - timestart)

    # print("getting brand_wise details")
    brand_deets = BrandDetails.get_brand_purchase_deets(shoppers, brands)
    brand_deets = AddBrandTags.add_names(brand_deets, brand_code_name_dictionary)
    # print("Add brand tags to brand details")
    # Add categories
    brand_deets = AddBrandTags.add_random_categories(brand_deets)
    # Add some ordinal scale
    brand_deets = AddBrandTags.add_random_ordinal_scale(brand_deets)
    # Add percentile tag
    brand_deets = AddBrandTags.get_percentile_tags(brand_deets)
    # Even though it has not been mentioned whether the data has been ordered time-stamp wise, if we assume it has been,
    # we can add a value tag - how many times has this brand been the first purchase of user
    brand_deets = AddBrandTags.first_purchase(brand_deets, shoppers, brands)
    print("Obtained Brand transaction details. Time taken = ", time.time() - timestart)
    # print("write brand_details to file")
    WritetoFile.write_df_to_file('output/brand_details.txt', brand_deets)
    print("Wrote brand purchase details to file. Time taken = ", time.time() - timestart)
    # print("brand_deets[meta]")
    # print(brand_deets["meta"])
    # print("time taken:", time.time() - timestart)

    # import ReadDBFile
    # user_deets = ReadDBFile.read_simple_db("output/user_details.txt")
    # brand_deets = ReadDBFile.read_simple_db("output/brand_details.txt")
    copurchase_dictionary = ProductCopurchase.get_copurchase_dictionary(user_deets)
    print("Got copurchase dict. Time taken = ", time.time() - timestart)
    # print("len(copurchase_list)= ",end="")
    # print(len(copurchase_dictionary.keys()))
    # print("get_copurchase matrix")
    copurchase_matrix = ProductCopurchase.get_product_co_purchase_matrix(copurchase_dictionary,
                                                                         brand_deets["meta"]["size"])
    print("Got copurchase matrix. time taken:", time.time() - timestart)
    np.save("output/copurchase_matrix.npy", copurchase_matrix, allow_pickle=True)
    # np.savetxt("output/copurchase_matrix.txt",copurchase_matrix, delimiter=",", fmt="%6d")
    print("Saved copurchase matrix to file. Time taken = ", time.time() - timestart)



if __name__ == "__main__":
    start_time = time.time()
    get_intermediate_files_from_raw_data("data/brands_filtered.txt")
    print("Finished initiation run. Total time taken : ",time.time() - start_time)









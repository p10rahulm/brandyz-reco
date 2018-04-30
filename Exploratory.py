import Openfile,ConverttoFactor,WriteListtoFile
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

def get_user_purchase_matrix(shoppers,numshoppers, brands,num_brands):
    # numpy zeros is sparse, so size is ok.
    shopper_brand_matrix = np.zeros((numshoppers,num_brands),dtype = np.int8)
    for i in range(len(shoppers)):
        shopper_brand_matrix[shoppers[i],brands[i]]+=1
    return shopper_brand_matrix


def get_user_purchase_deets(shoppers,num_uniq_shoppers,brands):
    # we shall get deets: total_num_transactions, start_row, end_row, brands as a list
    # add more if you find more
    user_deets = []
    end_row = 0
    total_transactions = len(shoppers)
    while end_row < total_transactions:
        num_transactions = 0
        transactions_list = []
        start_row = end_row
        start_user = shoppers[start_row]
        while(end_row < total_transactions and shoppers[end_row] == start_user):
            num_transactions+=1
            transactions_list.append(brands[end_row])
            end_row+=1
        user_deets.append((num_transactions,start_row,end_row,transactions_list))
    return user_deets



def get_copurchase_list(user_details):
    copurchase_list = []
    for user in user_details:
        purchases = user[3]
        i=0
        while i < len(purchases):
            j =i+1
            while j<len(purchases):
                copurchase_list.append((purchases[i],purchases[j]))
                j+=1
            i+=1
    return(copurchase_list)




def get_product_co_purchase_matrix(copurchase_list,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.uint32)
    # i want lower triangular matrix, so switching sides
    for coincidence in copurchase_list:
        brand_copurchase_matrix[coincidence[1],coincidence[0]]+=1
    return brand_copurchase_matrix

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

    '''
    print("getting brand matrix")
    shopper_brand_matrix = get_user_purchase_matrix(shoppers, num_uniq_shoppers, brands, num_uniq_brands)
    print("sparse purchase matrix obtained: first row below:- ")
    print(shopper_brand_matrix[0])
    del shopper_brand_matrix
    '''

    print("getting user_wise details")
    user_deets = get_user_purchase_deets(shoppers, num_uniq_shoppers, brands)
    print("write userdetails to file")
    WriteListtoFile.write_file('output/user_details.txt',user_deets)
    print("user_deets[0:5]")
    print(user_deets[0:5])


    print("get_copurchase list")
    copurchase_list = get_copurchase_list(user_deets)
    print("len(copurchase_list)=",len(copurchase_list))

    print("get_copurchase matrix")
    copurchase_matrix = get_product_co_purchase_matrix(copurchase_list, num_uniq_brands)
    print("save to file")
    np.savetxt("output/copurchase_matrix.csv",copurchase_matrix, delimiter=",", fmt="%6d")

    print("Done! Time taken = ", time.time() - timestart)






# Ran some checks on speed for complete. It is much faster to convert list to dictionary and then add to
# copurchase matrix rather than adding from the list to copurchase matrix one by one.
# Time comparison:
# Starttime =  5.745817184448242
# Got copurchase list. Time taken =  22.694000005722046
# Got copurchase matrix. Time taken =  149.1616563796997
# Got copurchase dict. Time taken =  188.23662972450256
# Got copurchase matrix. Time taken =  196.46579241752625


import numpy as np
import itertools
# from collections import defaultdict
from collections import Counter



def get_copurchase_list(user_df):
    list_of_transactions = user_df["list_of_transactions"]
    copurchase_list = list(itertools.permutations(list_of_transactions[0], 2))
    for i in range(1,len(list_of_transactions)):
        user_transactions = list_of_transactions[i]
        extension = list(itertools.combinations(user_transactions, 2))
        copurchase_list.extend(extension)
    # sorting so it's fast while making further changes
    copurchase_list = sorted(copurchase_list, key=lambda x: x[0])
    return(copurchase_list)


def get_copurchase_dictionary(user_df):
    copurchase_list = get_copurchase_list(user_df)
    copurchase_dictionary = Counter(copurchase_list)
    return(copurchase_dictionary)


'''
# Getting a slightly faster inbuilt method for this, using Counter from collections - see above
def get_copurchase_dictionary(user_df):
    copurchase_list = get_copurchase_list(user_df)
    copurchase_dictionary = defaultdict(int)
    for item in copurchase_list:
        copurchase_dictionary[item]+=1
    return(copurchase_dictionary)
'''

def get_product_co_purchase_matrix(copurchase_dict,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.uint32)
    for xy in copurchase_dict.keys():
        brand_copurchase_matrix[xy[0],xy[1]]+=copurchase_dict[xy]
    brand_copurchase_matrix = brand_copurchase_matrix.T + brand_copurchase_matrix
    return brand_copurchase_matrix


def get_product_co_purchase_matrix_from_list(copurchase_list,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.uint32)
    for xy in copurchase_list:
        brand_copurchase_matrix[xy[0],xy[1]]+=1
    brand_copurchase_matrix = brand_copurchase_matrix.T + brand_copurchase_matrix
    return brand_copurchase_matrix


'''
below is damn slow: again! reworking
def get_copurchase_list_old(user_details):
    copurchase_list = []
    transactions = user_details["list_of_transactions"]
    for user_purchases in transactions:
        i=0
        while i < len(user_purchases):
            j =i+1
            while j<len(user_purchases):
                copurchase_list.append((user_purchases[i],user_purchases[j]))
                j+=1
            i+=1
    return(copurchase_list)
'''

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

'''
#iteration n: below too slow. Reworking
def get_product_co_purchase_matrix_old(copurchase_list,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.uint32)
    for coincidence in copurchase_list:
        # below corresponds to lower triangular matrix, since the copurchase list is sorted such
        # brand_copurchase_matrix[coincidence[1], coincidence[0]] += 1
        # Instead of using that, i can simply use numpy transpose addition.

        # below corresponds to upper triangular matrix
        brand_copurchase_matrix[coincidence[1],coincidence[0]]+=1
    brand_copurchase_matrix = brand_copurchase_matrix.T + brand_copurchase_matrix
    # we get a symmetric matrix
    return brand_copurchase_matrix
'''


if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    from UserDetails import get_user_purchase_deets
    customer_wise_purchase_details = get_user_purchase_deets(customers, purchases)
    coprch_dictionary = get_copurchase_dictionary(customer_wise_purchase_details)
    copurch_matrix = get_product_co_purchase_matrix(coprch_dictionary,len(np.unique(purchases)))
    print("coprch_list = ",coprch_dictionary)
    print("copurch_matrix = ", copurch_matrix)

    # Now for the real stuff
    import ReadDBFile,ProductCopurchase
    import time
    timestart = time.time()
    user_deets = ReadDBFile.read_simple_db("output/user_details.txt")
    brand_df = ReadDBFile.read_simple_db("output/brand_details.txt")
    print("Finished reading. Time taken = ", time.time() - timestart)
    print("get_copurchase list")
    copurchase_list = ProductCopurchase.get_copurchase_list(user_deets)
    print("Got copurchase list. Time taken = ", time.time() - timestart)
    copurchase_matrix = ProductCopurchase.get_product_co_purchase_matrix_from_list(copurchase_list,brand_df["meta"]["size"])
    print("Got copurchase matrix from list. Time taken = ", time.time() - timestart)
    copurchase_dictionary = ProductCopurchase.get_copurchase_dictionary(user_deets)
    print("Got copurchase dict. Time taken = ", time.time() - timestart)
    print("len(copurchase_doct)= ", end="")
    print(len(copurchase_dictionary.keys()))
    print("get_copurchase matrix")
    copurchase_matrix = ProductCopurchase.get_product_co_purchase_matrix(copurchase_dictionary,
                                                                         brand_df["meta"]["size"])

    #
    # print("save to file")
    # np.save("output/copurchase_matrix.npy",copurchase_matrix,allow_pickle=True)
    # np.savetxt("output/copurchase_matrix.txt",copurchase_matrix, delimiter=",", fmt="%6d")

    print("Done! Time taken = ", time.time() - timestart)

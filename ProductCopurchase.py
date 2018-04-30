import numpy as np

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


def get_product_co_purchase_matrix(copurchase_list,num_brands):
    brand_copurchase_matrix = np.zeros((num_brands,num_brands),dtype = np.uint32)
    # i want lower triangular matrix, so switching sides
    for coincidence in copurchase_list:
        brand_copurchase_matrix[coincidence[1],coincidence[0]]+=1
    return brand_copurchase_matrix
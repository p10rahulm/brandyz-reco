import numpy as np

def get_user_purchase_matrix(shoppers,numshoppers, brands,num_brands):
    # numpy zeros is sparse, so size is ok.
    shopper_brand_matrix = np.zeros((numshoppers,num_brands),dtype = np.int8)
    for i in range(len(shoppers)):
        shopper_brand_matrix[shoppers[i],brands[i]]+=1
    return shopper_brand_matrix

if __name__ == "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    print(get_user_purchase_matrix(customers, 3, purchases, 6))
# In this module we will get the brand count and the users per brand as a list.
# Add more details as deemed necessary

# I'm using mergesort here instead of quicksort as the size of data is much larger than for users
import Mergesort
import numpy as np


def get_brand_purchase_deets(shoppers,brands):
    # Going to sort by brands
    brand_shoppers = zip(brands,shoppers)
    brand_shoppers = sorted(brand_shoppers)
    brand_sorted = [brands for brands, shoppers in brand_shoppers]
    shoppers_sorted = [shoppers for brands, shoppers in brand_shoppers]

    # Creating Brand Details
    brand_deets = {}
    brands_list = []
    num_transactions_list = []
    list_of_users = []
    end_row = 0
    total_transactions = len(brands)
    while end_row < total_transactions:
        num_transactions = 0
        users_list = []
        start_row = end_row
        start_brand = brand_sorted[start_row]
        while (end_row < total_transactions and brand_sorted[end_row] == start_brand):
            num_transactions += 1
            users_list.append(shoppers_sorted[end_row])
            end_row += 1
        users_list = Mergesort.mergesorts(users_list)

        # Input into main lists
        brands_list.append(start_brand)
        num_transactions_list.append(num_transactions)
        list_of_users.append(users_list)

    # Add to data frame
    brand_deets["brand_code"] = np.array(brands_list,dtype=np.int32)
    brand_deets["num_transactions"] = np.array(num_transactions_list,dtype=np.int32)
    brand_deets["list_of_users"] = list_of_users
    brand_deets["meta"] = {"size":len(num_transactions_list),
                           "num_columns": 3,
                          "column_type_list": [("brand_code",np.int32),
                                               ("num_transactions",np.int32),
                                               ("list_of_users",list)]}
    return brand_deets

# Below was using list of tuples for storage, now going to convert to dictionary of np.arrays or lists. This could be more R or database style.
def get_brand_purchase_deets_old(shoppers,brands):
    # below we are sorting by brand rather than by shoppers
    brand_shoppers = zip(brands,shoppers)
    brand_shoppers = sorted(brand_shoppers)
    brand_sorted = [brands for brands, shoppers in brand_shoppers]
    shoppers_sorted = [shoppers for brands, shoppers in brand_shoppers]

    # Creating Brand Details
    brand_deets = []
    end_row = 0
    total_transactions = len(brands)
    while end_row < total_transactions:
        num_transactions = 0
        users_list = []
        start_row = end_row
        start_brand = brand_sorted[start_row]
        while (end_row < total_transactions and brand_sorted[end_row] == start_brand):
            num_transactions += 1
            users_list.append(shoppers_sorted[end_row])
            end_row += 1
        users_list = Mergesort.mergesorts(users_list)
        brand_deets.append((start_brand, num_transactions, users_list))
    return brand_deets

if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    print(get_brand_purchase_deets(customers, purchases))
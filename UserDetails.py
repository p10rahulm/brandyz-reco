import Quicksort
import numpy as np
# using quicksort here as it has small overhead and each user only has a small number of transactions


def get_user_purchase_deets(shoppers,brands):
    # we shall get deets: total_num_transactions, start_row, end_row, brands as a list
    # add more deets if you need more

    end_row = 0
    total_transactions = len(shoppers)
    # Initialize
    user_deets = {}
    users_list = []
    num_transactions_list = []
    start_row_list =[]
    end_row_list = []
    list_of_transactions = []

    # Fill in values
    while end_row < total_transactions:
        num_transactions = 0
        transactions_list = []
        start_row = end_row
        start_user = shoppers[start_row]
        while(end_row < total_transactions and shoppers[end_row] == start_user):
            num_transactions+=1
            transactions_list.append(brands[end_row])
            end_row+=1
        Quicksort.quicksort(transactions_list)

        # input values into main lists
        users_list.append(start_user)
        num_transactions_list.append(num_transactions)
        start_row_list.append(start_row)
        end_row_list.append(end_row)
        list_of_transactions.append(transactions_list)


    user_deets["user_id"] = np.array(users_list,dtype = np.int)
    user_deets["num_transactions"] = np.array(num_transactions_list, dtype=np.int16)
    user_deets["start_row"] = np.array(start_row_list, dtype=np.int32)
    user_deets["end_row"] = np.array(end_row_list, dtype=np.int32)
    user_deets["list_of_transactions"] = list_of_transactions
    user_deets["meta"] = {"size": len(num_transactions_list),
                          "num_columns": 5,
                          "column_type_list": [("user_id",np.int),
                                               ("num_transactions",np.int16),
                                               ("start_row",np.int32),
                                               ("end_row",np.int32),
                                               ("list_of_transactions",list)]}

    return user_deets

# Earlier was using row wise storage, converting to columnwise keeping with most databases/R etc.
def get_user_purchase_deets_old(shoppers,brands):
    # we shall get deets: total_num_transactions, start_row, end_row, brands as a list
    # add more deets if you need more
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
        Quicksort.quicksort(transactions_list)
        user_deets.append((start_user,num_transactions,start_row,end_row,transactions_list))
    return user_deets

if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    print(get_user_purchase_deets(customers, purchases))
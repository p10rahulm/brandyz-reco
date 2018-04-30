def get_user_purchase_deets(shoppers,brands):
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
        transactions_list = transactions_list.sort()
        user_deets.append((num_transactions,start_row,end_row,transactions_list))
    return user_deets

if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    print(get_user_purchase_deets(customers, purchases))
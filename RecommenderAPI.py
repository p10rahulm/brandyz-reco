# The following signatures broadly define the API:
#
# 1) Get recommendations for new user
# 2) Get recommendations for front page (alltime hits)
# 3) Get showcase recommendations (top per category)
# 4) Get based on user_id (our encoding)
# 5) Get recommendation based on product
# 6) Get recommendation based on list of products

import ReadDBFile,ProductBasedReco,MultiProductRecos
import numpy as np
import pickle


# Ok first recommendations for new user
def reco_new_user(brand_df):
    names = brand_df["brand_name"]
    codes = brand_df["brand_code"]
    fp = brand_df["first_purchases"]
    recos = [names for first_purchases,codes,names in sorted(zip(fp,codes,names), reverse=True)[0:10]]
    return recos


# Easy one now, all time best for front page
def reco_alltime_best(brand_df):
    names = brand_df["brand_name"]
    codes = brand_df["brand_code"]
    total_transactions = brand_df["num_transactions"]
    recos = [names for total_transactions,codes,names in sorted(zip(total_transactions,codes,names), reverse=True)[0:10]]
    return recos


# Showcase recommendations, top 2 for every category, in order from 0 to 5
def reco_best_of_category(brand_df,category,num_required):
    names = brand_df["brand_name"]
    total_transactions = brand_df["num_transactions"]
    categories = brand_df["category"]
    filtered_zip = zip((total_transactions,categories,names) for (total_transactions,categories,names) in zip(total_transactions,categories,names) if categories == category)
    filtered_sorted = sorted(filtered_zip,reverse=True)[0:num_required]
    recos = [item[0][2] for item in filtered_sorted]
    return recos


def reco_showcase(brand_df):
    list_of_recos = []
    for category in range(5):
        list_of_recos = list_of_recos + reco_best_of_category(brand_df,category,2)
    return list_of_recos

def reco_cp(brand_df, copurchase_matrix, product_id, code_to_name_dict,id_code_dict):
    try:
        product_code = id_code_dict[product_id]
    except:
        print("Please enter valid product id. We couldn't find any product with id: ",product_id)
        return("")
    return(ProductBasedReco.conditional_probability_reco(brand_df, copurchase_matrix, product_code, code_to_name_dict))


def reco_ppm(brand_df, copurchase_matrix, product_id, code_to_name_dict,id_code_dict):
    try:
        product_code = id_code_dict[product_id]
    except:
        print("Please enter valid product id. We couldn't find any product with id: ",product_id)
        return ""
    prod_cop = copurchase_matrix[prod_code]
    arrange = np.arange(len(copurchase_matrix))
    copurchase_ids = [item[1] for item in sorted(zip(prod_cop,arrange),reverse=True)[0:10]]
    # Recommend current product also if product purchases is greater than the least of the num_purchases of the rest 10.
    purchases_number = sorted([brand_df["num_transactions"][id] for id in copurchase_ids])
    current_prodid_number_transactions = brand_df["num_transactions"][prod_code]
    if(current_prodid_number_transactions>=purchases_number[0]):
        top_10_copurchases = [code_to_name[prod_code]]+[code_to_name[item] for item in copurchase_ids[0:9]]
    else:
        top_10_copurchases = [code_to_name[item] for item in copurchase_ids]
    return top_10_copurchases


def reco_copurchase_prob_maximize(brand_df, copurchase_matrix, product_id, code_to_name_dict, id_code_dict, cutoff):
    try:
        product_code = id_code_dict[product_id]
    except:
        print("Please enter valid product id. We couldn't find any product with id: ",product_id)
        return("")
    return(ProductBasedReco.maximal_cooccurance_reco(brand_df, copurchase_matrix, product_code, code_to_name_dict,cutoff))


def reco_conditional_prob_userid(brand_df, user_df,copurchase_matrix, code_to_name_dict, userid_code_dict,user_id):
    try:
        user_code = userid_code_dict[user_id]
    except:
        print("Please enter valid product id. We couldn't find any product with id: ",user_id)
        return("")
    product_list = user_df["list_of_transactions"][user_code]
    return(MultiProductRecos.cp_reco_from_list(brand_df, copurchase_matrix, product_list, code_to_name_dict))


if __name__ == "__main__":
    brand_df = ReadDBFile.read_simple_db("output/brand_details.txt")
    user_df = ReadDBFile.read_simple_db("output/user_details.txt")

    # Load some stuff before the remaining three
    copurchase_matrix = np.load("output/copurchase_matrix.npy")
    with open('output/id_to_code_dict.pkl', 'rb') as file:
        id_code_dict = pickle.loads(file.read())
    with open('output/code_to_name_dict.pkl', 'rb') as file:
        code_to_name_dict = pickle.loads(file.read())
    with open('output/userid_to_code_dict.pkl', 'rb') as file:
        userid_to_code_dict = pickle.loads(file.read())

    print(reco_new_user(brand_df))
    print(reco_alltime_best(brand_df))
    print(reco_showcase(brand_df))
    print(product_based_reco(brand_df,51))

    # The below is a simple conditional probability based recommender
    print(reco_cp(brand_df, copurchase_matrix, 51, code_to_name_dict,id_code_dict))
    # Just to check that for a random product code, the solution is still robust. It still works
    # print(product_based_reco_cp(brand_df, copurchase_matrix, 'a', code_to_name_dict))
    # I recommend below over above bayesian probability accounts for popularity also
    print(reco_ppm(brand_df, copurchase_matrix, 51, code_to_name_dict,id_code_dict))
    # Just to check that for a random product code, the solution is still robust. It works.
    # print(product_based_reco_bayesian(brand_df, copurchase_matrix, 'a', code_to_name_dict))
    print(reco_copurchase_prob_maximize(brand_df, copurchase_matrix, 51, code_to_name_dict,id_code_dict,10))
    print(reco_copurchase_prob_maximize(brand_df, copurchase_matrix, 11, code_to_name_dict,id_code_dict, 10))

    print(reco_conditional_prob_userid(brand_df, user_df,copurchase_matrix, code_to_name_dict, userid_to_code_dict,1))

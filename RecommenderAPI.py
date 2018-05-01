# The following signatures broadly define the API:
#
# 1) Get recommendations for new user
# 2) Get recommendations for front page (alltime hits)
# 3) Get showcase recommendations (top per category)
# 4) Get based on user_id (our encoding)
# 5) Get recommendation based on product
# 6) Get recommendation based on list of products

import ReadDBFile,Mergesort


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


# Get recommendation based on product: Here we will use just the most
def product_based_reco(brand_df,product_id):
    return

if __name__ == "__main__":
    brand_df = ReadDBFile.read_simple_db("output/brand_details.txt")
    print(reco_new_user(brand_df))
    print(reco_alltime_best(brand_df))
    print(reco_showcase(brand_df))
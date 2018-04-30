#
# Here we add tags to the brand - classification and performance based.
# Some of these may be pre-assigned (say by marketing team), some may be updateable (the updation module will have to be separately created).
#
#  With relation to Brands, in the spirit of creating as real-world a scenario as possible, i intend to create:
# (i) categories (which are as of now randomly allocated) -
#       these could be things like books, appliances, etc in the case of an amazon or shoes, ties in case of a clothing retailer
#       As of now, the intention is that if there is a large tendency to select within a category, the same category will be recommended
#       Below I'm going to be using 4 random categories.
#
# (ii) first_purchase_scale (which are as of now randomly allocated).
#       The intention of this is to allocate some ordinal variable so that we can use it to create scores.
#       In real world scenarios, there may be some other ordinal variables like luxury/valueformoney, age_group_appeal, existing user rating, profitability, etc
#       Below I'm going to be using a scale from 1 to 5
#
# (iii) Performance: here i intend to allocate measures such as
#         a) globaltop10
#         b) top_1_percentile
#         c) top_10_percentile
#         d) top_20_percentile
#         e) top_40_percentile
#         f) top_80_percentile
#         g) bottom_20_percentile
#
# (iv) FirstPurchase:
#       Here we will input the number of times this product has been the first purchase of the user.
#

import random,numpy as np
import PercentileTags

def add_random_categories(brand_dataframe):
    out =[]
    for i in range(len(brand_dataframe)):
        rand_cat = random.randint(0,3)
        out.append((brand_dataframe[i][0],brand_dataframe[i][1],rand_cat,brand_dataframe[i][2]))
    return out


def add_random_ordinal_scale(brand_dataframe):
    out =[]
    for i in range(len(brand_dataframe)):
        rand_scale = random.randint(0,4)
        out.append((brand_dataframe[i][0],brand_dataframe[i][1],brand_dataframe[i][2],rand_scale,brand_dataframe[i][3]))
    return out


def get_percentile_tags(brand_dataframe):
    num_brands=len(brand_dataframe)
    brandwise_num_purchases =np.zeros((num_brands,1),dtype = np.int32)
    for i in range(num_brands):
        brandwise_num_purchases[i] = brand_dataframe[i][1]
    percentile_tags = PercentileTags.get_percentiles(brandwise_num_purchases)
    out = []
    for i in range(len(brand_dataframe)):
        out.append((brand_dataframe[i][0], brand_dataframe[i][1], brand_dataframe[i][2], brand_dataframe[i][3], percentile_tags[i], brand_dataframe[i][4]))
    return out

def first_purchase(brand_dataframe,shoppers,brands):

    num_brands=len(brand_dataframe)
    brandwise_num_purchases =np.zeros((num_brands,1),dtype = np.int32)
    for i in range(num_brands):
        brandwise_num_purchases[i] = brand_dataframe[i][1]
    percentile_tags = PercentileTags.get_percentiles(brandwise_num_purchases)
    out = []
    for i in range(len(brand_dataframe)):
        out.append((brand_dataframe[i][0], brand_dataframe[i][1], brand_dataframe[i][2], brand_dataframe[i][3], percentile_tags[i], brand_dataframe[i][4]))
    return out
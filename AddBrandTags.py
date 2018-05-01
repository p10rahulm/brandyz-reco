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
import BrandDetails
import random,numpy as np
import PercentileTags


def add_names(brand_dataframe,code_name_dictionary):
    num_elements = brand_dataframe["meta"]["size"]
    brand_codes = brand_dataframe["brand_code"]
    names = np.empty(num_elements, dtype='U20')
    for i in range(num_elements):
        brand_code = brand_codes[i]
        names[i] = code_name_dictionary[brand_code]
    brand_dataframe["brand_name"] = names
    brand_dataframe["meta"]["num_columns"] += 1
    brand_dataframe["meta"]["column_type_list"].append(("brand_name", 'U20'))
    return brand_dataframe




def add_random_categories(brand_dataframe):
    num_elements = brand_dataframe["meta"]["size"]
    category_list = np.zeros(num_elements,dtype=np.int8)
    for i in range(num_elements):
        category_list[i] = random.randint(0,4)
    brand_dataframe["category"] = category_list
    brand_dataframe["meta"]["num_columns"] += 1
    brand_dataframe["meta"]["column_type_list"].append(("category", 'int8'))
    return brand_dataframe


def add_random_ordinal_scale(brand_dataframe):
    num_elements = brand_dataframe["meta"]["size"]
    ordinal_list = np.zeros(num_elements, dtype=np.int8)
    for i in range(num_elements):
        ordinal_list[i] = random.randint(0, 4)
    brand_dataframe["ordinal_scale"] = ordinal_list
    brand_dataframe["meta"]["num_columns"] += 1
    brand_dataframe["meta"]["column_type_list"].append(("ordinal_scale", 'int8'))
    return brand_dataframe


def get_percentile_tags(brand_dataframe):
    brandwise_num_purchases = brand_dataframe["num_transactions"]
    percentile_tags = PercentileTags.get_percentiles(brandwise_num_purchases)
    brand_dataframe["percentile_tag"] = percentile_tags
    brand_dataframe["meta"]["num_columns"] += 1
    brand_dataframe["meta"]["column_type_list"].append(("percentile_tag", 'int8'))
    return brand_dataframe

def first_purchase(brand_dataframe,shoppers,brands):
    num_brands = brand_dataframe["meta"]["size"]
    brandwise_first_purchases =np.zeros(num_brands,dtype = np.int32)
    # Using the first row as special case
    brandwise_first_purchases[brands[0]] += 1
    # Below gets required in single pass, ie. O(n)
    for i  in range(1,len(shoppers)):
        if(shoppers[i]!=shoppers[i-1]):
            brandwise_first_purchases[brands[i]]+=1
    brand_dataframe["first_purchases"] = brandwise_first_purchases
    brand_dataframe["meta"]["num_columns"]+=1
    brand_dataframe["meta"]["column_type_list"].append(("first_purchases", 'int32'))
    return brand_dataframe

if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    brand_df = BrandDetails.get_brand_purchase_deets(customers, purchases)
    brand_df = add_random_categories(brand_df)
    brand_df = add_random_ordinal_scale(brand_df)
    brand_df = get_percentile_tags(brand_df)
    brand_df = first_purchase(brand_df,customers,purchases)
    print(brand_df)
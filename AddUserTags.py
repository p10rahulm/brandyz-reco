#
# Here we add tags to the user - typically these may contain some demographics like age group and location (rural urban etc) and performance based metrics.
# For now only going with a single performance based metric - percentile.

import PercentileTags,UserDetails
import numpy as np

def get_percentile_tags(user_dataframe):
    userwise_num_purchases =user_dataframe["num_transactions"]
    percentile_tags = PercentileTags.get_percentiles(userwise_num_purchases)
    user_dataframe["percentile_tag"] = percentile_tags
    user_dataframe["meta"]["num_columns"] += 1
    user_dataframe["meta"]["column_type_list"].append(("percentile_tag",np.int8))
    return user_dataframe


if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    user_details = UserDetails.get_user_purchase_deets(customers, purchases)
    user_details = get_percentile_tags(user_details)
    print(user_details)
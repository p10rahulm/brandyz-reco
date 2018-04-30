#
# Here we add tags to the user - typically these may contain some demographics like age group and location (rural urban etc) and performance based metrics.
# For now only going with a single performance based metric - percentile.


import numpy as np
import PercentileTags


def get_percentile_tags(user_dataframe):
    num_users=len(user_dataframe)
    userwise_num_purchases =np.zeros((num_users,1),dtype = np.int32)
    for i in range(num_users):
        userwise_num_purchases[i] = user_dataframe[i][1]
    percentile_tags = PercentileTags.get_percentiles(userwise_num_purchases)
    out = []
    for i in range(num_users):
        out.append((user_dataframe[i][0], user_dataframe[i][1], user_dataframe[i][2], user_dataframe[i][3], percentile_tags[i], user_dataframe[i][4]))
    return out

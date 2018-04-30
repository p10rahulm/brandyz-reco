# This is used to measure performance. The standard tags we'll use are
#         a) globaltop10
#         b) top_1_percentile
#         c) top_10_percentile
#         d) top_20_percentile
#         e) top_40_percentile
#         f) top_80_percentile
#         g) bottom_20_percentile
import Mergesort
import numpy as np

def get_percentiles(input_list):
    num_in_list = len(input_list)
    ordered_list = Mergesort.mergesorts(input_list)
    top10 = ordered_list[len(ordered_list)-10]
    percentile99 = ordered_list[int(0.99*num_in_list)]
    percentile90 = ordered_list[int(0.9 * num_in_list)]
    percentile80 = ordered_list[int(0.8 * num_in_list)]
    percentile60 = ordered_list[int(0.6 * num_in_list)]
    percentile20 = ordered_list[int(0.2 * num_in_list)]
    percentile_tags = np.zeros(num_in_list,dtype=np.int8)
    for i in range(num_in_list):
        current = input_list[i]
        if(current<percentile20):
            # no need to add curr_out to  out-list because outlist already initialized to 0
            continue
        if (current < percentile60):
            percentile_tags[i]=1
            continue
        if (current < percentile80):
            percentile_tags[i]=2
            continue
        if (current < percentile90):
            percentile_tags[i]=3
            continue
        if (current < percentile99):
            percentile_tags[i]=4
            continue
        if (current < top10):
            percentile_tags[i]=5
            continue
        if (current > top10):
            percentile_tags[i]=6

    return percentile_tags


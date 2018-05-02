# Here ideally we may be able to use powerful models. The efficacy of these cannot be tested due to paucity of time.
# We will be using the bayesian system here as well
# 1) Conditional probability based system:
#       We want to find P(A | E1, E2, E3 ...)
#
#       Now we can substitute co-occurance of E1, E2, E3, etc with E
#       Then the question boils down to  P(A | E)
#
#       As seen before, this is given by the conditional probability
#       P(A | E) = P(A ∩ E)/(P(E)
#       Now if we substitute back
#       E = E1 ∩ E2 ∩ E3 ...
#
#       P(A | E) = P(A ∩ E1 ∩ E2 ∩ E3 ...)/(P(E1 ∩ E2 ∩ E3 ...)
#       The denominator is constant, so all we need is the intersection
#       P(A | E) ∝ P(A ∩ E1 ∩ E2 ∩ E3 ...)
#
#       Thus the problem boils down to finding the intersection.
#       By the includsion exclusion principle: https://en.wikipedia.org/wiki/Inclusion–exclusion_principle
#       We can say that Union(Ai) = Sum((-1)^k * Intersection(Ai..Ai+k))
#       Please see given link for more clarity on this.
#
#       Let's take 3 elements - or two conditions, E1 and E2. Here we get
#       P(A | E) ∝ P(A ∪ E1 ∪ E2) - (P(A) + P(E1) + P(E2)) + P(A ∩ E1) + P(E1 ∩ E2) + P(A ∩ E2)
#
#       Gethering only A related terms
#       P(A | E) ∝ P(A ∪ E1 ∪ E2) - P(A) + P(A ∩ E1) + P(A ∩ E2)
#
#       Similarly, we can calculate for 4 elements (Note to self: please check below later)
#       P(A | E) ∝ +P(A ∪ E1 ∪ E2 ∪ E3) - (P(A)) + (P(A ∩ E1) + P(A ∩ E2) + P(A ∩ E3)) -
#                       (P(A ∩ E1 ∩ E2) + P(A ∩ E1 ∩ E3) + P(A ∩ E2 ∩ E3))
#
#       Asymptotically, we can say that the terms that are intersections of greater number of events are much less
#       likely, and therefore we can at a small risk ignore them.
#
#       Further, we can presume that the probability of the union of four events minus the prob of the events
#       tends to 0
#
#       Thus we are left with
#       P(A | E) ∝ (P(A ∩ E1) + P(A ∩ E2) + P(A ∩ E3))
#
#       Thus we can take the sum of the probabilities given by our conditional probability method and that should be
#       a fairly robust answer
#

import numpy as np


# Get recommendation based on product: This is based on (1) above
def conditional_probability_reco_from_list(brand_df, copurchase_matrix, product_code_list, code_to_name_dict):
    overall_copurch_sum = np.zeros(brand_df["meta"]["size"],dtype = np.float)
    for product_code in product_code_list:
        num_transactions = brand_df["num_transactions"][product_code]
        prod_copurchase = np.copy(copurchase_matrix[product_code])
        prod_copurchase[product_code] = num_transactions
        prod_copurchase = prod_copurchase/num_transactions
        overall_copurch_sum = overall_copurch_sum + prod_copurchase
    codes = np.arange(len(copurchase_matrix))
    top_10_copurchases = [code_to_name_dict[item[1]] for item in sorted(zip(overall_copurch_sum,codes),reverse=True)[0:10]]
    return (top_10_copurchases)

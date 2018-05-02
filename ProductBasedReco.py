# Here we will get the recoommendations based on a single product.
# The idea is to use a bayesian system. Bayesian should work well as this is a single dependancy
# 1) Conditional probability based system:
#       P(A | B) = P(A ∩ B)/(P(B)
#
#       If we know that the product B has been purchased, what is the probability A will be purchased.
#       Under this definition, we have that the probability
#       is equal to the number of times both have been purchased together/ number of times B has been purchased.
#
#       Therefore,
#       P(A|B) = copurchase(A with B)/num_transactions(B)
#
#       Since num_transactions(B) is constant, we can just say
#       P(Ai|B) ∝ copurchase(Ai with B)
#
#       Once we calculate this for various A, we can line them up by descending order and output results.
#       Note that by definition, B itself will have a result of 1 and be the highest.
#
#
# 2) Maximise overall purchase probability given purchase of product:
#       Here we modify overall purchase probability of products based on the purchase of B.
#
#       P(A | B) * P(A) = P(A) * (P(B | A) * P(A)/(P(B))
#       =>
#       P(A1 | B) = P(A) *(P(B | A1) * P(A1)) / ((P(B | A1) * P(A1)) + (P(B | A2) * P(A2)) + (P(B | A3) * P(A3)) +  ...)
#
#       Since the denominator is common for all such Ai, we can calculate outcome proportional to P(B ∩ Ai) * P(Ai)
#
#       Therefore,
#       P(Ai|B) * P(A) ∝ copurchase(Ai with B)*num_transactions(Ai)
#
#       Once we calculate this for various Ai, we can line them up by descending order and output results.
#       Note that here, B need not be the largest
#       Further note that to take into account the fact that in some cases, the copurchase weight may be 0,
#       we can add some small residual to give more balanced results
#
#
# 3) Maximize copurchase probability - maximize probability of tail products being purchased:
#       Here instead of the question, what are the products Ai maximised by the purchase of B,
#       we ask the question what are the products Ai which maximize the percentage probability of purchase of B
#
#       ie. we maximize
#       P(B | Ai) = P(Ai ∩ B)/(P(Ai)
#
#       Therefore, we maximize
#       P(B | Ai) ∝ copurchase(Ai with B)/num_transactions(Ai)
#
#       Once we calculate this for various Ai, we can line them up by descending order and output results.
#       Note that here, B need not be the largest


import numpy as np


# Get recommendation based on product: This is based on (1) above
def conditional_probability_reco(brand_df, copurchase_matrix, product_code, code_to_name_dict):
    num_transactions = brand_df["num_transactions"][product_code]
    prod_copurchase = np.copy(copurchase_matrix[product_code])
    prod_copurchase[product_code] = num_transactions
    codes = np.arange(len(copurchase_matrix))
    top_10_copurchases = [code_to_name_dict[item[1]] for item in sorted(zip(prod_copurchase,codes),reverse=True)[0:10]]
    return (top_10_copurchases)


# Get recommendation based on purchase probability maximization: This is based on (2) above
def purchase_prob_maximization_reco(brand_df, copurchase_matrix, product_code, code_to_name_dict):
    num_transactions = brand_df["num_transactions"]
    num_current_transactions = num_transactions[product_code]
    prod_copurchase_probability = np.copy(copurchase_matrix[product_code])
    prod_copurchase_probability[product_code] = num_current_transactions
    residual = 1/len(num_transactions)
    prod_copurchase_probability =prod_copurchase_probability + residual
    # below not required as doesn't change outcomes. Same as denominator being same over all products
    # prod_copurchase_probability = prod_copurchase_probability/num_current_transactions
    prod_copurchase_probability = num_transactions*prod_copurchase_probability
    # codes below gives an index over which to sort.
    codes = np.arange(len(copurchase_matrix))
    top_10_copurchases = [code_to_name_dict[item[1]] for item in sorted(zip(prod_copurchase_probability,codes),reverse=True)[0:10]]
    return (top_10_copurchases)


# Get recommendation based on maximal cooccurence of product purchase: This is based on (3) above
def maximal_cooccurance_reco(brand_df, copurchase_matrix, product_code, code_to_name_dict,cutoff):
    num_transactions = brand_df["num_transactions"]
    num_current_transactions = num_transactions[product_code]
    # Reworking cutoff for really small transaction sizes
    cutoff = min(cutoff,int(num_current_transactions/10))
    prod_copurchase_probability = np.copy(copurchase_matrix[product_code])
    prod_copurchase_probability[product_code] = num_current_transactions
    # prod_copurchase_probability = np.where(prod_copurchase_probability < cutoff, 0, prod_copurchase_probability)
    prod_copurchase_probability[np.where(prod_copurchase_probability < cutoff) or np.where(prod_copurchase_probability ==num_current_transactions)] = 0
    prod_copurchase_probability = prod_copurchase_probability/num_transactions
    # codes below gives an index over which to sort.
    codes = np.arange(len(copurchase_matrix))
    top_10_copurchases = [code_to_name_dict[item[1]] for item in sorted(zip(prod_copurchase_probability,codes),reverse=True)[0:10]]
    return (top_10_copurchases)
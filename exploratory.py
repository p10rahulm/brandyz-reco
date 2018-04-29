import openfile,numpy as np

def get_data(filename):
    brands_preference_lines = openfile.openfile_returnlist(filename)
    (shopping_profile_id, brand_id, id_brand_mapping) = openfile.data_operations(brands_preference_lines)
    return (shopping_profile_id, brand_id, id_brand_mapping)

# def get_user_purchase_matrix(shopping_profile_id, brand_id):


# def get_product_co_purchase_matrix(shopping_profile_id, brand_id):


if __name__ == "__main__":
    (shopping_profile_id, brand_id, id_brand_mapping) = get_data("data/brands_filtered.txt")
    print(shopping_profile_id[0:100])
    print(brand_id[0:100])
    print(id_brand_mapping[51])
    print(len(np.unique(shopping_profile_id)))
    print(len(np.unique(brand_id)))

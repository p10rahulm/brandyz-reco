
def write_list_to_file(filename,outlist):
    outfile = open(filename, 'w')
    for list_item in outlist:
        outfile.write(str(list_item))
        outfile.write('\n')
    outfile.close()


def write_df_to_file(filename,data_container):
    outfile = open(filename, 'w')
    filelen = data_container["meta"]["size"]
    num_cols = data_container["meta"]["num_columns"]
    col_names = []
    print("size:",filelen, file=outfile)
    print("columns:", num_cols, file=outfile)
    print("--columns--", file=outfile)
    for item in data_container["meta"]["column_type_list"]:
        key, value = item
        col_names.append(key)
        print(key,",",value,file=outfile,sep="")
    columns = []
    for col_name in col_names:
        columns.append(data_container[col_name])
    print("--data--", file=outfile)
    for i in range(filelen):
        for j in range(num_cols):
            print(columns[j][i],file=outfile, end="")
            if(j!=num_cols-1):
                print(",",file=outfile, end="")
        print("",file=outfile)
    outfile.close()

if __name__== "__main__":
    customers = [0,0,1,1,1,2,2,2,2]
    purchases = [0,3,5,1,2,4,1,3,5]
    import UserDetails
    user_details = UserDetails.get_user_purchase_deets(customers, purchases)
    write_df_to_file("output/writedf_test.txt",user_details)
    import BrandDetails,AddBrandTags
    brand_details = BrandDetails.get_brand_purchase_deets(customers, purchases)
    brand_details = AddBrandTags.add_random_categories(brand_details)
    brand_details = AddBrandTags.add_random_ordinal_scale(brand_details)
    brand_details = AddBrandTags.get_percentile_tags(brand_details)
    brand_details = AddBrandTags.first_purchase(brand_details,customers,purchases)
    write_df_to_file("output/writebrand_df_test.txt", brand_details)

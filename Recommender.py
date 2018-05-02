# Here we create a scaffolding for the Recommender API.
# It will loop till the user exits.
# The choices for the user will be:
# 1) Get new user recommendations
# 2) Get front page recommendations
# 3) Get showcase recommendations
# 4) Get "You might also like" recommendations below product:
#       Enter (i) product_id
# 5) Get similar Products carousel recommendations below product:
#       Enter (i) product_id
# 6) Get email or front page recommendations for purchaser of single product:
#       Enter (i) product_id
# 7) Get multiple product based recommendations
#       Enter product ids separated by enter
# 8) Get user based recommendations
#       Enter user id, then products purchased are retrieved

import ReadDBFile,RecommenderAPI,MultiProductBasedRecommendations
import numpy as np,pickle


def get_overall_recommendation(choice,brand_df):
    if(choice==1):
        print("\nThe recommendations for a new user are:")
        recolist = RecommenderAPI.reco_new_user(brand_df)
        for i in range(len(recolist)):
            print(recolist[i],end="")
            if(i != len(recolist)-1):
                print(",",end="")
        print()
    if(choice==2):
        print("\nThe alltime best recommendations for front page are:")
        recolist = RecommenderAPI.reco_alltime_best(brand_df)
        for i in range(len(recolist)):
            print(recolist[i],end="")
            if(i != len(recolist)-1):
                print(",",end="")
        print()
    if(choice==3):
        print("\nThe showcase recommendations for someone you want to try something new are: ")
        recolist = RecommenderAPI.reco_showcase(brand_df)
        for i in range(len(recolist)):
            print(recolist[i],end="")
            if(i != len(recolist)-1):
                print(",",end="")
        print()


def get_product_recommendations(choice,brand_df,copurchase_matrix,code_to_name_dict,id_code_dict):
    product_id = input("Please enter a product ID: ")
    try:
        product_id = int(product_id)
    except:
        print("Please enter valid product id. We couldn't find any product with id: ", product_id)
        return
    if(choice == 4):
        recolist = RecommenderAPI.reco_cp(brand_df, copurchase_matrix, product_id, code_to_name_dict, id_code_dict)
        if(recolist!=""):
            print("\nThe recommendations for a 'You might also like' carousel below product are:")
            for i in range(len(recolist)):
                print(recolist[i],end="")
                if(i != len(recolist)-1):
                    print(",",end="")
    if (choice == 5):
        recolist = RecommenderAPI.reco_copurchase_prob_maximize(brand_df, copurchase_matrix, product_id, code_to_name_dict, id_code_dict,10)
        if (recolist != ""):
            print("\nSimilar products carousel below product can contain:")
            for i in range(len(recolist)):
                print(recolist[i], end="")
                if (i != len(recolist) - 1):
                    print(",", end="")
    if (choice == 6):
        recolist = RecommenderAPI.reco_ppm(brand_df, copurchase_matrix, product_id, code_to_name_dict, id_code_dict)
        if (recolist != ""):
            print("\nPopular products based on the purchase for email and marketing campaigns are:")
            for i in range(len(recolist)):
                print(recolist[i], end="")
                if (i != len(recolist) - 1):
                    print(",", end="")


def get_product_recommendations_by_userid(choice,brand_df,user_df,copurchase_matrix,code_to_name_dict,userid_to_code_dict):
    user_id = input("Please enter a user id: ")
    try:
        user_id = int(user_id)
    except:
        print("Please enter valid user id. We couldn't find any user with id: ", user_id)
        return
    if(choice == 8):
        recolist = RecommenderAPI.reco_conditional_prob_userid(brand_df, user_df,copurchase_matrix, code_to_name_dict, userid_to_code_dict,user_id)
        if(recolist!=""):
            print("\nThe recommendations for user id ",user_id," are:")
            for i in range(len(recolist)):
                print(recolist[i],end="")
                if(i != len(recolist)-1):
                    print(",",end="")


def get_recommendations_from_product_list(choice,brand_df,copurchase_matrix,code_to_name_dict,id_code_dict):
    getting_list = True
    product_list = []
    while(getting_list):
        product_id = input("Please enter a product ID or press q if done: ")
        if product_id=='q':
            break;
        try:
            product_id = int(product_id)
            product_code = id_code_dict[product_id]
            product_list.append(product_code)
        except:
            print("Please enter valid product id. We couldn't find any product with id: ", product_id)

    # print(product_list)
    if(len(product_list)==0):
        print("Please enter atleast one product")
        return

    recolist = MultiProductBasedRecommendations.conditional_probability_reco_from_list(brand_df, copurchase_matrix, product_list, code_to_name_dict)
    if(recolist!=""):
        print("\nThe recommendations based on your product list are:")
        for i in range(len(recolist)):
            print(recolist[i],end="")
            if(i != len(recolist)-1):
                print(",",end="")


def recommender():
    # Initialize Loads
    brand_df = ReadDBFile.read_simple_db("output/brand_details.txt")
    user_df = ReadDBFile.read_simple_db("output/user_details.txt")
    copurchase_matrix = np.load("output/copurchase_matrix.npy")
    with open('output/id_to_code_dict.pkl', 'rb') as file:
        id_code_dict = pickle.loads(file.read())
    with open('output/code_to_name_dict.pkl', 'rb') as file:
        code_to_name_dict = pickle.loads(file.read())
    with open('output/userid_to_code_dict.pkl', 'rb') as file:
        userid_to_code_dict = pickle.loads(file.read())

    # Start the recommender
    exit_bool = False
    while not exit_bool:
        print("1. Get new user recommendations")
        print("2. Get front page recommendations")
        print("3. Get showcase recommendations")
        print("4. Get 'You might also like' recommendations below product")
        print("5. Get 'View similar products' carousel recommendations below product")
        print("6. Get email or front page recommendations for purchaser of single product")
        print("7. Get multiple product based recommendations")
        print("8. Get user_id based recommendations")
        print("9. Exit")
        choice = input("Enter an option between 1 and 9: ")
        wrongchoice = False
        try:
            choice = int(choice)
        except:
            wrongchoice= True
        if(not wrongchoice):
            if(choice>=1 and choice <= 3):
                get_overall_recommendation(choice,brand_df)
            if (choice >= 4 and choice <= 6):
                get_product_recommendations(choice, brand_df, copurchase_matrix, code_to_name_dict,id_code_dict)
            if (choice ==7):
                get_recommendations_from_product_list(choice,brand_df,copurchase_matrix,code_to_name_dict,id_code_dict)
            if (choice ==8):
                get_product_recommendations_by_userid(choice, brand_df, user_df, copurchase_matrix, code_to_name_dict,userid_to_code_dict)
            if(choice==9):
                print("Thank you for using the Brandyz Recommender!")
                exit_bool = True
            else: wrongchoice = True
        if wrongchoice:
            print("\n\nPlease reinput a number between 1 and 9")
        else:
            print("\n")



if __name__=="__main__":
    recommender()


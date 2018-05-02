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

import ReadDBFile,RecommenderAPI
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

def recommender():
    # Initialize Loads
    brand_df = ReadDBFile.read_simple_db("output/brand_details.txt")
    copurchase_matrix = np.load("output/copurchase_matrix.npy")
    with open('output/id_to_code_dict.pkl', 'rb') as file:
        id_code_dict = pickle.loads(file.read())
    with open('output/code_to_name_dict.pkl', 'rb') as file:
        code_to_name_dict = pickle.loads(file.read())

    # Start the recommender
    exit_bool = False
    while not exit_bool:
        print("1. Get new user recommendations")
        print("2. Get front page recommendations")
        print("3. Get showcase recommendations")
        print("4. Get 'You might also like' recommendations below product")
        print("5. Get similar Products carousel recommendations below product")
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
                print("in first")
                get_overall_recommendation(choice,brand_df)
            if (choice >= 4 and choice <= 6):
                print("in second")
                get_product_recommendations(choice, brand_df, copurchase_matrix, code_to_name_dict,id_code_dict)
            if(choice==9):
                print("Thank you for checking this file!")
                exit_bool = True
            else: wrongchoice = True
        if wrongchoice:
            print("\n\nPlease reinput a number between 1 and 9")
        else:
            print("\n")



if __name__=="__main__":
    recommender()


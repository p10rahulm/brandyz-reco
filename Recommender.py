# Here we create a scaffolding for the Recommender API.
# It will loop till the user exits.
# The choices for the user will be:
# 1) Get new user recommendations
# 2) Get front page recommendations
# 3) Get showcase recommendations
# 4) Get Product based recommendations:
#       Enter (i) product_id
# 5) Get multiple product based recommendations
#       Enter product ids separated by enter
# 6) Get user based recommendations
#       Enter user id, then products purchased are retrieved

import ReadDBFile,RecommenderAPI


def get_recommendation(choice,brand_df):
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
    if(choice==7):
        print("Thank you for checking this file!")



def recommender():
    brand_df = ReadDBFile.read_simple_db("output/brand_details.txt")
    exit_bool = False
    while not exit_bool:
        print("1. Get new user recommendations")
        print("2. Get front page recommendations")
        print("3. Get showcase recommendations")
        print("4. Get single product based recommendations")
        print("5. Get multiple product based recommendations")
        print("6. Get user_id based recommendations")
        print("7. Exit")
        choice = input("Enter an option between 1 and 7: ")
        wrongchoice = False
        try:
            choice = int(choice)
        except:
            wrongchoice= True
        if(not wrongchoice):
        # if(isinstance(choice, int)):
            if(choice>0 and choice < 8):
                print("in")
                get_recommendation(choice,brand_df)
                if(choice==7):
                    exit_bool = True
            else: wrongchoice = True
        if wrongchoice:
            print("\n\nPlease reinput a number between 1 and 7")
        else:
            print("\n")



if __name__=="__main__":
    recommender()


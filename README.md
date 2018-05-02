# Brandyz Recommender

A recommender system using transaction details of brand id and user id written in Python.

## Getting Started

This is a general purpose simple recommendation system for getting product based and user based recommendations. 
It has been tested on a fashion dataset that contains data on user ids and user purchases of various fasion brands.

The following instructions will get you a copy of the project up and running on your local machine.

### Pre Requisites

- We recommend a system with atleast 8GB of Ram in order to run this project smoothly. 
- Ideally you could run this on a development system that can run unix commands like sed and tail.
- If you are on windows, these tools can be downloaded from: 
		(a) [Sed Tool](https://github.com/mbuilov/sed-windows/blob/master/sed-4.4-x64.exe) 
		(b) [Unix Utilities](https://sourceforge.net/projects/unxutils)

### How to setup

There are three main files that you need to run in order to set this up on your system.

- First run ExtractData.sh. Post running this, you should see an additional txt file in the data folder
```
$> ExtractData.sh
```

- Then do the initial setup to get all the requisite files in place. 
```
$> python InitializeRecoEngine.py
```
- This above step may take about 5 minutes, go grab a coffee or soup

- You are now ready to go. To test the system run the recommender.py file
```
$> python Recommender.py
```

## Examples:
The main choices for the user will be:
1) Get new user recommendations
2) Get front page recommendations
3) Get showcase recommendations
4) Get "You might also like" recommendations below product:
      Enter (i) product_id
5) Get similar Products carousel recommendations below product:
      Enter (i) product_id
6) Get email or front page recommendations for purchaser of single product:
      Enter (i) product_id
7) Get multiple product based recommendations
      Enter product ids separated by enter
8) Get user based recommendations
      Enter user id, then products purchased are retrieved

## Running Tests

- Each file comes with its own test. For example, if you run the RecommenderAPI  module on it's own, it would run a simple test
```
$> python RecommenderAPI.py
```

## Details

- The system has been built to be as general as possible. While the recommendation engine can be changed the scaffolding is good to handle that change.
- We have used our own data structure to store data. While this may be less efficient than say using a binary format, it is inline with data storage formats of some databases and languages like R
- In some cases, instead of using Python's inbuilt sorting tools, we have used Quicksort (for smaller lists) and Mergesort (for larger lists)
- This program has almost fully been written in Python. The only place where we have used external tools is in the SedOperations file. This is for speed of string operatiosn. 
- Note: Above file may have OS dependencies. It shoudl work for linux systems and for windows if sed.exe and tail.exe are in PATH.
- The recommendation itself has been done using bayesian methods. The explanation for these is in the ProductBasedReco and MultiProductRecos files
- For testing in more general cases, we have created certain random categories, ordinal scales and first-purchase data. While these have not been used in product recos as of now, in case of availability of real data on these they can be used
- Once the initial setup is done, any additional brand or user can be added through the AddNewUser and AddNewBrand APIs without paying the computational cost of the entire run.
- The product co-purchase matrix may be obtained/updated through batch runs.




## Built With

* [Python 3.6](https://www.python.org/doc/)
* [Sed](https://github.com/mbuilov/sed-windows/blob/master/sed-4.4-x64.exe) - Used for some text editing
* [Gnu Utils](https://sourceforge.net/projects/unxutils) - Utilities like tail for windows
* [Numpy](https://docs.scipy.org/doc/numpy-1.13.0/reference/) - Main math utility used

## Authors

* **Rahul Madhavan** - *[CodeFRA]*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to the world at large and specifically stackoverflow

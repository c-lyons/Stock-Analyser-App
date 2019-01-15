# get_stock_info.py
from all_imports import pd
import menus

# The following are lists of keywords which are used to check user input
yesWords = ['y', 'yes', 'ok', 'ye', 'yup', 'sure']
noWords = ['n', 'no', 'nope']
backWords = ['back', 'b', 'bac', 'go back']
quitWords = ['quit', 'q', 'close', 'exit']
mainWords = ['main menu', 'main', 'home', 'mainmenu']

# loading stock ticker data upon opening of application
stock_tickers = pd.read_csv('http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchan0ge=nasdaq&render=download')
# Set Ticker Symbols to Index for easier retrieval
stock_tickers.set_index('Symbol',inplace=True)
# create new column "Name Lower" for easier name search using lower case input
stock_tickers['Name Lower'] = stock_tickers['Name'].str.lower()


def get_ticker():
    """this function checks if a ticker is valid and gets stock from stock_tickers dataframe"""
    ticker = input("""
To view more information about a stock please enter stock TICKER:\n(or hit RETURN to go back...)\n""")

    if len(ticker) > 0: # if some value entered for ticker (i.e. not RETURN) print ticker info
        if ticker.upper() in stock_tickers.index: # if ticker found in stock_tickers.index

            ticker_info = stock_tickers.loc[ticker.upper()] # creating temp object to store ticker info
            # dropping unwanted columns for clean printing to user
            ticker_info = ticker_info.drop('Name Lower')
            ticker_info = ticker_info.drop('Unnamed: 8')
            user_in = input("Ticker {} found. This ticker is for {}. Would you like to continue? (Y/N)".format(ticker.upper(),ticker_info[0]))

            if user_in.lower() in yesWords:  # is user selects yes
                menus.menu_3(ticker, ticker_info)

            elif user_in.lower() in noWords:  # if user selects no
                menus.menu_2()

            elif user_in.lower() in backWords:  # if user selects back
                menus.menu_2()

            elif user_in.lower() in quitWords:  # if user selects quit
                print("Goodbye!")
                exit()
            else:
                print("That is not a valid query. Please try again!")
                get_ticker()

        else:
            print('\nSorry, that ticker was not found! Please try another query, or search for a stock by name.\n')
            menus.menu_2()
    else:
        # else if RETURN entered, go back to previous menu
        menus.menu_2()

def print_ticker(ticker, ticker_info):
    """ This function """
    print("\nOverview for {} ({})\n".format(ticker_info[0],ticker.upper()))
    print("*" * 40)
    print("\n", ticker_info, "\n")
    print("*" * 40)
    user_in2 = input("\nEnter 'Back' to return to the previous menu, or enter 'Quit' to exit.\n").lower()
    if user_in2.lower() in backWords:
        menus.menu_3(ticker, ticker_info)  # return to previous menu
    elif user_in2.lower in quitWords:
        print('Goodbye!')
        exit()  # close application
    else:
        print("\nI'm sorry. That is not a valid query. Please try again!\n")
        menus.menu_3(ticker, ticker_info)

def find_name():
    """ This function finds a lower case string input using .contain() method and returns all entries with string"""

    user_in = input('Please enter the search term below:\n')
    # calling rows where user_in2 found in stock_tickers['Name Lower'] and converting type series to string for retrieval
    if len(stock_tickers[stock_tickers['Name Lower'].str.contains(user_in.lower())]) > 0:
        print("\nYour search '{}' returned the following queries...\n".format(user_in))
        stock_temp = stock_tickers[stock_tickers['Name Lower'].str.contains(user_in.lower())] # temp file for printing
        # stock_temp = stock_temp.drop('Name Lower', axis=1) # removing "Name Lower" column so does not print
        # stock_temp = stock_temp.drop('Unnamed: 8', axis=1) # removing "Unnamed:  8" column so does not print
        print(stock_temp['Name'])
        get_ticker()
    else:
        print("Sorry, your search returned no queries. Please try a searching a different query.")
        menus.menu_2()

def load_ticker(ticker, ticker_info):
    """ This function pulls stock information for specified ticker"""
    # pulling data from alphavantage.com using time series adjusted daily values
    # API Key = SVXDA7FAELA4RSD0
    # data type = csv
    # file size = "full" (up to 20 years of data - varies with stock choice)
    # Time Series Daily Adjusted Figures

    print("Loading Stock Data...\n")  # loading message while downloading data

    # loading stock from www.alphavantage.co
    loaded_stock = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey=SVXDA7FAELA4RSD0&datatype=csv'.format(ticker))

    # setting timestamp column as index for easier retrieval
    loaded_stock.set_index('timestamp', inplace=True)

    # adding percentage change of close price to df, converting to percentage and rounding to 2 decimal places
    loaded_stock['% Change'] = round(loaded_stock['adjusted_close'].pct_change()*100,2)

    # checking if stock download was successful
    if len(loaded_stock) > 2:
        # checking if loaded_stock dataframe has successfully downloaded. (Unsuccessful download has len = 2)
        print("{} Stock Data Loaded Successfully!\n".format(ticker.upper()))
        menus.menu_4(loaded_stock, ticker, ticker_info)
    else:
        # if unsuccessfull print error and returns to previous menu
        print("Error. Could not retrieve stock data. Please try again.")
        menus.menu_3(ticker, ticker_info)




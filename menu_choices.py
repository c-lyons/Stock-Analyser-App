# menu_choices

import menus, get_stock_info, stock_plot # importing other referenced modules

# The following are lists of keywords which are used to check user input
yesWords = ['y', 'yes', 'ok', 'ye', 'yup', 'sure']
noWords = ['n', 'no', 'nope']
backWords = ['back', 'b', 'bac', 'go back']
quitWords = ['quit', 'q', 'close', 'exit']
mainWords = ['main menu', 'main', 'home', 'mainmenu']

def menu_1_choose(user_in):
    """This function processes the user selection from the main menu"""

    exploreWords = ['1','stock','explore','info','explore stock','explorestock'] # words for user input for option 1

    # checking user input and corresponding action
    if user_in.lower() in exploreWords:
        # if user selects 1 launch menu_2() function
        menus.menu_2()
    elif user_in == '2' or user_in.lower() in quitWords:
        # if user selects 3, exit app
        print('Goodbye!')
    else:
        print('That is not a valid query! \nPlease try again or enter "Quit" to exit.\n')
        menus.main_prompt()


def menu_2_choose(user_choice):
    """ processing user input from search menu"""
    if user_choice.lower() in ['1', 'ticker', 'search ticker', 'tick', 'searchticker']:
        # open get_ticker function
        get_stock_info.get_ticker() # if option 1, open get_tciker()
    elif user_choice.lower() in ['2', 'name', 'search name','searchname']:
        # open find_name function
        get_stock_info.find_name()
    elif user_choice == "3" or user_choice.lower() in backWords:
        # back to main menu
        menus.main_prompt()
    elif user_choice == "4" or user_choice.lower() in quitWords:
        # exit application
        print("Goodbye!")
        exit()
    else:
        # print in case of any other query
        print('Please enter a valid query!\n')
        menus.menu_2()


def menu_3_choose(ticker, ticker_info, user_in):
    """ processing user input for menu 3"""

    # creating lists to check user input words
    stockover_words  = ['1', 'overview', 'stock overview', 'view stock']
    timeseries_words = ['2', 'time', 'time series', 'time-series', 'stock time', 'time series analysis']

    # checking user input vs input lists and performing corresponding action
    if user_in.lower() in stockover_words:
        get_stock_info.print_ticker(ticker, ticker_info)

    elif user_in.lower() in timeseries_words:
        get_stock_info.load_ticker(ticker, ticker_info)

    elif user_in == "3" or user_in.lower() in backWords:
        menus.menu_2()

    elif user_in == "4" or user_in.lower() in mainWords:
        menus.main_prompt()

    elif user_in == "5" or user_in.lower() in quitWords:
        print("Goodbye!")
        exit()
    else:
        print("That is not a valid query. Please try again.")
        menus.menu_3(ticker, ticker_info)

def menu_4_choose(loaded_stock, ticker, user_in, ticker_info):
    """ processing user input for menu 4 """

    # defining lists for processing user input
    stockdescr_words = ['1', 'descriptive', ' descriptive analysis','descr', 'description']
    stockpred_words  = ['2', 'predict', 'prediction', 'predictive', 'predictive analysis', 'pred']

    # checking user input and caryying out corresponding action
    if user_in.lower() in stockdescr_words:
        menus.get_stock_descriptive(loaded_stock,ticker, ticker_info)
    elif user_in.lower() in stockpred_words:
        menus.get_lin_reg_prediction(ticker, loaded_stock, ticker_info)
    elif user_in == "3" or user_in.lower() in backWords:
        menus.menu_3(ticker, ticker_info)
    elif user_in == "4" or user_in.lower() in mainWords:
        menus.main_prompt()
    elif user_in == "5" or user_in.lower() in quitWords:
        print("Goodbye!")
        exit()
    else:
        print("That is not a valid query. Please try again.") # error message if user input not recognised
        menus.menu_3(ticker, ticker_info)


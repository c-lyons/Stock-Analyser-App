# menus.py

#importing cross referenced modules
import menu_choices, stock_describe, stock_predict, stock_plot


def main_prompt():
    """ this function is the main menu that the user will use upon opening the application"""
    user_in = input("""
************************************************
                 MAIN MENU
************************************************

Please choose:
_________________________________
1. Explore a Stock
2. Quit

""")
    menu_choices.menu_1_choose(user_in) # launch menu_1_choose function following user input


def menu_2():
    """This Search function prompts user for stock ticker"""
    user_choice = input("""
         SEARCH MENU
__________________________________

Please select an option from below:
__________________________________
1. Select stock by Ticker
2. Search stocks by Name
3. Back to Main Menu
4. Quit

""")
    menu_choices.menu_2_choose(user_choice)  # open menu_2_choose() with user input


def menu_3(ticker, ticker_info):
    """ This is the menu for the Stock Menu when ticker is found """
    user_in = input("""
           STOCK MENU
_________________________________
~   {}      ({})   ~

Please select from the following:
_________________________________

1. View Stock Overview
2. Stock Time-Series Analysis
3. Go Back
4. Main Menu
5. Quit

""".format(ticker_info[0], ticker.upper()))
    menu_choices.menu_3_choose(ticker, ticker_info, user_in) # open menu_3_choose() with user input


def menu_4(loaded_stock,ticker, ticker_info):
    """ This menu allows users to select which type of analyses they wish to perform
        before they enter a given date range"""
    user_in = input("""
                        ANALYSIS MENU
____________________________________________________________________

{} ({}) data loaded

Please select what type of analysis you would like to perform:
____________________________________________________________________

1. Descriptive Analysis
2. Predictive Analysis
3. Go Back
4. Main Menu
5. Quit

""".format(ticker_info[0], ticker.upper()))
    menu_choices.menu_4_choose(loaded_stock, ticker, user_in, ticker_info) # open menu_4_choose and pass variables


def stock_describe_menu(start, end, loaded_stock, ticker, ticker_info):
    """ This function allows users to select an action for the given time period """
    user_in = input("""
                    DESCRIPTION MENU
____________________________________________________________________

{} ({}) data loaded for period: {} to {}

Please select what type of analysis you would like to perform:
____________________________________________________________________

1. Descriptive Statistics (incl. mean, min, std and inter-quartile ranges)
2. Plot graphs for the selected date range
3. Back
4. Main Menu
5. Quit

""".format(ticker_info[0], ticker.upper(), start, end))

    stock_describe.stock_analyse(start, end, loaded_stock, ticker, user_in, ticker_info)


def get_lin_reg_prediction(ticker, loaded_stock, ticker_info):
    """ This function prepares a stock for price prediction using sklearn """

    print('''
******************************************************************** 
              Welcome to the Stock Predictor*
******************************************************************** 
(*We accept no responsibility if you lose all your money)

This application will predict a stock price for {} stock.

To begin, we must first select the number of days of recent data you
wish to use to train your model. (Recommended 30 days min -> 365 days max).

Please enter a number for number of training days
Please enter a target date in DD/MM/YYYY format. 
____________________________________________________________________
\n'''.format(ticker.upper()))

    stock_predict.lin_reg_prediction(ticker, loaded_stock, ticker_info)


def get_stock_descriptive(loaded_stock,ticker, ticker_info):
    """ this function is to select a time range for descriptive analytics """
    print("""
********************************************************************  
                Welcome to the Time Series Explorer! 
********************************************************************
To begin, please enter the time range you wish to view for {} stock.

Note:
-------------------------------------------------------------------
The following options are available:

Enter:

1. "Week"     : previous 7 days of data
2. "Month"    : previous 28 days of data
3. "Year"     : previous 365 days of data
4. "Custom"   : Manually enter "start" and "end" dates in DD/MM/YYYY format

Note: For "Custom" selection the following shortcuts are available:

"Earliest" : earliest available stock information
"Latest"   : latest available stock information.
____________________________________________________________________
""".format(ticker.upper()))

    stock_describe.stock_descr_time_checker(loaded_stock, ticker, ticker_info)


def stock_plotter_menu(loaded_stock, ticker, start, end, ticker_info):
    """ this function is to open menu for user selected features for plotting """
    print("""\n
********************************************************************
                 Welcome to the Stock Plotter. 
********************************************************************

This will plot the Closing Price for {} Stock

Please select which features you would like to include with your plot
_____________________________________________________________________

1. Simple Moving Average (SMA)
2. Exponentially Weighted Moving Average (EWMA)
3. Trend Line 
_____________________________________________________________________

""".format(ticker.upper()))
    stock_plot.stock_plotter(loaded_stock, ticker, start, end, ticker_info)


def stock_sub_plotter_menu(ticker):
    """ user selected options for subplot in descriptive plot"""
    print("""
____________________________________________________________________

Please also select which features you would like to include as a sub-plot
which will appear below your main graph (user may SELECT 1 OPTION ONLY)

(Note: by default Volume will be plotted if no selection given.)
____________________________________________________________________

1. Volume
2. Daily % Change in Close Price
3. Moving Average Convergence Divergence (MACD)

    \n""".format(ticker.upper()))


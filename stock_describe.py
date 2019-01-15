# stock_describe.py

# importing modules
from all_imports import datetime, pd, timedelta
import stock_plot, menu_choices, menus

# The following are lists of keywords which are used to check user input
yesWords = ['y', 'yes', 'ok', 'ye', 'yup', 'sure']
noWords = ['n', 'no', 'nope']
backWords = ['back', 'b', 'bac', 'go back']
quitWords = ['quit', 'q', 'close', 'exit']
mainWords = ['main menu', 'main', 'home', 'mainmenu']


def stock_descr_time_checker(loaded_stock, ticker, ticker_info):
    """ This function will prompt a user for date inputs.

       Options include selecting week, month, year or for a custom date rage in DD/MM/YYYY

       Entered dates will then be checked for their validity"""

    # list values to check user inputs
    weekWords = ['1','week', '1week', '1 week', '7 days', '7']
    monthWords = ['2', 'month', '1month', '1 month', '30 days']
    yearWords = ['3', 'year', '1year', '1 year', '365 days']
    customWords = ['4', 'custom', 'custom range', 'range', 'manual', 'enter custom']
    earlyWords = ['earliest', 'early', 'e', 'first', 'beginning', 'oldest', 'max']
    lateWords = ['latest', 'late', 'l', 'recent', 'today', 'youngest', 'min']

    user_in = input('Please select a desired time range:')  # asking user for selection
    today = datetime.now()  # setting variable for todays date using datetime function

    try:  # try and except to catch any Value Errors from user inputs

        # processing user inputs and checking input using list values
        if user_in.lower() in quitWords: # if user selects quit
            print('Goodbye!')
            exit()
        elif user_in.lower() in backWords: # if user selects back
            menus.menu_4(loaded_stock, ticker, ticker_info)
        # using datetime timedelta() function to calculate desired dates by subtracting from "today" variable

        elif user_in.lower() in weekWords: # if user selects week
            time_start_strip = today - timedelta(days=7)

        elif user_in.lower() in monthWords: # if user select month
            time_start_strip = today - timedelta(days=28)

        elif user_in.lower() in yearWords: # if user selects year
            time_start_strip = today - timedelta(days=365)
        # else if user selects custom range

        elif user_in.lower() in customWords:
            # new prompt for user to input custom dates
            time_start = input("Please enter a start date for your search...\n")

            if time_start in earlyWords:
                # if user enters 'earliest' retrieve earliest date on record.
                time_start_strip = datetime.strptime(loaded_stock.index[-1], "%Y-%m-%d")
            else:
                # else strip time from entered string
                time_start_strip = datetime.strptime(time_start, '%d/%m/%Y')

            if time_start_strip < datetime.strptime(loaded_stock.index[-1], "%Y-%m-%d"):
                # checking if start date entered is before earliest date on record
                print(
                    'No records exist for this stock before {}. Please try a different start date(or enter "Earliest" to select earliest available date).'.format(
                        datetime.strptime(loaded_stock.index[-1], "%Y-%m-%d")))
                stock_descr_time_checker(loaded_stock, ticker,
                                         ticker_info)  # restart stock_descr_time_checker to re-enter dates
        else:
            print('Please enter a valid option!')
            stock_descr_time_checker(loaded_stock, ticker, ticker_info)

    except ValueError: # checking for Value Errors for user input for invalid date formats
        print("Invalid selection! Please select an option from above.")
        stock_descr_time_checker(loaded_stock, ticker, ticker_info)

    try:
        # extracting end time similar to above
        # setting all end times to today variable, unless custom range selected
        if user_in.lower() in weekWords:  # if user originally selected week
            time_end_strip = today

        elif user_in.lower() in monthWords:  # if user originally selected month
            time_end_strip = today

        elif user_in.lower() in yearWords:  # if user selected year
            time_end_strip = today

        # if user selects customWords, then new prompt for end date
        elif user_in.lower() in customWords:

            time_end = input("Please enter an end date for your search...\n") # user input for end date

            if time_end.lower() in lateWords:
                # if user enters 'latest' retrieve latest available date (eg if used on the weekend and Friday was market close).
                time_end_strip = datetime.strptime(loaded_stock.index[0],"%Y-%m-%d")

            else:
                # else strip time from entered string
                time_end_strip = datetime.strptime(time_end, '%d/%m/%Y')

            if time_end_strip > datetime.strptime(loaded_stock.index[0], "%Y-%m-%d"):
                # checking if end date entered is beyond latest date on record
                print(
                    'This date ({})is beyond current records for this stock. Please try a different end date (or enter "Latest" to select latest available date)'.format(
                        time_end))
                stock_descr_time_checker(loaded_stock, ticker,
                                         ticker_info)  # restart stock_descr_time_checker to re-enter dates

            elif time_end_strip < time_start_strip:
                # checking if end date entered is before start date
                print('Error! You cannot select an end date before your start date. Please try again!')
                stock_descr_time_checker(loaded_stock, ticker,
                                         ticker_info)  # restart stock_descr_time_checker to re-enter dates

            elif time_end_strip == time_start_strip:
                # checking if end date entered is same as start date
                print('Error! You cannot select the same start date and end date! Please try again. ')
                stock_descr_time_checker(loaded_stock, ticker,
                                         ticker_info)  # restart stock_descr_time_checker to re-enter dates

        elif user_in.lower() in backWords:  # if user selects back
            menus.menu_4(loaded_stock, ticker, ticker_info)

        elif user_in.lower() in quitWords:  # if user selects quit
            print('Goodbye!')
            exit()
        else:
            print('Please enter a valid option!')
            stock_descr_time_checker(loaded_stock, ticker, ticker_info)

    except ValueError: # checking for user input value errors due to invalid formats etc
        print("Invalid selection! Please select an option from above.")
        stock_descr_time_checker(loaded_stock, ticker, ticker_info)

    #  converting end date to string format YYYY-MM-DD for index retrieval
    end = time_end_strip.strftime('%Y-%m-%d')

    # converting start date to string format YYYY-MM-DD for index retrieval
    start = time_start_strip.strftime('%Y-%m-%d')

    # else if dates are valid, then run stock_analyse function
    menus.stock_describe_menu(start, end, loaded_stock, ticker, ticker_info)


def stock_analyse(start, end, loaded_stock, ticker, user_in, ticker_info):
    """ this function analyses the selected loaded_stock dataframe for the user selected date ranges """

    # defining lists to check user inputs
    stockdescr_words = ['1', 'descriptive', ' descriptive analysis','descr', 'description']
    stockplot_words = ['2', 'plot', 'graph', 'plotter']

    if user_in.lower() in stockdescr_words: # if user selects descriptive...
        print('\nHere is the following summary statistics for the stock {} from {} to {}\n'.format(ticker.upper(), start, end))

        # creating new object to hold info for summary statistics and dropping unwanted columns
        loaded_print = loaded_stock.loc[end:start][::-1].drop(columns=['dividend_amount', 'close', 'split_coefficient'])

        # creating new dataframe for summary statistics
        loaded_print = pd.DataFrame(loaded_print.describe())
        loaded_print = loaded_print.drop('count', axis=0)
        loaded_print.loc['range'] = loaded_print.loc['max'] - loaded_print.loc['min'] # adding range to summary
        loaded_print.loc['coeff of var'] = loaded_print.loc['std'] / loaded_print.loc['mean'] # adding coeff var to summary
        print(loaded_print) # return summary description of stock for given dates

        user_in2 = input('Enter any key to return to the previous menu') # prompt to delay going back to menu
        menus.stock_describe_menu(start, end, loaded_stock, ticker, ticker_info) # go back to previous menu

    elif user_in.lower() in stockplot_words:  # if user selects stock
        menus.stock_plotter_menu(loaded_stock, ticker, start, end, ticker_info)

    elif user_in == "3" or user_in.lower() in backWords:  # if user selects back
        menus.get_stock_descriptive(loaded_stock,ticker, ticker_info)

    elif user_in == "4" or user_in.lower() in mainWords:  # if user selects main menu
        menus.main_prompt()

    elif user_in == "5" or user_in.lower() in quitWords:  # if user selects quit
        print('Goodbye!')
        exit()

    else:
        print('Error! Not a valid entry. Please try again.')  # else if user in not recognised return error and restart
        menus.stock_describe_menu(start, end, loaded_stock, ticker, ticker_info)


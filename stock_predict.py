# stock_predict.py

# importing required modules
from all_imports import LinearRegression, r2_score, mean_squared_error
from all_imports import datetime, pd, sqrt, timedelta

# importing cross referenced modules
import menus, menu_choices, stock_plot

# The following are lists of keywords which are used to check user input
yesWords = ['y', 'yes', 'ok', 'ye', 'yup', 'sure']
noWords = ['n', 'no', 'nope']
backWords = ['back', 'b', 'bac', 'go back']
quitWords = ['quit', 'q', 'close', 'exit']
mainWords = ['main menu', 'main', 'home', 'mainmenu']


def lin_reg_prediction(ticker, loaded_stock, ticker_info):
    """ This function accepts a user input for training days and prediction date for stock predictor
        time is entered as a string and checked using strptime function in datetime """

    time_train = input('Please enter the number of days from which the model will be trained.\n')

    # CHECKING TRAINING TIME INPUT

    if time_train.lower() in backWords:  # if user inputs back
        menus.menu_4(loaded_stock, ticker, ticker_info)

    elif time_train.lower() in quitWords:  # if user inputs quit
        print('Goodbye!')
        exit()
    else:
        pass

    try:
        time_train = int(time_train)  # setting time_train as integer

        if time_train < 0:  # if user selects negative return error
            print("Error! Please try again! Please enter the number of days you wish to use as training data.")
            lin_reg_prediction(ticker, loaded_stock, ticker_info)

        elif time_train > len(loaded_stock):
            print('Number of training days exceeds available data for stock. Please select a lower number.')
            lin_reg_prediction(ticker, loaded_stock, ticker_info)

        elif time_train > 365:  # if user selects greater than 365 days return warning
            print("Warning, you have selected training data beyond the recommended amount of days.")
            time_start_strip = datetime.strptime(loaded_stock.index[int(time_train)], "%Y-%m-%d")

        else:  # else strip time from user input
            time_start_strip = datetime.strptime(loaded_stock.index[int(time_train)], "%Y-%m-%d")

    except ValueError:
        print("Error! Please try again! Please enter the NUMBER of days you wish to use as training data.")
        lin_reg_prediction(ticker, loaded_stock, ticker_info)

    # checking if start date entered is before earliest date on record
    if time_start_strip < datetime.strptime(loaded_stock.index[-1], "%Y-%m-%d"):

        print('\nNo records exist for this stock before {}. Please try a different start date for training data.'.format(
                datetime.strptime(loaded_stock.index[-1], "%Y-%m-%d")))
        lin_reg_prediction(ticker, loaded_stock, ticker_info)  # restart to re-enter dates

    time_predict = input('Please enter the date you wish to predict closing price for {} stock.\n'.format(ticker.upper()))

    # CHECKING PREDICTION DATE INPUT

    if time_predict.lower() in backWords:
        menus.menu_4(loaded_stock, ticker, ticker_info)

    elif time_predict.lower() in quitWords:
        print('Goodbye!')
        exit()
    else:
        pass

    try:
        time_end_strip = datetime.strptime(time_predict, '%d/%m/%Y')

    except ValueError:
        print("Error! Wrong date format! Please enter the prediction date in the format DD/MM/YYYY.")
        lin_reg_prediction(ticker, loaded_stock, ticker_info)

    if time_end_strip > (datetime.now() + timedelta(days=10000)):
        # checking if prediction date entered is too dar into future
        print(
            '\nYou cannot predict this far into the future! Please try again...'.format(
                time_predict))
        lin_reg_prediction(ticker, loaded_stock, ticker_info)  # restart stock_descriptive() to re-enter dates

    # THIS IS THE BIT WE DELETED BY MISTAKE
    elif time_end_strip < datetime.now():
        # checking if prediction date entered is before today's date
        print(
            '\nYou cannot predict a price for a date that has already passed. Please try again.'.format(
                time_predict))
        lin_reg_prediction(ticker, loaded_stock, ticker_info)  # restart stock_descriptive() to re-enter dates

    else:
        # converting end date to datetime format YYYY-MM-DD for index retrieval
        end = time_end_strip.strftime('%Y-%m-%d')

        # converting start date to datetime format YYYY-MM-DD for index retrieval
        start = time_start_strip.strftime('%Y-%m-%d')

        # if dates are valid then run stock_predictor function
        stock_predictor(loaded_stock, start, end, time_predict, ticker, ticker_info)


def stock_predictor(loaded_stock, start, end, time_predict, ticker, ticker_info):
    print('Loading Stock Predictor. Please Wait...')

    # NB using adjusted close to account for stock split
    df_pred = pd.DataFrame(loaded_stock['adjusted_close'].loc[end:start][::-1])
    df_pred.columns = ['adjusted_close']  # renaming df_pred column to 'adjusted close'
    df_pred.index = pd.to_datetime(df_pred.index)  # setting index as datetime values for plotting

    # creating new 'date' column in df, mapping datetime index
    df_pred['date'] = pd.to_datetime(df_pred.index, dayfirst=False)
    # converting datetime values in 'date' column to ordinal values for regression plots
    df_pred['date'] = df_pred['date'].map(datetime.toordinal)

    y = df_pred['adjusted_close'].values.reshape(-1, 1)  # setting y as close price and reshapping as array
    X = df_pred['date'].values.reshape(-1, 1)  # setting X as date in tordinal and reshpaping as array

    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    df_pred['y_pred'] = lin_reg.predict(X)

    userin_date = pd.to_datetime(time_predict, dayfirst=True)
    userin_tord = userin_date.toordinal()
    # Make predictions w.r.t. 'x' and store it in a column called 'y_pred'
    user_pred = lin_reg.predict(userin_tord)
    user_pred_print = round(user_pred[0,0],2) # extracting value from array for clearer printing

    print('\nPredicted Stock Price for {} is {}\n'.format(time_predict, user_pred_print))

    # Returning R^2 and RMSE values using imported r2_score and mean_squared_error Linear Regression metrics
    print('\nR^2 Value for Model is: ', r2_score(y_pred = df_pred['y_pred'], y_true=df_pred['adjusted_close']))
    print('\nRMSE for Model is: ', sqrt(mean_squared_error(y_true = df_pred['adjusted_close'], y_pred=df_pred['y_pred'])))

    user_in = input('\nWould you like to plot this prediction? (Y/N)\n')  # ask user if they wish to plot

    if user_in.lower() in yesWords: # if user selects yes then plot
        stock_plot.predict_plotter(df_pred, ticker, user_pred, userin_date, user_pred_print, loaded_stock, ticker_info)

    else:  # else returm to previous menu
        menus.menu_4(loaded_stock, ticker, ticker_info)

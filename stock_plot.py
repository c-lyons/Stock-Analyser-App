# stock_plot.py

from all_imports import plt, datetime, sns, pd, LinearRegression

import menu_choices, menus, stock_predict

# setting plot styles from seaborn module for plotting
sns.set_style('darkgrid')
sns.set_palette('coolwarm')
sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2}) # setting custom seaborn settings for plotting

# The following are lists of keywords which are used to check user input
yesWords = ['y', 'yes', 'ok', 'ye', 'yup', 'sure']
noWords = ['n', 'no', 'nope']
backWords = ['back', 'b', 'bac', 'go back']
quitWords = ['quit', 'q', 'close', 'exit']
mainWords = ['main menu', 'main', 'home', 'mainmenu']

pd.options.mode.chained_assignment = None  # default='warn' # turning off warning relating to copying slice of df


def stock_plotter(loaded_stock, ticker, start, end, ticker_info):
    """ This function is for plotting closing price for a user selected stock"""
    from matplotlib import gridspec # import gridspec module (descriptive plots only for volume plot)

    # --------------------------------------------------------------------------------------
    #                           Data frame manipulation for plotting
    # --------------------------------------------------------------------------------------

    # creating dataframe of loaded stock for plotting and using normalised adjusted close to account for splits
    # note need to call [::-1] to reverse order of all rows so plot in correct order

    df_plot = pd.DataFrame(
        loaded_stock['adjusted_close'].loc[end:start][::-1])
    df_plot.columns = ['adjusted_close'] # renaming df_plot column to 'adjusted close'
    df_plot['volume'] = pd.DataFrame(loaded_stock['volume'].loc[end:start][::-1])  # adding volume column to data frame
    df_plot['% change'] = pd.DataFrame(loaded_stock['% Change'].loc[end:start][::-1]) # adding pct change column to data frame
    df_plot.index = pd.to_datetime(df_plot.index)  # setting index as datetime values for plotting

    # --------------------------------------------------------------------------------------
    #                                       Plotting
    # --------------------------------------------------------------------------------------

    fig = plt.figure(figsize=(20, 10)) # Create Figure (empty canvas)

    # use gridspec to plot volume as subplot and control aspect ratios
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) # GridSpec(rows,columns,height_ratios)

    ax0 = plt.subplot(gs[0, :])   # create ax0 and add labels and plot info
    ax0.plot(df_plot['adjusted_close'], label='Close Price')
    # create ax1 and share x axis with ax0
    ax1 = plt.subplot(gs[1, :], sharex=ax0)

    # --------------------------------------------------------------------------------------
    #                             User Prompts for adding Features
    # --------------------------------------------------------------------------------------

    feature_prompter(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)

    # plotting

    ax0.set_title('Close Price for {} Stock'.format(ticker.upper()))
    ax0.set_ylabel('Close Price ($)')
    ax0.legend()
    ax1.legend()

    # formating plot to have tight layout and to remove x-axis labels for top plot
    plt.tight_layout()
    plt.setp(ax0.get_xticklabels(), visible=False)

    # removing deadspace around plot to tighten
    ax0.autoscale(enable=True, axis='x', tight=True)
    ax1.autoscale(enable=True, axis='x', tight=True)
    plt.show(fig)  # plot figure
    menus.stock_describe_menu(start, end, loaded_stock, ticker, ticker_info)


def predict_plotter(df_pred, ticker, user_pred, userin_date, user_pred_print, loaded_stock, ticker_info):
    """ This function is for plotting closing price for a user selected stock"""

    # --------------------------------------------------------------------------------------
    #                             Formating Data for Plotting
    # --------------------------------------------------------------------------------------
    # creating dataframe for extrapolating trend line to predicted value and renaming column
    df_prediction = pd.DataFrame(user_pred)
    df_prediction.columns = ['prediction']

    # setting temp column name to extract date
    df_prediction['date pred'] = userin_date

    # resetting index to datetime date
    df_prediction.index = df_prediction['date pred']

    # appending last data entry from fitted model to extrapolate future trend line
    df_prediction = df_prediction.append(df_pred.iloc[-1])
    df_prediction['prediction'].iloc[1] = df_prediction['y_pred'].iloc[1]
    df_prediction = df_prediction.drop(columns=['date pred', 'adjusted_close', 'date', 'y_pred'])
    df_prediction.index = pd.to_datetime(df_prediction.index)

    # --------------------------------------------------------------------------------------
    #                                       Plotting
    # --------------------------------------------------------------------------------------
    fig = plt.figure(figsize=(20, 10)) # Create Figure (empty canvas)
    ax0 = plt.subplot() # creating axis object
    ax0.plot(df_pred['adjusted_close'], label='Close Price')
    ax0.plot(df_pred['y_pred'], label='Trend Line', color='c', ls='--')
    ax0.plot(df_prediction['prediction'], label='Predicted Trend Line', color='r', ls='--')
    ax0.plot(df_prediction['prediction'][:1], 'ro', label = 'Predicted Stock Price of {}'.format(user_pred_print))

    # set titles and legend for ax0
    ax0.set_title('Close Price for {} Stock'.format(ticker.upper()))
    ax0.set_ylabel('Close Price ($)')
    ax0.legend()

    # formating plot to have tight layout and to remove x-axis labels for top plot
    plt.tight_layout()

    plt.show()  # plot figure
    user_in = input('Would you like to perform another prediction? (Y/N) ')
    if user_in in yesWords:
        stock_predict.lin_reg_prediction(ticker, loaded_stock, ticker_info)
    else:
        menus.menu_4(loaded_stock, ticker, ticker_info)


def lin_reg_plot(df_plot):

    # Fit linear regression model using scikit-learn

    # creating new 'date' column in df_plot, mapping datetime index
    df_plot['date'] = pd.to_datetime(df_plot.index, dayfirst=False)

    # converting datetime values in 'date' columm to ordinal values for regression plots
    df_plot['date'] = df_plot['date'].map(datetime.toordinal)

    y = df_plot['adjusted_close'].values.reshape(-1, 1)  # setting y as adjusted close price and reshapping as array
    X = df_plot['date'].values.reshape(-1, 1)  # setting X as date in tordinal and reshpaping as array

    reg = LinearRegression() # obstantiating linear regression object
    reg.fit(X, y) # fitting X and y data
    df_plot['y_pred'] = reg.predict(X) # creating new df_plot column "y_pred" for plotting fitted trend line
    return df_plot


def feature_prompter(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot):
    """ Function to prompt user for which features they wish to add to plot"""
    # 1 - SIMPLE MOVING AVERAGE
    add_sma(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
    # 2 - EWA
    add_ewa(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
    # 3 - TREND
    add_trend(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
    # Ad SUBPLOT
    add_sub(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)

    return loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot


def add_sma(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot):
    """ function for adding simple moving average"""
    # PROMPT 1 - SMA

    prompt_1 = input("Include Simple Moving Average? (Y/N)\n")
    if prompt_1.lower() in yesWords:
        window = input('\nPlease enter the number of days for the Moving Average Window\n')
        try:

            if window.isdigit() is False:  # reject if negative variable entered
                print('\nValue must be a positive number, please try again\n')
                add_sma(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
            elif window.isdigit() is True:
                window = int(window)  # if string is a positive number then convert to int
                # plot to ax0 object
                ax0.plot(df_plot['adjusted_close'].rolling(window=window).mean(),
                         label='{} Day Rolling Closing Average'.format(window), color='r', alpha=0.6)
                return ax0
            else:
                print('\nValue must be a positive number, please try again\n')
                add_sma(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
        except ValueError:
            print('Value must be a whole positive number. Please try again!')
            add_sma(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)


    elif prompt_1.lower() in noWords:
        return ax0
    else:
        print('\nThat is not a valid query, please try again!\n')
        # restart add_sma function if invalid query
        add_sma(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)


def add_ewa(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot):
    """function for adding exponentially weighted average"""
    # PROMPT 2 - EWA

    prompt_2 = input("\nInclude Exponentially Weighted Moving Average? (Y/N)\n")
    if prompt_2.lower() in yesWords:

        span = input('\nPlease enter the number of days for the EWMA Window\n')

        try:

            if span.isdigit() is False:  # checking if entered value if pos whole number
                print('\nValue must be a positive whole number, please try again\n')
                add_ewa(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
            elif span.isdigit() is True:
                span = int(span)
                ema = df_plot['adjusted_close'].ewm(span=span).mean()  # calculating EMA using user defined window
                # adding EMA plot to axes
                ax0.plot(ema, color='g', alpha=0.6, label='{} Day Exponentially Weighted Moving Average'.format(span))

                return ax0

            else:
                print('\nValue must be a positive whole number, please try again\n')
                add_ewa(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)
        except ValueError:
            print('\nValue must be a positive whole number, please try again\n')
            add_ewa(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)

    elif prompt_2.lower() in noWords:
        # else if EWA not wanted, pass
        return ax0

    else:
        print('\nThat is not a valid query, please try again.\n')
        # restart add_ewa function if invalid query
        add_ewa(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)


def add_trend(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot):
    """function for adding trend line"""
    # 3 - TREND LINE
    prompt_3 = input("\nInclude Trend Line? (Y/N)\n")

    if prompt_3.lower() in yesWords:
        print('\nApplying selection. Please wait...')
        lin_reg_plot(df_plot) # if yes, calling on lin_reg_plot function to create trend line using linear regession
        ax0.plot(df_plot['y_pred'], label='Trend Line', color='c', ls='--')

        return ax0

    elif prompt_3.lower() in noWords:

        return ax0

    else:
        print('\nThat is not a valid query, please try again.\n')
        add_trend(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)


def add_sub(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot):
    """function for adding trend line"""
    # SUB-PLOT PROMPTS
    menus.stock_sub_plotter_menu(ticker)  # running subplot menu and getting user input
    sub_in = input()

    vol_plot = ['1', 'vol', 'volume']
    pct_plot = ['2', 'percent', '%', 'pct change']
    macd_plot = ['3', 'macd', 'moving', 'moving']

    # VOLUME SUBPLOT
    if sub_in.lower() in vol_plot:

        ax1.plot(df_plot['volume'], label='Volume', color='k', alpha=0.5)
        # adjusting limits for y-axis
        ax1.ticklabel_format(axis='y', style='sci', useMathText=True, scilimits=(0, 6))
        ax1.set_ylabel('Volume')
        return ax1

    # PCT CHANGE SUBPLOT
    elif sub_in.lower() in pct_plot:

        ax1.plot(df_plot['% change'], label='Daily % Change in Close', color='k', alpha=0.5)
        # adjusting limits for y-axis
        ax1.set_ylabel('Daily % Change in Close Price')
        return ax1

    # MACD SUBPLOT
    elif sub_in.lower() in macd_plot:

        # Calculating Exp. Weighted Moving Avergages for 26 and 12 day periods for MACD
        ema26 = df_plot['adjusted_close'].ewm(span=26).mean()  # calculating 26 day EMA
        ema12 = df_plot['adjusted_close'].ewm(span=12).mean()  # calculating 12 day EMA
        # macd is difference between ema26 or ema12
        macd = ema26 - ema12

        # SIGNAL LINE
        prompt_b = input('\nDo you wish to include the 9 EMA signal line?\n')
        if prompt_b.lower() in yesWords:

            ema9 = macd.ewm(span=9).mean()  # calculating 9 day EMA
            ax1.plot(ema9, color='k', alpha=0.4, label='MACD Signal Line')
            # adding MACD plot to axes
            ax1.plot(macd, color='m', alpha=0.4, label='Moving Average Convergence Divergence')
            # labelling axis
            ax1.set_ylabel('MACD')

            return ax1

        elif prompt_b.lower() in noWords:
            # adding MACD plot to axes
            ax1.plot(macd, color='m', alpha=0.4, label='Moving Average Convergence Divergence')
            # labelling axis
            ax1.set_ylabel('MACD')

            return ax1

        else:
            print('Invalid entry. Please reply "Yes" or "No"!.')
            add_sub(loaded_stock, ticker, start, end, ticker_info, ax0, ax1, df_plot)

        return ax1

    else:
        # ELSE PLOT VOLUME AS DEFAULT
        ax1.plot(df_plot['volume'], label='Volume', color='k', alpha=0.5)
        # adjusting limits for y-axis
        ax1.ticklabel_format(axis='y', style='sci', useMathText=True, scilimits=(0, 6))
        ax1.set_ylabel('Volume')
        return ax1
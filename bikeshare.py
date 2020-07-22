import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def separator_display(message, symb):
    """
    Display and center a message on the screen.

    Args :
        (str) message - the message to display
        (str) symb     - the symbol used to draw a line
    """
    shift = (79 - len(message)) // 2
    reminder = (79 - len(message)) % 2
    #print(symb * 79)
    print(symb * shift + message + symb * (shift + reminder))
    print(symb * 79)

def clear():
    """ Clean the console"""

    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def menu_display():
    """ Display the Principal Menu  """

    #separator_display('Bikeshare Application Menu', ' ')
    print('-'*79)
    print('| Load Data [1] ' + '| Raw Data [2] ' + '| Time Statistics [3] ' + '| Station Statistics [4] |')
    print('-'*79)
    print('|    Duration Statistics [5]   ' + '| User Statistics [6] |' + ' Exit Application   [7] |')
    print('-'*79)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nPlease, choose One City from the list [chicago, new york city, washington] :\n')
        if city.lower() in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Invalid input, try again!!!')


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nMake your Month choice from the list [all, january, february, ... , june]\nYou can choose more than One Month. You have to separate the Months by a comma:\n')

        month = month.title()
        month = month.replace(" ", "")
        month = month.split(",")

        if 'All' in month:
            month = ['All']

        if set(month).intersection(set(['All', 'January', 'February', 'March', 'April', 'May', 'June'])) == set(month):
            break
        else:
            print('\nInvalid input, try again!!!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('\nMake your Day choice from the list [all, monday, tuesday, ... sunday] \nYou can choose more than One Day. You have to separate the Days by a comma:\n')

        day = day.title()
        day = day.replace(" ", "")
        day = day.split(",")

        if 'All' in day:
            day = ['All']

        if set(day).intersection(set(['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])) == set(day):
            break
        else:
            print('\nInvalid input, try again!!!\n')

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    separator_display("Data Loading", "-")
    print('Loading Data....')

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

    # filter by month if applicable
    if month != ['All']:
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'].isin(month)]

    # filter by day of week if applicable
    if day != ['All']:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].isin(day)]
    df['trip'] = df['Start Station'] + '==>' + df['End Station']
    separator_display("!!! Data Loaded Successfully !!!", ' ')
    print()

    return df

def raw_data_display(df):
    """To display the raw data from DataFrame"""

    i = int(input('Enter the number of rows to be displayed : '))    

    separator_display("Displaying raw Data", "-")
    print('\nData Columns details :\n')
    pd.set_option('display.max_columns', None)

    cols = [col for col in df.columns if col not in ['trip', 'Unnamed: 0']]
    print(df[cols].info())
    print('\nThe {} first rows of the Data : \n'.format(i))
    print(df[cols].head(i))
    print()
    
    count = i
    while count <= len(df) :
        continue_display = input('Would you display the next {} lines of raw data? "y" for yes, "n" for no.\nYou can even jump to a specified row where the row number between 0 and {} : '.format(i, len(df) - 1))
        print("-"*79)
        if continue_display.lower() == "y" or continue_display.lower() == "yes":
            print(df[cols].iloc[count:(count + i), :])
            count += i 
        elif continue_display.lower() == "n" or continue_display.lower() == "no":
            clear()
            break
        elif (continue_display.isdigit()) and (int(continue_display) in range(len(df))) and (int(continue_display) >= 0):
            count = int(continue_display)
            print(df[cols].iloc[int(continue_display):(int(continue_display) + i), :])
            count += i
        else:
            print("\nInvalid input.\n")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    separator_display("Time Statistics", "-")

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nMost Common Month ========> ',df['month'].mode()[0])

    # display the most common day of week
    print('\nMost Common Day of week ==> ',df['day_of_week'].mode()[0])

    # display the most common start hour
    print('\nMost Common Start Hour ===> '+ str(df['Start Time'].dt.hour.mode()[0])+'H')

    # display Months Vs Days by Number of Rentals

    print('\nMonths Vs Days by Number of Rentals ===>\n')
    print(df.pivot_table(index = 'month', columns = 'day_of_week', values = 'Trip Duration', aggfunc = 'count'))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    separator_display("Stations Statistics", "-")
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost Commonly used Start Station ==> ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nMost Commonly used End Station ====> ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip

    print('\nMost frequent combination of Start Station and End Station trip :\n')

    trips_max = df['trip'].value_counts()[df['trip'].value_counts()== df['trip'].value_counts().max()]
    trips_max_df = trips_max.index.to_series().str.split('==>', expand = True)
    trips_max_df.columns = ['Start Station', 'End Station']
    print(trips_max_df.reset_index(drop = True))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    separator_display("Trips Duration Statistics", "-")
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time ==> ', round(df['Trip Duration'].sum() / 60, 2), 'Minutes.')

    # display mean travel time
    print('\nMean travel time ===> ',round(df['Trip Duration'].mean() / 60, 2), 'Minutes.')

    # display Months Vs Days by Trip Duration Mean
    print('\nMonths Vs Days by Trip Duration Mean (in Minutes) ===> ')
    print(round(df.pivot_table(index = 'month', columns = 'day_of_week', values = 'Trip Duration', aggfunc = np.mean)/60,2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    separator_display("Users Statistics", "-")
    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types =======>')
    print(df['User Type'].value_counts().rename_axis('User Type').reset_index(name = 'Counts'),'\n')

    # Display user types Vs Days by Number of Rentals
    print('\nUser Types Vs Days by Number of Rentals =======>')
    print(df.pivot_table(index = 'User Type', columns = 'day_of_week', values = 'Trip Duration', aggfunc = 'count'),'\n')

    # Display user types Vs Months by Number of Rentals
    print('\nUser Types Vs Months by Number of Rentals =======>')
    print(df.pivot_table(index = 'User Type', columns = 'month', values = 'Trip Duration', aggfunc = 'count'),'\n')


    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        # Display counts of gender
        print('\nCounts of gender ===========>')
        print(df['Gender'].value_counts(dropna = False).rename_axis('Gender').reset_index(name = 'Counts'))

        # Display earliest year of birth
        print('\nEarliest year of birth =====>', int(df['Birth Year'].min()))

        # Display most recent year of birth
        print('\nMost recent year of birth ==>', int(df['Birth Year'].max()))

        # Display most common year of birth
        print('\nMost common year of birth ==>', int(df['Birth Year'].mode()[0]))

    else:
        # Display counts of gender
        print("\nCounts of gender ===========> Sorry! No Gender data for :", city)

        # Display earliest year of birth
        print("\nEarliest year of birth =====> Sorry! No birth data for :", city)

        # Display most recent year of birth
        print("\nMost recent year of birth ==> Sorry! No birth data for :", city)

        # Display most common year of birth
        print("\nMost common year of birth ==> Sorry! No birth data for :", city)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    clear()
    cwd=''
    cwd = os.getcwd()
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path     = os.path.dirname(os.path.abspath(filename))
    os.chdir(path)
    while True:
        menu_display()
        while True:
            menu_input = input('Choose Menu Item from 1 to 7 : ')
            if (menu_input.isdigit()) and (int(menu_input) in range(1,8)):
                break
            else:
                print('\nInvalid input !!!.\n')

        if int(menu_input) == 1:
            clear()
            city, month, day = get_filters()
            df = load_data(city, month, day)
        elif int(menu_input) == 7:
            clear()
            exit_input = input('\nWould you really like to exit? Enter yes or no.\n')
            if exit_input == "yes":
                clear()
                os.chdir(cwd)
                break
        else:
            if 'df' not in locals():
                clear()
                print()
                print("Data have not been loaded. Try to load a Data Set.")
                print()

            else:
                if int(menu_input) == 2:
                    clear()
                    raw_data_display(df)
                    print()
                elif int(menu_input) == 3:
                    clear()
                    time_stats(df)
                    print()
                elif int(menu_input) == 4:
                    clear()
                    station_stats(df)
                    print()
                elif int(menu_input) == 5:
                    clear()
                    trip_duration_stats(df)
                    print()
                elif int(menu_input) == 6:
                    clear()
                    user_stats(df, city)
                    print()


if __name__ == "__main__":
    main()
import timeit
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

seperator = lambda i :print(i*70)

def operation_time(start_time):
    #calculate the time
    stop =  timeit.default_timer()
    opt_time = "[... %s seconds]" % round((stop - start_time),4)
    print(opt_time.rjust(100,"-"))
    print(seperator)

def filter_city():
    """
    Asks user to specify city.

    Returns:
        (str) city - name of the city to analyze
    """
    #display the list of cities that which we have datasets
    cities_list = list()
    number_cities = 0
    seperator("*")
    print("\nPlease select a city from below which you would like to discover data...\n\n")
    for city in CITY_DATA:
        cities_list.append(city)
        number_cities += 1
        print('     {0}  --> {1}'.format(number_cities, city.title()))

    # Choose the number of the city that you would like to explore choosen city's data from the list of cities-- Integer is more easier than string for choosing.
    while True:
        try:
            city_numb = int(input("\n     Enter a number for the city (1 - {}):  ".format(len(cities_list))))
        except:
            continue
        if city_numb in range(1, len(cities_list)+1):
            seperator("*")
            break
        else:
            cstr="Please input valid number from the list of cities..."
            print(cstr.rjust(40,'-'))
    # get the city's name in string format from the list
    city_name = cities_list[city_numb - 1]
    return city_name

def filter_month():
    """
    Asks user to specify month to filter, or all months.

    Returns:
        (str)  month - name of the month to filter by, or "all" to apply no month filter
    """
    month_list = list()
    number_month = 0
    #display the list of months that which we have datasets
    for month in MONTHS:
        month_list.append(month)
        number_month +=1
        print('     {0}  --> {1}'.format(number_month, month.title()))
    print('\n     OR\n     all -->For All Months')
    # Choose the number of the month or all that you would like to explore choosen city's data from the list of months.
    while True:
        try:
            month_ind = input("\n     Enter the month with January=1, June=6 or 'all' for all:  ")
        except:
            continue
        if month_ind == 'all':
            month = month_ind
            seperator("=")
            break
        elif month_ind in {'1', '2', '3', '4', '5', '6'}:
            # -1 for assign correct index.
            month = MONTHS[int(month_ind) - 1]
            seperator("=")
            break
        else:
            print("\nPlease input valid option:  1 - 6 or all")
            continue
    return month

def filter_day():
    """
    Asks user to specify a day to filter, or all days.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    day_list = list()
    number_day = 0
    #display the list of months that which we have datasets
    for day in DAYS:
        day_list.append(day)
        number_day +=1
        print('     {0}  --> {1}'.format(number_day, day.title()))
    print('\n     OR\n     all --> For All Days')
    while True:
        try:
            day_ind = input("\n     Enter the day with Monday=1, Sunday=7 or 'all' for all:  ")
        except:
            continue

        if day_ind == 'all':
            day = day_ind
            seperator("=")
            break
        elif day_ind in ['1', '2', '3', '4', '5', '6', '7']:
            # -1 for assign correct index.
            day = DAYS[int(day_ind) - 1]
            seperator("=")
            break
        else:
            print("\nPlease input valid option:  1 - 7 or all")
            continue
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    seperator("*")
    print('\n  Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    #  HINT: Use a while loop to handle invalid inputs
    city = filter_city()

    # get user input for month (all, january, february, ... , june)
    month = filter_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = filter_day()

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
    #Load data files into a dataframe
    start_time=timeit.default_timer()
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    # extract month, day and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if available
    if month != 'all':
        # the index of the MONTHS list to get the corresponding integer
        month_index = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df.month == month_index]
        month= month.title()
    # filter by day of week if available

    if day != 'all':
        # use the index of the DAYS list to get the corresponding integer
        day_index = DAYS.index(day)
        # filter by day of week to create the new dataframe
        df = df[df.day == day_index]
        day=day.title()

    print("\nSelected city name: ",city.title())
    print("Selected time (month and day): ",month,"-",day)
    print("Total rows in dataset: {}\n" .format(len(df)))
    operation_time(start_time)
    seperator("=")
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time=timeit.default_timer()
    print('Here is the result of the most frequent times of travel;')
    # display the most common month
    month = MONTHS[df['month'].mode()[0] - 1].title() # -1 for 0-based
    print('-----> Month:               ', month)

    # display the most common day of week
    common_day = df['day'].mode()[0]
    common_day = DAYS[common_day].title()
    print('-----> Day of the week:     ', common_day)

    # display the most common start hour; convert to 12-hour string
    hour = df['hour'].mode()[0]
    print('-----> Start hour:          ', hour)
    operation_time(start_time)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time=timeit.default_timer()
    print('Here is the result of the most frequent stations of trips:\n')

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_trips = df['Start Station'].value_counts()[start_station]

    print('    Start station:       ', start_station)
    print('    {}{}/{} trips ---> %{:3.2f}\n'.format(' '*len('Start station:'),start_station_trips, len(df),(start_station_trips*100)/len(df)))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_station_trips = df['End Station'].value_counts()[end_station]

    print('    End station:         ', end_station)
    print('    {}{}/{} trips ---> %{:3.2f}\n'.format(' '*len('End station:'),end_station_trips, len(df),(end_station_trips*100)/len(df)))

    # display most frequent combination of start station and end station trip
    # group the results by start station and end station
    df_comb_str_end_gb = df.groupby(['Start Station', 'End Station'])
    max_freq_trip_count = df_comb_str_end_gb['Trip Duration'].count().max()
    max_freq_trip = df_comb_str_end_gb['Trip Duration'].count().idxmax()
    print('    Frequent trip:        {}, {}'.format(max_freq_trip[0], max_freq_trip[1]))
    print('    {}{} trips'.format(' '*len('Frequent trip:'), max_freq_trip_count))
    operation_time(start_time)

def seconds_to_HMS_str(total_seconds):
    """
    Converts number of seconds to human readable string format.

    Args:
        (int) total_seconds - number of seconds to convert
    Returns:
        (str) day_hour_str - number of weeks, days, hours, minutes, and seconds
    """
    #The divmod() method in python takes two numbers and returns a pair of numbers consisting of their quotient and remainder.
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    day_hour_str = ''
    if weeks > 0:
        day_hour_str += '{} weeks, '.format(weeks)
    if days > 0:
        day_hour_str += '{} days, '.format(days)
    if hours > 0:
        day_hour_str += '{} hours, '.format(hours)
    if minutes > 0:
        day_hour_str += '{} minutes, '.format(minutes)

    # always show the seconds, even 0 secs when total > 1 minute
    if total_seconds > 59:
        day_hour_str += '{} seconds'.format(seconds)

    return day_hour_str
def seconds_conv(total_seconds):
    """
    Converts number of seconds to string format.

    Returns:
        (str) time_str - number of weeks, days, hours, minutes, and seconds
    """

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    time_str = ''
    if weeks > 0:
        time_str += '{} weeks '.format(weeks)
    if days > 0:
        time_str += '{} days '.format(days)
    if hours > 0:
        time_str += '{} hours '.format(hours)
    if minutes > 0:
        time_str += '{} minutes '.format(minutes)

    return time_str

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time=timeit.default_timer()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('    Total travel time:   ', seconds_conv(total_travel_time),"\n")

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('    Mean travel time:    ',  seconds_conv(mean_travel_time))

    operation_time(start_time)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time=timeit.default_timer()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of the user type:')
    for i in range(len(user_types)):
        value = user_types[i]
        user_type = user_types.index[i]
        print('{}{}  :  {}'.format(' '*20,user_type ,value))

    # Display counts of gender
    print('\nCount of the gender type:')
    if 'Gender' in df.columns: # 'if' for NaN
        genders = df['Gender'].value_counts()
        for index in range(len(genders)):
            value = genders[index]
            gender = genders.index[index]
            print('{}{}  :  {}'.format(' '*20,gender , value))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns: # 'if' for NaN
        print('\nYear of Birth:')
        print('{}Earliest  :  {}'.format(' '*20,int(df['Birth Year'].min())))
        print('{}Most recent  :  {}'.format(' '*20,int(df['Birth Year'].max())))
        print('{}Most common  :  {}'.format(' '*20,int(df['Birth Year'].mode())))

    operation_time(start_time)

def print_raw_data(df):
    """
    Asks if the user would like to see some rows of data from the dataset.
    Displays 5 rows,then again asks that they would like to see 5 rows more.
    Continues asking until the users input no.
    """
    show_rows = 5
    rows_str = 0
    rows_end = show_rows - 1    # use index values for rows

    print('\n Would you like to see some raw data from the dataset?')
    while True:
        data = input(' ------>Yes or No? :  '.format(' '))
        if data.lower() == 'yes':
            # display show_rows number of rows but we add +1 for users (human readable)
            # rows_strt = 0 -- rows_end = 4, print to user --> "rows 1 to 5"
            print('\n    Displaying rows {} to {}:'.format(rows_str+1, rows_end + 1))

            print('\n', df.iloc[rows_str : rows_end + 1]) # +1 because 'rows_end + 1' is excluded.
            rows_str += show_rows
            rows_end += show_rows

            seperator('=')
            print('\n Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no ?\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

# set option to display all columns of the dataframe (Source: URL: https://towardsdatascience.com/how-to-show-all-columns-rows-of-a-pandas-dataframe-c49d4507fcf)
# this option is used for showing the raw data in the raw_data function
pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Would you like to see data for Chicago, New York or Washington?')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in ['chicago', 'new york city', 'washington', 'all']:
        city = input('Please enter the desired city (all, chicago, new york city, washington): ').lower()


    # get user input for filtering
    filter_by = ''

    while filter_by not in ['not', 'month', 'day', 'both']:
        filter_by = input('Would you like to filter by month, day, both or not at all? Please enter "not" in the latter case! ').lower()

    # initializing month and day string variables
    month = ''
    day = ''

    # conditional user input dependent on the filtering setting
    if filter_by == 'month':
        while (month not in months and month != 'all'):
            month = input('Please enter the desired month (all, january, february, ... , june): ').lower()
            day = 'all'

    elif filter_by == 'day':
        while (day not in days and day != 'all'):
            day = input('Please enter the desired day (all, monday, tuesday, ... sunday): ').lower()
            month = 'all'

    elif filter_by == 'both':
        while (month not in months and month != 'all'):
            month = input('Please enter the desired month (all, january, february, ... , june): ').lower()
        while (day not in days and day != 'all'):
            day = input('Please enter the desired day (all, monday, tuesday, ... sunday): ').lower()
    else:
        month = 'all'
        day = 'all'


    print("\n")

    print('-'*40)
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
    # reading in one data set or all datasets dependent on user input
    # the first data set is always read in via the read_csv-function

    # in case of reading in all files, the index zero in the list of all keys of the dicitionary is used to differentiate between the first file and the subseqeuent files
    # Source: https://stackoverflow.com/questions/14538885/how-to-get-the-index-with-the-key-in-python-dictionary

    # the second and third files are then appended to the dataframe

    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    else:
        for x in CITY_DATA:
            if list(CITY_DATA.keys()).index(x) == 0:
                df = pd.read_csv(CITY_DATA[x])
            else:
                df = df.append(pd.read_csv(CITY_DATA[x]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().idxmax()
    popular_month_count = df['month'].value_counts().max()

    if month == 'all':
        print("Most popular month: {}, Count: {}".format(popular_month, popular_month_count))
    else:
        print("You have already filtered by {}. therefore most popular month: {}, Count: {}".format(month, popular_month, popular_month_count))

    # display the most common day of week
    popular_day = df['day_of_week'].value_counts().idxmax()
    popular_day_count = df['day_of_week'].value_counts().max()


    if day == 'all':
        print("Most popular day: {}, Count: {}".format(popular_day, popular_day_count))
    else:
        print("You have already filtered by {}, therefore most popular day: {}, Count: {}".format(day, popular_day, popular_day_count))


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    popular_hour_count = df['hour'].value_counts().max()
    print("Most popular hour: {}, Count: {}".format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    popular_start_station_count = df['Start Station'].value_counts().max()

    print("Most popular start station: {}, Count: {}".format(popular_start_station, popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    popular_end_station_count = df['End Station'].value_counts().max()

    print("Most popular end station: {}, Count: {}".format(popular_end_station, popular_end_station_count))

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + " AND " + df['End Station']
    popular_station_combination = df['Station Combination'].value_counts().idxmax()
    popular_station_combination_count = df['Station Combination'].value_counts().max()

    print("Most popular station combination: {}, Count: {}".format(popular_station_combination, popular_station_combination_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # defining variables
    seconds_per_day = 60*60*24
    seconds_per_hour = 60*60
    seconds_per_minute = 60

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_travel = df['Trip Duration'].sum()
    total_days = int(total_time_travel // seconds_per_day)
    total_hours = int((total_time_travel - total_days * seconds_per_day) // seconds_per_hour)
    total_minutes = int((total_time_travel - total_days * seconds_per_day - total_hours * seconds_per_hour) // seconds_per_minute)
    total_seconds = (total_time_travel - total_days * seconds_per_day - total_hours * seconds_per_hour) % seconds_per_minute

    print("Total time of travel: {} seconds or {} days {} hours {} minutes {} seconds".format(total_time_travel, total_days, total_hours, total_minutes, total_seconds))

    # display mean travel time
    mean_time_travel = df['Trip Duration'].mean()
    mean_days = int(mean_time_travel // seconds_per_day)
    mean_hours = int((mean_time_travel - mean_days * seconds_per_day) // seconds_per_hour)
    mean_minutes = int((mean_time_travel - mean_days * seconds_per_day - mean_hours * seconds_per_hour) // seconds_per_minute)
    mean_seconds = (mean_time_travel - mean_days * seconds_per_day - mean_hours * seconds_per_hour) % seconds_per_minute                  

    print("Mean time of travel: {} seconds or {} days {} hours {} minutes {} seconds".format(mean_time_travel, mean_days, mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print("\n")

    # Display counts of gender (not applicable for Washington)
    if city != 'washington':
        print(df['Gender'].value_counts())
        print("\n")
    else:
        print('For Washington there is no gender information!')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode())

        print("Earliest year of birth: {} ".format(earliest_year))
        print("Most recent year of birth: {} ".format(most_recent_year))
        print("Most common year of birth: {} ".format(most_common_year))
    else:
        print('For Washington there is no birth year information!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays the first 5 lines or the next 5 lines respectively if the user confirms."""

    # initializing the boundaries for the first and last line and initializing the counter variable
    # the counter variable is used to differentiate between the "first 5 lines " and the "next 5 lines"
    row_lower = 0
    row_upper = 5
    counter = 0

    while True:
        redo = ''
        while redo not in ['yes', 'no']:
            if counter == 0:
                redo = input('Would you like to see the first 5 lines of raw data? Enter yes or no: ').lower()
                counter += 1

                if redo not in ['yes', 'no']:
                    counter = 0
            else:
                redo = input('Would you like to see the next 5 lines of raw data? Enter yes or no: ').lower()
        if redo == 'yes':

            print("\n")

            # Source for the iloc-function: https://www.askpython.com/python/built-in-methods/python-iloc-function#:~:text=%20Python%20iloc%20%28%29%20function%20%E2%80%93%20All%20you,the%20functioning%20of%20Python%20iloc%20%28%29...%20More%20
            print(df.iloc[row_lower:row_upper, :])

            print("\n")
            row_lower = min(row_lower + 5, len(df))
            row_upper = min(row_upper + 5, len(df))

        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

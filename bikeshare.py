import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = 'all'
    day = 'all'
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        filter_type = input("Would you like to filter by month, day, both or without filter: ").lower()
        if filter_type in  ['month', 'day', 'both', 'without filter', 'without']:
            break
        print("please type a valid filter")
    while True:
        city = input("Please type the name of the city: " ).lower()
        if city in  ['chicago', 'new york city', 'washington']:
            break
        print("please type a valid city name")
    # get user input for month (all, january, february, ... , june)

    if filter_type == 'month' or filter_type == 'both':
        while True:
            month = input("Please type the month (january, february, ... , june) or type all : " ).lower()
            if month in ['all' , 'january', 'february', 'march', 'april', 'may' , 'june']:
                break
            print("please type a valid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_type == 'day' or filter_type == 'both':
        while True:
            day = input("Please type the day (monday, tuesday, ... sunday) or type all : " ).lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' , 'sunday', 'all']:
                break
            print("please type a valid day")

    print('-'*40)
    return city, month, day, filter_type


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    #day_dict = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, filter_type):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (if no filter by month is applied)
    if filter_type not in ['month', 'both']:
        months_dict = {1: 'January', 2: 'Februry', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
        month_count = {}
        for i in range(1, 7):
            count_df = df[df['month'] == i ].count()
            month_count[i] = count_df['month']
        most_month = max(month_count, key=month_count.get)
        print('The most common month is: {}'.format(months_dict[most_month]))

    # display the most common day of week (if no filter by day is applied)
    if filter_type not in ['day', 'both']:
        day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednsday', 3: 'Thursday', 4: 'Friday', 5: 'Saterday', 6: 'Sunday'}
        day_count = {}
        for i in range(6):
            count_df = df[df['day_of_week'] == i].count()
            day_count[i] = count_df['day_of_week']
        most_day = max(day_count, key=day_count.get)
        print('The most common day is: {}'.format(day_dict[most_day]))

    # display the most common start hour
    hour_count = []
    for i in range(24):
        count_df = df[df['Start Time'].dt.hour == i].count()
        hour_count.append(count_df['Start Time'])
    print('The most common hour is: {}'.format(hour_count.index(max(hour_count))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station (the first for loop takes alot of time
    start_station = df.groupby('Start Station')['Unnamed: 0'].nunique()
    most_sstation = start_station[start_station == max(start_station)].index[0]
    print('The most commonly used start station is: {}, with count of: {}'.format(most_sstation, max(start_station)))

    # display most commonly used end station
    end_station = df.groupby('End Station')['Unnamed: 0'].nunique()
    most_estation = end_station[end_station == max(end_station)].index[0]
    print('The most commonly used end station is: {}, with count of: {}'.format(most_estation, max(end_station)))


    # display most frequent combination of start station and end station trip
    trip_combination = df.groupby(['Start Station', 'End Station'])['Unnamed: 0'].nunique()
    most_combination = trip_combination[trip_combination == max(trip_combination)].index[0]
    print('The most frequent combination is: {}, with count of: {}'.format(most_combination, max(trip_combination)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time in minutes is: {}'.format(df['Trip Duration'].sum()/60))


    # display mean travel time
    print('The mean travel time in minutes is: {}'.format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby('User Type')['Unnamed: 0'].nunique()
    for i in range(len(user_type)):
        print('The user type ({}) has count of {}'.format(user_type.index[i], user_type[i]))

    if city != 'washington':
        # Display counts of gender
        gender = df.groupby('Gender')['Unnamed: 0'].nunique()
        print('The ({}) gender has count of {}\
        , while ({}) gender has count of {}'.format(gender.index[0], gender[0], gender.index[1], gender[1]))


        # Display earliest, most recent, and most common year of birth
        year_count = df.groupby('Birth Year')['Unnamed: 0'].nunique()
        most_year = year_count[year_count == max(year_count)].index[0]
        print('The earliest year of birth is ({}). And the most recent year of birth is({}). \
        \n And the most common year of birth is ({})'.format(min(df['Birth Year']), max(df['Birth Year']), most_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_raw_data(df):
    i = 0
    while True:
        raw_data = input('\nWould you like to view 5 lines of raw data? Enter yes or no.\n')
        if raw_data.lower() != 'yes' or df.iloc[i:i+5].empty == True:
            break
        else:
            print(tabulate(df.iloc[i:i+5], headers='keys'))
        i += 5

def main():
    while True:
        city, month, day, filter_type = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter_type)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

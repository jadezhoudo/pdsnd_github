import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """Prompt the user to provide filters for city, month, and day.

    Returns:
    tuple: A tuple containing strings representing the chosen city, month, and day.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input(
            "Which city would you like to analyze? (Washington, Chicago, New York City): ").lower()
        if city in CITY_DATA:
            break
        print("Sorry, that's not a valid city. Please choose from Washington, Chicago or New York City.")

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input(
        "Which month? January, February, March, April, May, June, or 'all': ").lower()
    if month != 'all' and month not in months:
        month = 'all'

    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    day = input(
        "Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all': ").lower()
    if day != 'all' and day not in days:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data from CSV file based on the chosen city, month, and day filters.

    Args:
    city (str): The chosen city.
    month (str): The chosen month.
    day (str): The chosen day.

    Returns:
    DataFrame: A DataFrame containing the filtered bikeshare data.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Calculate and display the most frequent times of travel.

    Args:
    df (DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print("Most common month:", popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print("Most common day of week:", popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most common start hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Calculate and display the most popular stations and trip.

    Args:
    df (DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station:", common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station:", common_end_station)

    df['Station Combo'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Station Combo'].mode()[0]
    print("Most frequent trip:", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Calculate and display trip duration statistics.

    Args:
    df (DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time:", total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Calculate and display user statistics.

    Args:
    df (DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts:\n", gender_counts)

    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("Earliest birth year:", earliest_year)
        print("Most recent birth year:", most_recent_year)
        print("Most common birth year:", most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Display rows of data based on user request.

    Args:
    df (DataFrame): The DataFrame containing the bikeshare data.
    """
    start_loc = 0
    while True:
        view_data = input(
            '\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n')
        if view_data.lower() != 'yes':
            break
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5


def main():
    """Main function to control the flow of the program."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

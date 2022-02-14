from curses import raw
import datetime as dt
import time
import pandas as pd
import numpy as np


chicagodata = pd.read_csv('/Users/edwinhuertasfuentes/Edwin/DataAnalytics/Udacity/ProgrammingForDataScience/PythonProject/Data/chicago.csv')
newyorkcitydata = pd.read_csv('/Users/edwinhuertasfuentes/Edwin/DataAnalytics/Udacity/ProgrammingForDataScience/PythonProject/Data/new_york_city.csv')
washingtondata = pd.read_csv('/Users/edwinhuertasfuentes/Edwin/DataAnalytics/Udacity/ProgrammingForDataScience/PythonProject/Data/washington.csv')

# Set a copy of the original csv files to work with
chicago = chicagodata.copy()
newyorkcity = newyorkcitydata.copy()
washington = washingtondata.copy()

# Create dictionary with all 3 cities names city_data
city_data = { 'chicago': chicago,
              'new york city': newyorkcity,
              'washington': washington}


"""
    Asks user to specify a city, month, and day to analyze. 
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
"""

# Get user input to select a city (chicago, new york city, washington)
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. 
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ('chicago', 'new york city','washington') 
    months = ('january','february', 'march','april','may','june','all')
    days = ('monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all')
    while True: 
        city = input('\nPlease select a city from Chicago, New York City or Washington: \n' ).lower()
        if city in cities:
            break
        elif city == 'all':
            break
        else:
            print('{} is not a valid input. please try again and check for extra spaces'.format(city))
            continue          

# Get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nSelect a month from Jan - June. ex. January, February,.. or all: \n').lower()
        if month in months:
            break
        elif month == 'all':
            break
        else:
            print('{} is not a valid input. please try again and check for extra spaces'.format(month))
            continue  

# Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day of the week? ex. all, Monday, Tuesday, etc : \n').lower()
        if day in days:
            break
        elif day == 'all':
            break
        else:
            print('{} is not a valid input. please try again and check for extra spaces'.format(day))
            continue    

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
    df = pd.DataFrame(city_data[city])

# Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# Extract month,day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

# Filter by month if applicable
    if month != 'all':
# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
# Filter by month to create the new dataframe
        df = df[df['month'] == month]

# Filter by day of week if applicable
    if day != 'all':
# Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

# Display the most common month
    df['month'].to_string() != 'month'
    popular_month = df['month'].mode()[0]
    print('Most popular month:\n{}'.format(popular_month))
        
# Display the most common day of week
    if df['day_of_week'].to_string() != 'day_of_week':
        popular_week = df['day_of_week'].mode()[0]
        print('\nMost popular day of the week:\n{}'.format(popular_week))

# Display the most common start hour
    popular_hour = df['hour'].mode()[0] 
    print('\nMost common start hour:\n{}'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
# Display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start station:\n{}'.format(common_start))

# display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nMost common end station:\n{}'.format(common_end))

# Display most frequent combination of start station and end station trip
    com_station = (df['Start Station'] + ',' + df['End Station']).mode()[0]
    print('\nMost frequest combination:\n{}'.format(com_station))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# Display total travel time
    total_travel = pd.to_timedelta(df['Trip Duration'].sum(),unit= 's')
    print('Total travel time:\n{}'.format(total_travel))

# Display mean travel time
    mean_travel = pd.to_timedelta(df['Trip Duration'].mean(),unit= 's')
    print('\nTotal average time:\n{}'.format(mean_travel))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser Type:\n{}'.format(user_types))
    
# Display counts of gender
    if 'Gender' in df:
        gender_type = df['Gender'].value_counts()
        print('\nGender:\n{}'.format(gender_type))

# Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        common_birth = int(df['Birth Year'].mode()[0])
        recent_birth = int(df['Birth Year'].max())
        earlier_birth = int(df['Birth Year'].min())

        print('\nCommon birth year:\n{}'.format(common_birth))
        print('\nEarliest year:\n{}'.format(earlier_birth))
        print('\nRecent year:\n{}'.format(recent_birth))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

# Set up iteration and ask user if they would like to see raw data
def raw_data(df):
    """
ask user if they would like to see raw data from csv files
    """
    i = 0
    rawdata = input("Do you want to see the first five rows of raw data?: ").lower()

    if rawdata == 'yes':
        while i <= df.shape[0] - 1:
            print(df.iloc[i:,:])
            i+= 5
            user_input = input("Do you wish to continue?: ").lower()
            if user_input == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
      
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
print(main)

if __name__ == "__main__":
	main()
from curses import raw
import datetime as dt
import time
import pandas as pd
import numpy as np

chicagodata = pd.read_csv("/Users/edwinhuertasfuentes/Edwin/DataAnalytics/Udacity/ProgrammingForDataScience/PythonProject/Data/chicago.csv")
newyorkcitydata = pd.read_csv("/Users/edwinhuertasfuentes/Edwin/DataAnalytics/Udacity/ProgrammingForDataScience/PythonProject/Data/new_york_city.csv")
washingtondata = pd.read_csv("/Users/edwinhuertasfuentes/Edwin/DataAnalytics/Udacity/ProgrammingForDataScience/PythonProject/Data/washington.csv")

# Set a copy of the original csv files to work with
chicago = chicagodata.copy()
newyorkcity = newyorkcitydata.copy()
washington = washingtondata.copy()

# Create dictionary with all 3 cities names city_data
city_data = {"chicago": chicago,
             "new york city": newyorkcity,
             "washington": washington}

# Get user input to select a city (Chicago, New York City, Washington)
try:
    def get_filters():
        """
        Asks user to specify a city, month, and day to analyze.
        Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """
        cities = ("chicago", "new york city", "washington")
        months = ("january", "february", "march", "april", "may", "june", "all")
        days = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all")
        while True:
            city = input("\nPlease select a city: 'Chicago, New York City or Washington': \n >>>").lower()
            if city in cities:
                break
            elif city == "all":
                break
            else:
                print(f"{city} is not a valid input. please try again and check for extra spaces")
                continue

        # Get user input for month (all, january, february, ... , june)
        while True:
            month = input("\nSelect a Month: \nJan-June ex. June - Type 'all' for all Months: \n >>>").lower()
            if month in months:
                break
            elif month == "all":
                break
            else:
                print(f"{month} is not a valid input. please try again and check for extra spaces..")
                continue

        # Get user input for day of week (all, Monday, Tuesday,...)
        while True:
            day = input("\nSelect a day of the week: \n ex.Monday, Tuesday, etc or 'all': \n >>>").lower()
            if day in days:
                break
            elif day == "all":
                break
            else:
                print(f"{day} is not a valid input. please try again and check for extra spaces")
                continue

        print("-" * 40)
        return city, month, day
except:
    print("Invalid input, please restart code")


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
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month,day of week, and hour from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["hour"] = df["Start Time"].dt.hour

    # Filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        # Filter by month to create the new dataframe
        df = df[df["month"] == month]

    # Filter by day of week if applicable
    if day != "all":
        # Filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Display the most common month
    popular_month = df["month"].mode()[0]
    print(f"Most popular month:\n{popular_month}")

    # Display the most common day of week
    if df["day_of_week"].to_string() != "day_of_week":
        popular_week = df["day_of_week"].mode()[0]
        print(f"\nMost popular day of the week:\n{popular_week}")

    # Display the most common start hour
    popular_hour = df["hour"].mode()[0]
    print(f"\nMost common start hour:\n{popular_hour}")
    print("\nThis took %s seconds." % (round(time.time() - start_time)))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    common_start = df["Start Station"].mode()[0]
    print(f"Most common start station:\n{common_start}")

    # display most commonly used end station
    common_end = df["End Station"].mode()[0]
    print(f"\nMost common end station:\n{common_end}")

    # Display most frequent combination of start station and end station trip
    com_station = (df["Start Station"] + ", " + df["End Station"]).mode()[0]
    print(f"\nMost frequent combination:\n{com_station}")
    print("\nThis took %s seconds." % (round(time.time() - start_time)))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    total_travel = pd.to_timedelta(df["Trip Duration"].sum(), unit="s")
    print(f"Total travel time:\n{total_travel}")

    # Display mean travel time
    mean_travel = pd.to_timedelta(df["Trip Duration"].mean(), unit="s")
    print(f"\nTotal average time:\n{mean_travel}")
    print("\nThis took %s seconds." % (round(time.time() - start_time)))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bike share users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print(f"\nUser Type:\n{user_types}")

    # Display counts of gender
    if "Gender" in df:
        gender_type = df["Gender"].value_counts()
        print(f"\nGender:\n{gender_type}")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        common_birth = int(df["Birth Year"].mode()[0])
        recent_birth = int(df["Birth Year"].max())
        earlier_birth = int(df["Birth Year"].min())

        print(f"\nCommon birth year:\n{common_birth}")
        print(f"\nEarliest year:\n{earlier_birth}")
        print(f"\nRecent year:\n{recent_birth}")
        print("\nThis took %s seconds." % (round(time.time() - start_time)))
        print('-' * 40)


# Set up iteration and ask user if they would like to see raw data
def raw_data(df):
    """
    ask user if they would like to see raw data from csv files
    """
    i = 0
    while i <= df.shape[0] - 1:
        rawdata = input("Would you like to see five rows of raw data?:\n >>>").lower()
        if rawdata == "yes":
            pd.set_option("display.max_columns", 200)
            print(df.iloc[i:, :].head())
            i += 5
            continue
        elif rawdata == "no":
            break
        else:
            print("Invalid entry!")
        # prompt user if they would like to see more data or carry on
        user_input = input("Do you wish to continue?:\n >>>").lower()
        if user_input == "yes":
            print()
        elif user_input == "no":
            break
        elif rawdata == "no":
            continue
        else:
            print(f"{rawdata} is invalid please try again.")


# Main function for the entire program
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        # ask user to restart program
        restart = input("\nWould you like to restart the program? 'Yes' or 'No': \n >>>").lower()
        if restart.lower() == "yes":
            print()
        elif restart.lower() == "no":
            quit()
        else:
            print("\nNot a valid entry! Try again!\n")


if __name__ == "__main__":
    main()

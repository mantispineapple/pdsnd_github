import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ["january", "february", "march", "april", "may", "june", "all"]
WEEK_DATA = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

def get_filters():
    global city, month, day

    city = input("Would you like to explore data for Chicago, New York City or Washington? ").lower()
    #day = input("Which day of the week would you like to explore bikehare data for. Type all to explore no filter data").lower()

    while city not in CITY_DATA:
        print("Oops that is not an appropriate response")
        city = input("Would you like to explore data for Chicago, New York City or Washington? ").lower()
    else:
        month = input("Which month would you like to explore bikeshare data for? Type all to apply no filter data. ").lower()
        day = input("Which day of the week would you like to explore bikeshare data for. Type all to apply no filter data. ").lower()
        if month in MONTH_DATA and day in WEEK_DATA:
            return city, day, month
        elif month not in MONTH_DATA and day in WEEK_DATA:
            print("There was something wrong with your month response. Data will not be filtered by month")
            month = "all"
            return city, day, month
        elif month in MONTH_DATA and day not in WEEK_DATA:
            print("There was something wrong with your response to day of week. Data will not be filtered by day")
            day = "all"
            return city, day, month
        elif month not in MONTH_DATA and day not in WEEK_DATA:
            print("There was something wrong with your response. Data will not be filtered by month or day")
            day = "all"
            month = "all"
            return city, day, month

def load_data(city, month, day):
    global month_num, week_num, df, df2
    filename_chicago = 'chicago.csv'
    filename_nyc =  'new_york_city.csv'
    filename_washington = 'washington.csv'
    month_num = MONTH_DATA.index(month)+1
    week_num = WEEK_DATA.index(day)+1
    df = pd.read_csv(CITY_DATA[city])

    if month_num <= 6:
        df["DOM"] = pd.DatetimeIndex(df["Start Time"]).month
        df = df[df["DOM"] == month_num]
        df1 = df
        if week_num <= 6:
            df1["DOW"] = pd.DatetimeIndex(df1["Start Time"]).weekday
            df2 = df1[df1["DOW"] == week_num]
            return df2
        elif week_num >=7:
            df1["DOW"] = pd.DatetimeIndex(df1["Start Time"]).weekday
            df2 = df1
            return df2
    elif month_num >= 7:
        df["DOM"] = pd.DatetimeIndex(df["Start Time"]).month
        df1 = df
        if week_num <= 7:
            df1["DOW"] = pd.DatetimeIndex(df1["Start Time"]).weekday
            df2 = df1[df1["DOW"] == week_num]
            return df2
        elif week_num >=7:
            df1["DOW"] = pd.DatetimeIndex(df1["Start Time"]).weekday
            df2 = df1
            return df2

def display_data(df2):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no.")
    start_loc = 0
    while view_data == "yes":
        df_display = df2.iloc[start_loc:start_loc + 5]
        print(df_display)
        start_loc += 5
        view_display = input("Do you wish to continue: ").lower()
        if view_display == "no":
            break
        else:
            continue
    else:
        print("Individual trip data will not be displayed")

def time_stats(df2):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_DOM = df2["DOM"].mode()[0]

    common_DOW = df2["DOW"].mode()[0]

    df2["hours"] = pd.DatetimeIndex(df2["Start Time"]).hour
    common_hr = df2["hours"].mode()[0]

    print("The most common hour to travel is {}:00".format(common_hr))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df2):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startstn = df2["Start Station"].mode()[0]

    # display most commonly used end station
    common_endstn = df2["End Station"].mode()[0]

    # display most frequent combination of start station and end station trip
    df2["start_endstn"] = df2["Start Station"]+ "to" + df2["End Station"]
    print(df2.start_endstn.mode().iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df2):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_traveltime = df2["Trip Duration"].sum()


    # display mean travel time
    mean_traveltime = df2["Trip Duration"].mean()

    print("The total travel time is {} and the average trip duration is {}".format(sum_traveltime, mean_traveltime))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df2):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_ut = df2.groupby("User Type").count()

    if "Gender" in df2:
    # Display counts of gender
        count_gender = df2.groupby("Gender").count()

        #print(count_gender)

    else:
        print("Gender Stats cannot be calculated because Gender does not appear in dataset")
# Display earliest, most recent, and most common year of birth
    if "Birth Year" in df2:
        earliest_birth = df2["Birth Year"].min()

        recent_birth = df2["Birth Year"].max()

        common_birth = df2["Birth Year"].mode()[0]

        print("The most recent birth year is {} and the most common birth year is {}".format(recent_birth, common_birth))

    else:
        print("Birth Stats cannot be calculated because Birth Year does not appear in dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#runs all functions created within file
def main():
    while True:
        get_filters()
        load_data(city, month, day)

        display_data(df2)
        time_stats(df2)
        station_stats(df2)
        trip_duration_stats(df2)
        user_stats(df2)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

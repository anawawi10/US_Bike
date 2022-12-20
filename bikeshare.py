import datetime

import pandas as pd
# This is the second project in Udacity Data science Programming Nando degree program

CITY_DATA = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
CITIES = ['chicago', 'new york', 'washington']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday']

N = 60





def get_input(msg, input_list):
    while True:
        y = 1
        print("\n\t ", msg)
        for element in input_list:
            print("\n\t", y, ". ", element, sep='', end='')
            y += 1
        print("\n\t", y, ". All ", sep='', end='')
        print("\n\t Enter Name :", end='')

        name = (input())
        if name in input_list:
            user_data = name
            break
        elif name.lower() == 'all':
            user_data = name
            break

    return user_data


def get_choices():
    while True:
        print(" Available Cities are : \n 1. Chicago\n 2. New York\n 3. Washington")

        city = input("\nEnter name of City : ")

        if city.lower() in CITIES:
            break

    month = get_input('Select Month ', MONTHS)

    day = get_input('Select Day of Week ', DAYS)
    print('-' * N)
    return city.lower(), month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    print('\n<<<<The Most Popular Times of Travel>>>>\n')

    most_common_month = df['month'].value_counts().idxmax()
    month = datetime.datetime.strptime(str(most_common_month), '%m').strftime('%B')
    print("The most common month is :", month)

    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    most_common_start_hour = df['hour'].value_counts().idxmax()
    hour = datetime.datetime.strptime(str(most_common_start_hour), '%H').strftime('%I %p')
    print("The most common start hour of day is :", hour)
    print('-' * N)


def station_stats(df):
    print('\n<<<The Most Popular Stations and Trip>>>' + '\n')

    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :",
          most_common_start_station)

    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    most_common_start_end_station = (df.groupby(['Start Station', 'End Station'])
                                     .size()
                                     .nlargest(1)
                                     .index.remove_unused_levels()
                                     .tolist()
                                     )
    print("The most commonly used start station and end station : {}, {}".format((most_common_start_end_station[0])[0],
                                                                                 (most_common_start_end_station[0])[1]))
    print('-' * N)


def trip_duration_stats(df):
    print('\n<<<Trip Duration>>>\n')

    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    mean_travel = df['Trip Duration'].mean()
    print("Average travel time :", mean_travel)


def user_stats(df):
    print('\n<<<User Information>>>\n')

    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()

    for index, user_count in enumerate(user_counts):
        print(" {}: {}".format(user_counts.index[index], user_count))
    print()
    if 'Gender' in df.columns:
        user_stats_gender(df)
    if 'Birth Year' in df.columns:
        user_stats_birth(df)
    print('-' * N)


def user_stats_gender(df):
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()

    for index, gender_count in enumerate(gender_counts):
        print(" {}: {}".format(gender_counts.index[index], gender_count))
    print()


def individual_data(df):

    start_data = 0
    end_data = 5
    df_length = len(df.index)

    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no' : ")
        if raw_data.lower() == 'yes':
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break


def user_stats_birth(df):
    birth_year = df['Birth Year']
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)

    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)

    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)


def main():
    while True:
        city, month, day = get_choices()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_data(df)
        restart = input('\n Do you want to rerun the program? (yes/no) ')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

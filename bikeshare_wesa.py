#Function IMPORT
from datetime import datetime
from pathlib import Path

import pandas as pd

    
def import_data(filenames):
    #Import Module
    ''' This module imports the data into a dataframe and creates new columns for the functions.
    Args: csv Files
    Out: dataframe'''
    print('Fetching data, please wait... \n'
          'and Yes I know, it takes a while \n'  )


    #Data Grabber

    df = pd.DataFrame()
    for f in filenames:
        data = pd.read_csv(f, parse_dates=["Start Time", "End Time"])
        data["City"] = f.stem 
        df = df.append(data )
    
    return df

def extend_data(df):
    df = df.copy()
    # Data Frame Extention and Data Manipulation     
    df["Trip Duration"] = df["Trip Duration"] #.round().astype("int32")     # Round values to seconds
    df['month'] = df['Start Time'].dt.strftime("%B")                      # Create month column
    df['day'] = df['Start Time'].dt.day                                   # Creat day column 
    df['hour'] = df['Start Time'].dt.hour                                 # Create hour column
    df['day_of_week'] = df['Start Time'].dt.day_name()                    # Create Day of Week column
    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')  # Concats Start to End Station to creates journey
    pd.set_option('max_colwidth', 100)                                    #Column width extention -> for journey

    # Relabeling Columns
#    df.columns = [col.replace(' ', '_').lower() for col in df.columns]
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels
    return df

#filter_options = [
#    ()
#]

def filter_by_choice(df, column, choices, readable, input_type_function):
    # column = 'city'
    # choices = ['chicago', 'new_york_city', 'washington','none']
    # readable = 'day of week'
    # input_type_function
    
    filter_desc = None

    while True:
        input_string = input('\nPlease select {}\n'.format(readable) +
                             'Choices: ' + ', '.join([str(choice) for choice in choices]) +
                             '\nPress enter if you dont want to filter.\n')
        
        if len(input_string) == 0:
            break
        
        # can be int or str or float etc.
        try:
            input_data = input_type_function(input_string)
            assert(input_data in choices)
        except:
            print('Please pay attention to the spelling and try again')
            continue
        
        filter_options = df[column] == input_data
        filter_desc = readable + ': ' + input_string

        df = df.loc[filter_options]
        break

    
    return df, filter_desc

def filter_data(df):
    filter_descriptions = list()
    
    column = 'city'
    choices = ['chicago', 'new_york_city', 'washington']
    readable = column
    input_type_function = lambda arg: str(arg).lower()
    df, filter_desc = filter_by_choice(df, column, choices, readable, input_type_function)
    if filter_desc:
        filter_descriptions.append(filter_desc)
    
    column = 'user_type'
    choices = ['Subscriber', 'Customer']
    readable = 'user type'
    input_type_function = lambda arg: str(arg).lower()
    df, filter_desc = filter_by_choice(df, column, choices, readable, input_type_function)
    if filter_desc:
        filter_descriptions.append(filter_desc)

    column = 'month'
    choices = ['January', 'February', 'March', 'April', 'May', 'June']
    readable = column
    input_type_function = lambda arg: str(arg).capitalize()
    df, filter_desc = filter_by_choice(df, column, choices, readable, input_type_function)
    if filter_desc:
        filter_descriptions.append(filter_desc)

    column = 'day'
    choices = list(range(1, 32))
    readable = 'day of month'
    input_type_function = int
    df, filter_desc = filter_by_choice(df, column, choices, readable, input_type_function)
    if filter_desc:
        filter_descriptions.append(filter_desc)

    column = 'day_of_week'
    choices = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    readable = column
    input_type_function = lambda arg: str(arg).capitalize()
    df, filter_desc = filter_by_choice(df, column, choices, readable, input_type_function)
    if filter_desc:
        filter_descriptions.append(filter_desc)

    filter_description = ', '.join(filter_descriptions)
    
    return df, filter_description

def seconds_to_hours_minutes_seconds(seconds):
    hours = int(seconds)
    minutes = (seconds*60) % 60
    seconds = (seconds*3600) % 60
    return hours, minutes, seconds

def show_statistics(df_filtered):
    #Statistic Module

    ''' Within this module the statics were displayed, based on the filtered dataframe.
        Args: Filtered Dataframe, Filters
        Out: Statistics'''


    print('\nStatistics \n')
    
    print('Number of records: {}'.format(df_filtered.index.size))


    #1 Popular times of travel (i.e., occurs most often in the start time)
    #1.1 most common month
    popular_month = df_filtered['month'].mode()[0]
    print('\nMost popular month:', popular_month)
    #1.2 most common day of week
    popular_hour = df_filtered['hour'].mode()[0]
    print('Most popular hour:', popular_hour)
    #1.3 most common hour of day
    popular_day = df_filtered['day_of_week'].mode()[0]
    print('Most popular day of the week:', popular_day, "\n")

    #2 Popular stations and trip
    #2.1 most common start station
    pop_start = df_filtered['start_station'].mode()[0]
    print('Most popular start station: {}.'.format(pop_start))

    #2.2 most common end station
    pop_end = df_filtered['end_station'].mode()[0]
    print('Most popular end station: {}.'.format(pop_end))

    #2.3 most common trip from start to end (i.e., most frequent combination of start station and end station)
    pop_journey = df_filtered['journey'].mode()[0]
    print('Most popular trip: {}.'.format(pop_journey),"\n")


    #3 Trip duration
    #3.1 total travel time
    total_travel_time = df_filtered['trip_duration'].sum()/3600
    tot_hours, tot_minutes, tot_seconds = seconds_to_hours_minutes_seconds(total_travel_time)
    print("Total travel time: %d:%02d:%02d" % (tot_hours, tot_minutes, tot_seconds), "hours")

    #3.2 average travel time
    avg_travel_time = df_filtered['trip_duration'].mean()/3600
    avg_hours, avg_minutes, avg_seconds = seconds_to_hours_minutes_seconds(avg_travel_time)
    print("Average trip duration: %d:%02d:%02d" % (avg_hours, avg_minutes, avg_seconds), "hours","\n")


    #4 User info
    #4.1 counts of each user type
    subscriber_count = df_filtered.query('user_type == "Subscriber"').index.size
    customer_count = df_filtered.query('user_type == "Customer"').index.size
    print('There are {} subscribers and {} customers.'.format(subscriber_count, customer_count))

    #4.2 Counts of each gender (only available for NYC and Chicago)
    male_count = df_filtered.query('gender == "Male"').index.size
    female_count = df_filtered.query('gender == "Female"').index.size
    nan_count = df_filtered.query('gender.isnull()').index.size
    print('There are {} male users and {} female users (no data for {} users).'.format(male_count, female_count, nan_count))

    #4.3 earliest, most recent, most common year of birth (only available for NYC and Chicago)
    if df_filtered.query('birth_year.notnull()').index.size > 0:
        popular_birth = df_filtered['birth_year'].mode()[0]
        print('Most common year of birth:', int(popular_birth))
        oldest_birth = df_filtered['birth_year'].min()
        print('Oldest user was born:', int(oldest_birth))
        youngest_birth = df_filtered['birth_year'].max()
        print('Youngest user was born:', int(youngest_birth))
    else:
        print('(DOB not available in filtered data)')

def show_raw_data(df, column_count):
    i = 0
    while True:
        input_string = input('Do you want to display raw data? If so, press Y.')
        if input_string.lower() != 'y':
            break
            
        print(df[df.columns[1:column_count]].iloc[i:i+5])
        
        i += 5
    
        
def main():
    files_csv = Path.cwd().glob('*.csv')

    df_original = import_data(files_csv)
    column_count_original = len(df_original.columns)

    df = extend_data(df_original)

    while True:
        df_filtered, filter_description = filter_data(df)
        print('You filtered for:' + filter_description)
        show_statistics(df_filtered)
        show_raw_data(df_filtered, column_count_original)

        restart = input("\nWould you like to restart? Please type 'y' for yes or anything else for no.")
        
        if restart != 'y':
            print('Bye bye')
            break

    return df
   
    
if __name__ == "__main__":
    df = main()    



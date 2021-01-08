# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import time
import streamlit as st
st.title('Capstone Project')

def filter_data(city, data_filter, Month, Day):
    """
    Loads data for the specified city and filters by month and/or day if applicable.

    INPUT/ARGS:
        (str) city - name of the city to analyze.
        (str) data_filter - type of filter to apply to raw data (month only, day only, both or none).
        (str) month - name of the month to filter by, if filter is month only or both.
        (str) day - name of the day of week to filter by, if filter is day only or both.
    BODY: Reads data from .csv file, converts the time/date column to python datetime format, and filters
          data by specified filter type.
    OUTPUT/RETURNS:
        df - Pandas DataFrame containing city data filtered by month and/or day, or none.
    """
    directory = 'C:/Users/The Presence/Documents/Personal Document/Personal Development/Data Science and Analytics/Udacity (Python Course)/Labs Tasks-20200924T221854Z-001/Lab Results/Capstone Project/bikeshare-2/' + city 
    df = pd.read_csv(directory)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Months'] = df['Start Time'].dt.month_name(locale='English')
    df['Days'] = df['Start Time'].dt.day_name(locale='English')
    df['Hours'] = df['Start Time'].dt.hour
    if data_filter == 'None':
        df = df
    elif data_filter == 'Month':
        spef_mon = Month
        df_month = df[df.Months == spef_mon]
        df = df_month
    elif data_filter == 'Day':
        spef_day = Day
        df_day = df[df.Days == spef_day]
        df = df_day
    elif data_filter == 'Both':
        spef_mon, spef_day = Month, Day
        df_month = df[df.Months == spef_mon]
        df_month_day = df_month[df_month.Days == spef_day]
        df = df_month_day
    return(df)

def stats(df):
    """
    Seciton 1: Displays statistics on the most frequent times of travel.
    Section 2: Displays statistics on the most popular stations and trip.
    Section 3: Displays statistics on the total and average trip duration.
    Section 4: Displays statistics on bikeshare users.
    
    OUTPUT/RETURN: section_1, section_2, section_3, seciton_4 - Panda DataFrame showing the various statistics.
    """
    mc_mon = df['Months'].value_counts().idxmax()
    mc_day = df['Days'].value_counts().idxmax()
    mc_hour = df['Hours'].value_counts().idxmax()
    section_1 = {'Most Common Month': [mc_mon], 'Most Common Day': [mc_day], 'Most Common Hour': [mc_hour]}
    section_1 = pd.DataFrame(section_1, index=[1])
    
    mc_stat = df['Start Station'].value_counts().idxmax()
    mc_end = df['End Station'].value_counts().idxmax()
    df['Route'] = df['Start Station'] + ' - ' + df['End Station']
    mc_route = df['Route'].value_counts().idxmax()
    section_2 = {'Most Common Start Station': [mc_stat], 'Most Common End Station': [mc_end], 'Most Common Route': [mc_route]}
    section_2 = pd.DataFrame(section_2, index=[1])
    
    df['Trip Duration (Mins)'] = df['Trip Duration']/60
    tot_dur = np.sum(df['Trip Duration (Mins)'])
    ave_dur = np.mean(df['Trip Duration (Mins)'])
    section_3 = {'Total Travel Time (Mins)': [tot_dur], 'Average Travel Time (Mins)': [ave_dur]}
    section_3 = pd.DataFrame(section_3, index=[1])
    
    if 'Gender' in df and 'Birth Year' in df:
        user_t = dict(df['User Type'].value_counts())
        gend = dict(df['Gender'].value_counts())
        section_4 = {**user_t, **gend}
        section_4 = pd.DataFrame(section_4, index=[1])
        section_4['Earliest Birth Year'], section_4['Most Recent Birth Year'] = np.min(df['Birth Year']), np.max(df['Birth Year'])
        mc_by = df['Birth Year'].value_counts().idxmax()
        section_4['Most Common Birth Year'] = mc_by
    else:
        user_t = dict(df['User Type'].value_counts())
        section_4 = pd.DataFrame(user_t, index=[1])
        
    return(section_1, section_2, section_3, section_4)

def get_month_day (data_filter):
    if data_filter == 'Month':
        print('Which month - January, February, March, April, May, or June?')
        mnth = st.sidebar.selectbox('Select Month', ('January', 'February', 'March', 'April', 'May', 'June'))
        dy = '' 
    elif data_filter == 'Day':
        mnth = ''
        dy = st.sidebar.selectbox('Select Day', ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
    elif data_filter == 'Both':
        mnth = st.sidebar.selectbox('Select Month', ('January', 'February', 'March', 'April', 'May', 'June'))
        dy = st.sidebar.selectbox('Select Day', ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
    elif data_filter == 'None':
        mnth, dy = '', ''
    return(mnth, dy)

#Interactive Section: Takes user input, to decide whether to compute the statistics or not.
st.sidebar.write('Hello! Would you like to see Statistical Breakdown of Bike Share Data?')
cty = st.sidebar.selectbox('Select Filename', ('chicago.csv', 'new_york_city.csv', 'washington.csv'))
data_filter = st.sidebar.selectbox('Select Data Filter', ('Month', 'Day', 'Both', 'None'))
mnth, dy = get_month_day(data_filter)

st.write('\nCity: ({}), Filter: ({}), Month: ({}), Day: ({})'.format(cty, data_filter, mnth, dy))
start_time = time.time()
data_frame = filter_data(cty, data_filter, mnth, dy)
st.write("\nIt took {} second(s) to load and filter the raw data of {} size." .format((time.time() - start_time), data_frame.shape))
start_time = time.time()
section_1, section_2, section_3, section_4 = stats(data_frame)
st.write("\nIt took %s second(s) to calculate the needed Statistical Data." % (time.time() - start_time))
st.write('\nSecion 1:\n', section_1)
st.write('\nSecion 2:\n', section_2)
st.write('\nSecion 3:\n', section_3)
st.write('\nSecion 4:\n', section_4)
       
#Interactive Section: Takes user input, to decide whether to display raw data or not.
city = st.sidebar.selectbox('View Raw Data\nSelect Filename', ('chicago.csv', 'new_york_city.csv', 'washington.csv'))
end_row = st.sidebar.slider('Select number of rows to display', 5, 100) 
filename = cty + '.csv'
directory = 'C:/Users/The Presence/Documents/Personal Document/Personal Development/Data Science and Analytics/Udacity (Python Course)/Labs Tasks-20200924T221854Z-001/Lab Results/Capstone Project/bikeshare-2/' + city 
df = pd.read_csv(directory)
st.write('\n', df[:end_row])
        




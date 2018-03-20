# import modules and system

import matplotlib.pyplot as plt
import seaborn as sns
import time
import math
import pandas as pd
from datetime import datetime
from statistics import mode
import numpy as np
import os
import fnmatch
#PATH = os.getcwd() + "/"

# get the .csv file from the directory

def get_csv_file(city):
    for file in os.listdir( os.getcwd()):
        if fnmatch.fnmatch(file, city + '.csv'): return 1

# Convert .csv file to pandas dataframe
# Insert columns: Start Day, Start Month & Full Trip 

def load_file(city):
    data_file_found = get_csv_file(city)
    
    if data_file_found > 0:
        #data_file_path = PATH+city+".csv"
        #data_file_path = "./"+city+".csv"
        city_csv_to_df = pd.read_csv('./chicago.csv') #pd.read_csv(data_file_path)
        df = pd.DataFrame(city_csv_to_df)
        df.iloc[:,1:3] = df.iloc[:,1:3].apply(pd.to_datetime, errors = 'coerce')
        df['Start Day'] = df['Start Time'].dt.weekday_name
        df['Start Month'] = df['Start Time'].dt.month
        df['Full Trip'] = df[['Start Station', 'End Station']].apply(lambda x: ' to '.join(x), axis = 1)
        return df
    else:
        print("We currently do not have data for the city that you requested")
        return -1
# Ask user for the city. If the input does not match the list of cities, a quit option is given after 3 failed attempts.
def get_city():
    
    i = 0
    lst = ['chicago', 'new york', 'washington']
    
    print("Hello! Let's explore some US bikeshare data!")
    
    while (i <=3):
        i += 1
        city = input('Please select from the following cities: Chicago, New York, or Washington?\n')
        
        if not (city.lower() in lst):
            print('\nSorry could not process!! Please check the spelling and try again\n ')
            if (i == 3):
                quit = input('\nDo you want to comeback later? Y/N: \n')
                if quit.lower() == 'n':
                    i = 0
                else:
                    print('Thank you for visiting! Have a great day!!')
                    break
        else:
            print('You have selected {}'.format(city))
            break
        
    return city  

 
# Ask user for the time period. If the input does not match the list of time period, a quit option is given after 3 failed attempts.
def get_time_period():
    i=0
    lst = ['month', 'day', 'both', 'none']

    while (i<=3):
        i += 1
        time_period = input('\nWould you like to filter the data by Month, Day, Both or None\n')

        if not ((time_period.lower())in lst):
            if (i == 3):
                quit = input('\nDo you want to comeback later? Y/N: ')
                if (quit).lower() == 'n':
                    i = 0
                else:
                    print('Thank you for visiting! Have a great day!!')
                    return time_period
                
        else:
            print('You have selected {}'.format(time_period))
            return time_period


# Ask user for the month. If the input does not match the list of months, a quit option is given after 3 failed attempts.        
def get_month():

    i =0
    lst = [1,2,3,4,5,6]

    while (i<=3):
        i += 1

        try:
            month = int(input('\nChoose a month as an integer - January:1, February:2, March:3, April:4, May:5, June:6\n'))
        except ValueError:
            print('\nPlease enter an integer corresponding to the month\n')  
        else:
            if not (month in lst):
                if (i == 3):
                    quit = input('\nDo you want to come back later? Y/N: ')
                    if (quit).lower() == 'n':
                        i=0
                    else:
                        print("Thank you for visiting! Have a great day!!")
                        return month
                    
            else:
                print('You have selected {}'.format(month))
                return month
                    
        
        
# Ask user for the day. If the input does not match the list of day, a quit option is given after 3 failed attempts.
def get_day():
    i=0
    lst = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


    while (i<=3):
        i+=1
        day = input('\nPlease Select a day of the week - Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday\n')

        if not((day.lower()) in lst):
            if (i == 3):
                quit = input('\nDo you want to comeback later? Y/N: ')
                if (quit).lower() == 'n':
                    i = 0
                else:
                    print("Thank you for visiting! Have a great day!!")
                    return day
                    
        else:
            print('You have selected {}'.format(day))
            return day
        
 # Visualization input       
        quit = input('\nDo you want to check out some cool charts? Y/N: ')
        if quit.lower() == 'n':
            print("Thanks for visiting us")
        else:
            show_bikeshare_charts(city_data)
def get_insights(city, time_period, month, day):
    
    if city == "new york":
        city="new_york_city"
 
    city_data = load_file(city)
    
    if (time_period).lower() == 'month':
        city_data = city_data.loc[(city_data['Start Month'] == month)]
    elif (time_period).lower() == 'day':
        city_data = city_data.loc[(city_data['Start Day'] == day)]
    elif (time_period).lower() == 'both':
        city_data = city_data.loc[(city_data['Start Month'] == month) & (city_data['Start Day']== day)]
    elif (time_period).lower() == 'none':
        city_data = load_file(city)
    return city_data
# Stats
def show_data_points_non_visual(city_data):
    
    #city_data = get_insights(city, time_period, month, day)
   
    # Print Data Analysis
    print('Most Popular Trip for your filter is: {}'.format(str(city_data['Full Trip'].mode())))  
    print('Most Popular Hour for your filter is: {}:00'.format(int(city_data['Start Time'].dt.hour.mode())))
    print('Most Popular Day for your City is: {}'.format(str(city_data['Start Time'].dt.weekday_name.mode()))) 
    print('Total Trip Duration for your filter is: {}'.format((city_data['Trip Duration'].cumsum(axis = 0)).iloc[-1]))  
    print('Average Trip Duration for your filter is {}'.format((city_data['Trip Duration'].cumsum(axis = 0)).iloc[-1]/(len(city_data['Trip Duration']))))
   
    if 'Birth Year' in city_data:
        print('Popular Birth Year for your filter is: {}'.format(int(city_data['Birth Year'].mode())))
        print('Youngest person birth year is: {}'.format(int(city_data['Birth Year'].max())))
        print('Oldest person birth year is: {}'.format(int(city_data['Birth Year'].min())))
    else:
        print("The City data does not include birth year data")
    return 1
# Visualizations
def show_bikeshare_charts(city_data):

    # Following visualizations will be generated for the cities which has data of Birth Year 

    # Bar chart for the User Type of the city
    sns.factorplot('User Type', data = city_data, kind='count')
    plt.xlabel('User Type', fontsize=14)
    plt.title("Customer Vs Subscriber Data",fontsize=16)
    ax = plt.gca()
    ax.axes.get_yaxis().set_visible(False)
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width()/2., p.get_height(),'%d' % int(p.get_height()), fontsize=12, ha='center',va='bottom')
    plt.show()

    # Pie chart for User Type of the city
    city_data['User Type'].value_counts().plot(kind='pie', autopct='%1.1%%f')
    plt.axis('equal')
    plt.title('User Type',fontsize=16)

    # Ridership for the Days of the Week
    sns.factorplot('Start Day', data=city_data, kind='count',order=['Sunday','Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], size=8 )
    plt.xlabel('Weekday', fontsize=14)
    plt.title("Ridership for the Days of the Week",fontsize=16)
    ax = plt.gca()
    ax.axes.get_yaxis().set_visible(False)
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width()/2., p.get_height(),'%d' % int(p.get_height()), fontsize=12, ha='center',va='bottom')
    plt.show()

    # Following visualization will be generated for the cities which has data for Gender
    if 'Gender' in city_data:
        sns.factorplot('Gender', data=city_data, kind='count', size=8 )
        plt.xlabel('Gender', fontsize=14)
        plt.title("Bike Share Gender Data", fontsize=16)
        ax = plt.gca()
        ax.axes.get_yaxis().set_visible(False)
        for p in ax.patches:
            ax.text(p.get_x() + p.get_width()/2., p.get_height(),'%d' % int(p.get_height()), fontsize=12, ha='center',va='bottom')
        plt.show()

def main():
    none = ''
    city = get_city()
    time_period = get_time_period().lower()
    
    if time_period == 'both':
        month = get_month()
        day = get_day()
    elif time_period == 'month':
        month = get_month()
        print(month) 
    elif time_period == 'day':
        day = get_day()

    print('Calculating....')
    
    if (len(city) > 0): #and len(time_period) > 0 and  month > 0 and len(day) > 0):
        city_data = get_insights(city, time_period=none, month=0, day=none)
        show_data_points_non_visual(city_data)

main()
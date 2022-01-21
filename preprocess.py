from lib2to3.pgen2.pgen import DFAState
import streamlit as st
import numpy as np
import seaborn as sn
import pandas as pd
import re


def gettimeanddate(string):
    string = string.split(',')
    date, time = string[0], string[1]
    time = time.split('-')
    time = time[0].strip()

    return date+" "+time

def getstring(text):
    return text.split('\n')[0]

def preprocess(data):

# '1/29/19, 11:41 - Amaan Cr: Guys there is no class of english today.'
# it will break the time&Date and msg into different column -> messages & dates
# time format is 24-hrs
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

# convert it into pandas library and rename 
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    df['message_date'] = df['message_date'].apply(lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)


# now, in msg part there are two more different attribute
# 1-name 2- msg 
    users = []
    messages = []

    for message in df['user_messages']:

        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['User'] = users
    df['message'] = messages




    df['message'] = df['message'].apply(lambda text: getstring(text))

    df = df.drop(['user_messages'], axis=1)
    df = df[['message', 'date', 'User']]

    df = df.rename(columns={'message': 'Message','date': 'Date'})

    
    # data preprocess and time furtherly divide
    df['Only_date'] = pd.to_datetime(df['Date']).dt.date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['Date']).dt.day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute


    period = []
    for hour in df[['Day_name', 'Hour']]['Hour']:

            if hour == 23:
               period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
               period.append(str('00') + "-" + str(hour + 1))
            else:
               period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df 
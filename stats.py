from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

import emoji
extract = URLExtract()


def fetchstats(selected_user, df):

    # if the selected user is a specific user,then make changes in the dataframe,else do not make any changes
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['Message']:
        words.extend(message.split())

    # counting the number of media files shared
    mediaommitted = df[df['Message'] == '<Media omitted>']

    # number of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), mediaommitted.shape[0], len(links)

# 2- most busy users {group level}
def fetchbusyuser(df):

    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()

    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, newdf

# 3-
def createwordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=250, min_font_size=10, background_color='white')

    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc

# 4- get most common words,this will return a dataframe of most common words
def getcommonwords(selecteduser, df):

    # getting the stopwords
    file = open('stop_hinglish.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df[(df['User'] != 'Group Notification') |
              (df['User'] != '<Media omitted>')]

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon

# 5-
def getemojistats(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf

# 6-
def monthtimeline(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))

    temp['Time'] = time
    return temp

# 8-
def monthactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Month'].value_counts()

def weekactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Day_name'].value_counts()

# 7-
def daily_timeline(selecteduser,df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
        
    daily_timeline = df.groupby('Only_date').count()['Message'].reset_index()

    return daily_timeline

# 9-
def activity_heatmap(selecteduser,df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    # hour-> period
    user_heatmap = df.pivot_table(index='Day_name', columns='period', values='Message', aggfunc='count').fillna(0)
    return user_heatmap
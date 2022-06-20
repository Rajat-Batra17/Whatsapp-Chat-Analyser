
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract=URLExtract()

# FIRST FUNCTION----> TO TELL ABOUT THE BASIC STATS LIKE NO. OF WORDS,MESSAGES,LINKS AND MEDIA

def fetch_stats(selected_user,df):

    # IF NOT OVERALL GROUP/CHAT, WE HAVE TO SELECT MESSAGES OF PARTICULAR PERSON FROM MESSAGE COLUMN
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] #means all those rows of where user ==selected user

        # fetch the number of messages
    num_messages = df.shape[0] #no of rows

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split()) # splitting by space

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0] # whereever media omitted written in msg

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links);

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df


def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    # FIRSTLY WILL REMOVE GROUP NOTIFICATION
    # THEN MEDIA OMITTED
    # THEN STOP WORDS

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df




# EMOJI ANALYSIS

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = [] # empty list
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']]) # using emoji library

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))) #  converting to dataframe

    return emoji_df


# TO HAVE MONTH WISE TIMELINE
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index() # making data frame
    # year month_number month_name  message( denotes no of msg at particular  given time)

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
   # July-2022 ; in this form

    timeline['time'] = time #new column added of time

    return timeline;

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
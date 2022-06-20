# IMPORTING IMPORTANT FILES
import streamlit as st;
import preprocessor,helper
import matplotlib.pyplot as plt;
import seaborn as sns
import time

st.set_page_config(
     page_title="Rajat's App",
     page_icon="👑",
     layout="wide",
     initial_sidebar_state="expanded",
 )


#st.text("Please upload whatsapp chat in 24 hour format")
#st.text("Date format == month/date/year")
# GIVING TITLE
st.sidebar.title("Made by Rajat ❤")
st.sidebar.subheader("Email : rajatbatra.engr@gmail.com")
st.sidebar.subheader("Phone: 8199064120")
st.sidebar.subheader("Linkedin: https://www.linkedin.com/in/rajat-batra-5389081b1/")
st.sidebar.title("Whatsapp Chat Analyzer")
st.info('( Supported Format: Time -> 24 hours &  Date -> month/date/year )')
#st.snow()



# TO HAVE THE OPTION TO UPLOAD FILE
uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    st.success('File uploaded successfully. Click on Show Analysis button to get detailed report ')
    bytes_data = uploaded_file.getvalue() # STREAM OF BYTES
    data = bytes_data.decode("utf-8")     # CONVERTING TO STRING USING ENCODING UTF-8
    # st.text(data)
    df = preprocessor.preprocess(data);   # CREATING DATA-FRAME
    #st.dataframe(df)                      # PRINTING DATA-FRAME ON SCREEN

     # STEP: FETCH NEW USERS

     # 1. TAKE UNIQUE USERS
     # 2. SORT USERS
     # 3. REMOVE GROUP NOTIFICATIONS
     # 4. BRING OVERALL TO TOP

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

# CREATING DROP DOWN MENU
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        st.title('Your Personalised Detailed Chat Analysis')
        # HERE WE ARE SHOWING SOME STATISTICS , LIKE NUMBER OF MESSAGES,LINKS,WORDS AND MEDIA

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

#-> TOTAL MESSAGES , TOTAL WORDS, TOTAL MEDIA, TOTAL LINKS;
#st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

# DEFINING 4 COLUMS BASICALLY

        with col1: # NUMBER OF MESSAGES
            st.header("Total Messages")
            st.title(num_messages)

        with col2:# NUMBER OF WORDS
            st.header("Total Words")
            st.title(words)

        with col3: #NUMBER OF MEDIA FILES, <here written as media omitted>
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4: #NUMBER OF LINKS USING URL EXTRACTOR LIBRRAY
            st.header("Links Shared")
            st.title(num_links)


        # Finding the busyies user in the group( group level)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots() # Create just a figure and only one subplot
            col1, col2 = st.columns(2)

       # used to draw multiple plots in same figure
            with col1:
              ax.bar(x.index, x.values, color='red')
              plt.xticks(rotation='vertical')
              plt.ylabel("Number of messages")
              plt.xlabel("Users")
              st.pyplot(fig)

            with col2:
              st.dataframe(new_df)

        # WORDCLOUD GENERATION:

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df) # RETURNS AN IMAGE
        fig, ax = plt.subplots() # WHATEVER WE WILL DO WITH AX, WILL BE SHOWN PN FIGURE
        ax.imshow(df_wc)
        st.pyplot(fig)

      # MOST COMMON WORDS

        most_common_df = helper.most_common_words(selected_user, df) # WE GET A DF
        #st.dataframe(most_common_df)
        # WHERE FIRST COLUMN IS THE WORD AND SECOND IS THE COUNT
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        plt.ylabel("Words")
        plt.xlabel("Frequency")
        st.title('Most commmon words')
        st.pyplot(fig)

     # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

      # FOR ACTIVITY MAP

        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            plt.title("Most busy day")
            plt.ylabel("Number of messages")
            plt.xlabel("Day")
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            plt.title("Most busy month")
            plt.ylabel("Number of messages")
            plt.xlabel("month")
            st.pyplot(fig)


 # Emoji Analysis
            # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


 # HEAT MAP

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
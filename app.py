import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

# this is for uploading a file
uploaded_file = st.sidebar.file_uploader("Choose a file")

# if we choose the file, must not null then proceed
if uploaded_file is not None:         
    bytes_data = uploaded_file.getvalue()

    # converting the bytecode to the text-file
    data = bytes_data.decode("utf-8")

    # sending the file data to the preprocess function for further functioning
    df = preprocess.preprocess(data)

    # displaying the dataframe
    # st.dataframe(df)

    # fetch unique users
    user_list = df['User'].unique().tolist()
    # removing the groupnotification
    user_list.remove('Group Notification')
    # organinsing things
    user_list.sort()
    # including overall,this will be responsible for showcasing the  overall chat group analysis
    user_list.insert(0, "Overall")


    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)
    st.title("WhatsApp Chat Analysis for " + selected_user)
    
    if st.sidebar.button("Show Analysis"):

        # getting the stats of the selected user from the stats script
        num_messages, num_words, media_omitted, links = stats.fetchstats(selected_user, df)

        # 1-- first phase is to showcase the basic stats like number of users,number of messages,number of media shared and all,so for that i requrire the 4 columns
        # col1, col2, col3, col4 = st.beta_columns(4)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total No.of Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(media_omitted)

        with col4:
            st.header("Total Links Shared")
            st.title(links)




        # 2-- finding the busiest users in the group
        if selected_user == 'Overall':

            # dividing the space into two columns
            # first col is the bar chart and the second col is the dataframe representing 

            st.title('Most Busy Users')
            busycount, newdf = stats.fetchbusyuser(df)
            fig, ax = plt.subplots()
            # col1, col2 = st.beta_columns(2)
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(busycount.index, busycount.values, color='blue')
                plt.xticks(rotation='horizontal')
                st.pyplot(fig)
 
            with col2:
                st.dataframe(newdf)




        # 3-- Word Cloud
        st.title('Word Cloud')
        df_img = stats.createwordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)




        # 4-- most common words in the chat
        most_common_df = stats.getcommonwords(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='horizontal')
        st.title('Most commmon words')
        st.pyplot(fig)




        # 5-- Emoji Analysis
        emoji_df = stats.getemojistats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']

        st.title("Emoji Analysis")

        # col1, col2 = st.beta_columns(2)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
        #     fig,ax = plt.subplots()
        #     ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        #     st.pyplot(fig)
        # # with col3:
            emojicount = list(emoji_df['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)




        # 6-- Monthly timeline
        st.title("Monthly Timeline")
        time = stats.monthtimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='blue')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)



        # 7-- daily timeline 
        st.title("Daily Timeline")
        daily_timeline = stats.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Only_date'], daily_timeline['Message'], color='blue') #
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)



        # 8-- Activity maps
        st.title("Activity Maps")

        # col1, col2 = st.beta_columns(2)
        col1, col2 = st.columns(2)

        with col1:

            st.header("Most Busy Day")

            busy_day = stats.weekactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.header("Most Busy Month")
            busy_month = stats.monthactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)



        # 9-- heatmap weekly activity
        st.title("Weekly Activity Map")
        user_heatmap = stats.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
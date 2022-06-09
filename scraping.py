import streamlit as st
import snscrape.modules.twitter as sns
import pandas as pd

tweets_list = []
st.sidebar.image("https://pbs.twimg.com/amplify_video_thumb/1488571141220409349/img/dWUrn3KC7oVNBqgr?format=jpg&name=large")
st.sidebar.title("Tweets on a click")
pd.set_option('display.max_columns', None)
Searc_Key_Word = st.sidebar.text_input("Enter a key word for search")
start_Date=st.sidebar.date_input("Search from Date")
End_Date=st.sidebar.date_input("Search till Date")
if start_Date == End_Date:
    st.sidebar.caption("Please select Different Dates")

range=st.sidebar.number_input("Enter the Count of data to extract",0,1000,1)
val=st.sidebar.title(range)
butt=st.sidebar.button("Submit")
# st.sidebar.download_button(
#      label="Download data as CSV",
     # data=csv,
     # file_name='large_df.csv',
     # mime='text/csv',
 # )
data_scrap=f'{Searc_Key_Word} since:{start_Date} until:{End_Date}'
if butt==True:
    st.title("#Tweet's for You")
    for i,tweet in enumerate(sns.TwitterSearchScraper(data_scrap).get_items()):
        if i>range:
            break
        tweets_list.append([tweet.username, tweet.renderedContent, tweet.url, tweet.likeCount, tweet.date.date(), tweet.retweetCount])
        st.write("User : ", tweet.username)
        st.write("Tweet : ", tweet.renderedContent)
        st.write("Tweet Link : ", tweet.url)
        with st.expander("More"):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.caption("Likes")
                st.write(tweet.likeCount)

            with col2:
                st.caption("Date")
                st.write(tweet.date.date())

            with col3:
                st.caption("ReTweet Count")
                st.write(tweet.retweetCount)

        st.write("*"*50)
    tweets_df = pd.DataFrame(tweets_list, columns=['User_Name', 'Tweet', 'Tweet_Url', 'Like_Count', 'Tweet_Date', 'Retweet_Count' ])
    st.write(tweets_df)


    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(tweets_df)

    st.sidebar.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='tweets.csv',
        mime='text/csv',
        )

else:
    st.title("#TWEET's FROM TWITTER")
    st.image("data:image/png;base64,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")

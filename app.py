import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
from collections import Counter
import streamlit as st

#Import the english stop words list from NLTK
stopwords_english = stopwords.words('english')

# Activate lemmatizer
lemmatizer = WordNetLemmatizer()

#Logo
logo = './static/logo-Porsche.png'
favicon = './static/porsche.ico'

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def perform_data_cleaning(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    
    word_list_clean = []
    
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    
    text = lemmatizer.lemmatize(text) # Lemmatize (Root Words)
    
    text_list = text.split()
    
    for word in text_list:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
                word_list_clean.append(word)
            
    return word_list_clean

# def remove_stop_word_and_punc(word_list):
#     word_list_clean = []
#     for word in word_list: # Go through every word in your tokens list
#         if (word not in stopwords_english and  # remove stopwords
#             word not in string.punctuation):  # remove punctuation
#             word_list_clean.append(word)
#     return word_list_clean

def get_sentiments(user_input):
    
    score = SentimentIntensityAnalyzer().polarity_scores(user_input)
    neg = score['neg']
    pos = score['pos']
    if neg > pos :
        sentiment = 'Negative Sentiment'
    elif pos > neg:
        sentiment = 'Positive Sentiment'
    else:
        sentiment = 'Neutral Sentiment'
    return sentiment

def streamlit_interface(neg_lex_list, pos_lex_list):
    
    """
      Function for Streamlit Interface
    """
    # Switch Off Warning
    st.set_option('deprecation.showPyplotGlobalUse', False)


    # Page Setup
    st.set_page_config(
    page_title="Porsche Sales Forecasting",
    page_icon=favicon,
    layout="centered",
    initial_sidebar_state="auto")  

    # Load CSS
    local_css("./static/style.css")

    # Remove Made With Streamlit Footer
    st.markdown('<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>',
                unsafe_allow_html=True)

    # Load  Logo
    st.image('./static/porsche.png', width = 100)

    # Load Application Name
    st.title('Porsche Sentiment Analysis')

    user_input = st.text_area("")

    if st.button('Submit'):
        sentiment_polarity =  get_sentiments(user_input)
        st.header('Sentiment Polarity')
        st.write(sentiment_polarity)

        text_list = perform_data_cleaning(user_input)

        st.header('What Customers are saying ?')
        neg_feedback_words = []
        pos_feedback_words = []
        
        if sentiment_polarity == 'Negative Sentiment':
            for neg_word in text_list :
                if neg_word in neg_lex_list:
                    neg_feedback_words.append(neg_word)
            st.error(set(neg_feedback_words))
                    
        if ((sentiment_polarity == 'Positive Sentiment') or (sentiment_polarity == 'Neutral Sentiment')):
            for pos_word in text_list :
                if pos_word in pos_lex_list:
                    pos_feedback_words.append(pos_word)
            st.success(set(pos_feedback_words))

        # Biagram Analysis
        st.sidebar.header('Biagram Analysis')
        st.sidebar.table(list(zip(text_list[0:], text_list[1:])))
    

    # Increase width of sidebar
    st.markdown(
                """
                <style>
                [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                    width: 500px;
                }
                [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
                    width: 500px;
                    margin-left: -500px;
                }
                </style>
                """,
                unsafe_allow_html=True,
                )   

    # Foreacasing Option
    

            

if __name__ == "__main__":
    file_neg_lex = open("./static/negative-words.txt", "r")
    neg_lex_list = file_neg_lex.read().split()

    file_pos_lex = open("./static/positive-words.txt", "r")
    pos_lex_list = file_pos_lex.read().split()

    streamlit_interface(neg_lex_list, pos_lex_list)
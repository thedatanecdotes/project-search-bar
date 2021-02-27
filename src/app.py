# for flask api
import streamlit as st
import seaborn as sns
import base64
import time
from joblib import Parallel,delayed
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tweet import get_data,get_api
from news import news_sentiments

st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href
def common(p,n):
    p = set(p.split(' '))
    n = set(n.split(' '))
    print(p)
    c = p.intersection(n)
    return list(c)

def rep(cloud,common_ele):
    cloud = cloud.split(' ')
    new_words = ' '.join([word for word in cloud if word not in common_ele])
    return new_words




st.set_page_config( page_title="The Data Anecdotes",page_icon="🧊",layout="centered",initial_sidebar_state="expanded")
st.title("The Data Anecdotes")
st.write("Enter the topic you want to search, in the sidebar. :wink: :mag:")
st.sidebar.title("Project Search Bar")
keyword=st.sidebar.text_input("Enter the keyword you want to search"," ")
if (keyword !=" "):

        st.write("Looking for ",keyword,"...")
        st.write("Reading News Articles and tweets ...")
        
        p = Parallel(n_jobs=-1)([
            delayed(news_sentiments)(keyword,10),
            delayed(get_data)(keyword,get_api())
        ])
        
        news_data = p[0]
        data = p[1]
        st.success("Done")
        
        pos=[row['Clean Tweets'] for _,row in data.iterrows() if row['SS']=="POSITIVE"]
        neg=[row['Clean Tweets'] for _,row in data.iterrows() if row['SS']=="NEGATIVE"]
        sns.set()
        fig, ax = plt.subplots()
        fig.set_size_inches(11.7, 8.27)
        with st.beta_expander("Disclaimer"):
            st.write("**Disclaimer**: This website simply performs analysis.We free our data from all possible biases prior to analysis but certain biases ,like that of opinions(in case of twitter and news websites), cannot be removed.Our analysis is done with the help of mathematical formulas and tend to have a certain amount of accuracy. They must not be perceived as absolute truth.")
        with st.beta_expander("Tweet Analysis"):
            st.header("Sentiments Each Day") 
            sns.countplot(data['Date'].dt.date,hue=data['SS'])
            plt.xticks(rotation=90)
            st.pyplot(clear_figure="False",use_column_width="True")
            st.header("Top 10 tweet Locations")
            sns.countplot(y="Location",  data=data,order=data['Location'].value_counts().iloc[1:11].index)
            st.pyplot(clear_figure="False",use_column_width="True")
            
            st.header("Positive Word Cloud")
            poscloud=' '.join([i for i in pos])
            negcloud=' '.join([i for i in neg])
            c = common(poscloud,negcloud)
            poscloud = rep(poscloud,c)
            negcloud = rep(negcloud,c)
            wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(poscloud)
            plt.figure(figsize=(15, 8))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            st.pyplot(clear_figure="False",use_column_width="True")
            
            st.header("Negative Word Cloud")
            
            wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(negcloud)
            plt.figure(figsize=(15, 8))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            st.pyplot(clear_figure="False",use_column_width="True")
        
        with st.beta_expander("News Websites Analysis"):
            if (type(news_data) is dict):
                for i in range(len(news_data)):
                    st.write("**Article**:",i)
                    for key,value in news_data[i].items():
                        st.write(" _",key,"_ :",value)
            else:
                st.write(news_data)
        with st.beta_expander("See Tweet Data"):
             st.dataframe(data)
             st.markdown(get_table_download_link(data))
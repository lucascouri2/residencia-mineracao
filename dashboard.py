import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# Set page title
st.title('Reviews da Amazon - Firestick TV')

@st.cache
def load_data():
    df = pd.read_csv("reviews_v2.csv")
    df = df[df["reviews"].notna()]
    df["class"] = df["stars"].apply(lambda x : "Positiva" if x >=4 else "Negativa")
    df["dates"] = pd.to_datetime(df["dates"])
    return df

# @st.cache
# def load_wordcloud(data):
#     lista_rev = data["reviews"].tolist()
#     big_string = (" ").join(lista_rev)
#     stop_words = stopwords.words('portuguese')
#     wordcloud = WordCloud(stopwords=stop_words, background_color="white", max_words=500, contour_width=3, width=1600, height=800).generate(big_string)
#     fig = plt.figure(figsize=[20,10])
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     return fig

data_load_state = st.text('Loading data...')
data = load_data()
# wordcloud = load_wordcloud(data)
data_load_state.text("Done! (using st.cache)")

# st.subheader('Raw data')
# st.write(data)

col1, col2= st.columns(2)

### Plot Time Series - Reviews ###
# st.subheader('Número de reviews')
col1.header("Reviews no tempo")
df_count_reviews = pd.DataFrame({'count' : data.groupby( [ "dates", "class"] ).size()}).reset_index()
fig = px.line(df_count_reviews, x="dates", y="count", color='class',
                labels={
                        "dates": "Data",
                        "count": "Número de reviews",
                        "class": "Tipo de review"
                        },
                        title="Reviews no tempo")
col1.plotly_chart(fig)


### Plot Wordcloud ###
# st.subheader('Wordcloud')
col2.header("Wordcloud")
data_load_state = st.text('Loading data...')
lista_rev = data["reviews"].tolist()
big_string = (" ").join(lista_rev)
stopwords = stopwords.words('portuguese')
wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=200, contour_width=3, width=800, height=400).generate(big_string)
fig = plt.figure(figsize=[20,10])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
col2.pyplot(fig)
data_load_state.text("")



# hist_values = np.histogram(
#     #data[""].dt.hour, bins=24, range=(0,24))[0]
#     data["stars"], bins=24)[0]
# st.bar_chart(hist_values)


#st.line_chart(data[""])

#values = st.sidebar.slider(“Price range”, float(df.price.min()), 1000., (50., 300.))
#f = px.histogram(df.query(f”price.between{values}”), x=”price”, nbins=15, title=”Price distribution”)
#f.update_xaxes(title=”Price”)
#f.update_yaxes(title=”No. of listings”)
#st.plotly_chart(f)



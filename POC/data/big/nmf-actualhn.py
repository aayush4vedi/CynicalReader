#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
from collections import Counter
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary
from sklearn.decomposition import NMF
from gensim.models.nmf import Nmf
from operator import itemgetter
from tqdm.notebook import tqdm
# get_ipython().run_line_magic('load_ext', 'autotime')


# In[3]:


# get_ipython().system('pip install pandas')


# In[22]:


pd.set_option('display.max_colwidth', -1)


# # Data Extraction 

# In[5]:


data = pd.read_csv('/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn15Feb_15Aug/with_content/hn_all_15Feb_15Augwc.csv')


# In[6]:


data.shape


# In[115]:


type(data['TimeGST'])


# In[24]:


data.head(1)


# In[25]:


data.info()


# In[31]:


data.loc[data['Content'].isnull()]


# In[33]:


data.dropna(subset= ['Content'], inplace=True)


# In[36]:


def missing_percentage(df):
    total = df.isnull().sum().sort_values(ascending = False)
    percent = round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2)
    return pd.concat([total, percent], axis=1, keys=['Total','Percent'])
missing_percentage(data)


# # Cleaning 

# In[37]:


# import spacy
# spacy.load('en')
# # spacy.load('en_core_web_sm')


# from spacy.lang.en import English
# parser = English()
# def tokenize(text):
#     lda_tokens = []
#     tokens = parser(text)
#     for token in tokens:
#         if token.orth_.isspace():
#             continue
#         elif token.like_url:
#             lda_tokens.append('URL')
#         elif token.orth_.startswith('@'):
#             lda_tokens.append('SCREEN_NAME')
#         else:
#             lda_tokens.append(token.lower_)
#     return lda_tokens


# # Pre-processing the data for modelling 

# In[38]:


import nltk
# nltk.download('wordnet')
# print("+========================== here======================\n\n")

# from nltk.corpus import wordnet as wn
# def get_lemma(word):
#     lemma = wn.morphy(word)
#     if lemma is None:
#         return word
#     else:
#         return lemma
    
# from nltk.stem.wordnet import WordNetLemmatizer
# def get_lemma2(word):
#     return WordNetLemmatizer().lemmatize(word)


# In[39]:


# nltk.download('stopwords')
# en_stop = set(nltk.corpus.stopwords.words('english'))


# In[40]:


# def prepare_text_for_lda(text):
#     tokens = tokenize(text)
#     #tokens = [token for token in tokens if len(token) > 4]
#     tokens = [token for token in tokens if token not in en_stop]
#     tokens = [get_lemma(token) for token in tokens]
#     return tokens


# In[41]:


# data['tokens']=  data['Content'].apply(lambda x: prepare_text_for_lda(x))
data['tokens']=  data['Content']


# In[44]:


data.head(1)


# # EDA 

# In[45]:


# Get the word count
def word_count(text):
    return len(str(text).split(' '))
data['word_count'] = data['tokens'].apply(word_count)
data['word_count'].mean()


# In[48]:


data['word_count'].describe()


# In[85]:


# Plot a hist of the word counts
# fig = plt.figure(figsize=(5,5))

# plt.hist(
#     data['word_count'],
#     bins=100,
#     color='#60505C'
# )

# plt.title('Distribution - Article Word Count', fontsize=16)
# plt.ylabel('Frequency', fontsize=12)
# plt.xlabel('Word Count', fontsize=12)
# plt.yticks(np.arange(0, 7000, 500))
# plt.xticks(np.arange(0, 1000, 100))

# plt.show()


# In[93]:



# # Plot a boxplot of the word counts
# fig = plt.figure(figsize=(4,9))

# sns.boxplot(
#     data['word_count'],
#     orient='v',
#     width=500,
#     color='#ff8080'
# )

# plt.ylabel("Word Count", fontsize=12)
# plt.title('Distribution - Article Word Count', fontsize=16)
# plt.yticks(np.arange(0, 70000, 500))

# file_name = 'box_plot'

# plt.show()


# In[99]:



# Get the top 20 most common words among all the articles
p_text = data['tokens']

# Flaten the list of lists
p_text = [item for sublist in p_text for item in sublist]

# Top 20
top_20 = pd.DataFrame(
    Counter(p_text).most_common(2000),
    columns=['word', 'frequency']
)

top_20


# In[95]:


# Plot a bar chart for the top 20 most frequently occuring words
# fig = plt.figure(figsize=(20,7))

# g = sns.barplot(
#     x='word',
#     y='frequency',
#     data=top_20,
#     palette='GnBu_d'
# )

# g.set_xticklabels(
#     g.get_xticklabels(),
#     rotation=45,
#     fontsize=14
# )

# plt.yticks(fontsize=14)
# plt.xlabel('Words', fontsize=14)
# plt.ylabel('Frequency', fontsize=14)
# plt.title('Top 20 Words', fontsize=17)

# plt.show()


# In[96]:


# Get the number of unique words after processing
num_unique_words = len(set(p_text))
num_unique_words


# In[104]:


import time 


# In[108]:

from nltk.tokenize import word_tokenize

#Use Gensim's NMF to get the best num of topics via coherence score
# texts = word_tokenize(data['tokens'])
texts = data['tokens'].apply(lambda x: [word_tokenize(data['tokens'].astype(str))])

# Create a dictionary
# In gensim a dictionary is a mapping between words and their integer id
dictionary = Dictionary(texts)

# Filter out extremes to limit the number of features
dictionary.filter_extremes(
    no_below=3,
    no_above=0.85,
    keep_n=5000
)

# Create the bag-of-words format (list of (token_id, token_count))
corpus = [dictionary.doc2bow(text) for text in texts]

# Create a list of the topic numbers we want to try
topic_nums = list(np.arange(5, 75 + 1, 5))

# Run the nmf model and calculate the coherence score
# for each number of topics
coherence_scores = []
for i in tqdm(range(0, len(topic_nums))):
    for num in topic_nums:
        nmf = Nmf(
        corpus=corpus,
        num_topics=num,
        id2word=dictionary,
        chunksize=2000,
        passes=5,
        kappa=.1,
        minimum_probability=0.01,
        w_max_iter=300,
        w_stop_condition=0.0001,
        h_max_iter=100,
        h_stop_condition=0.001,
        eval_every=10,
        normalize=True,
        random_state=42
    )
    time.sleep(0.5)
    
    # Run the coherence model to get the score
    cm = CoherenceModel(
        model=nmf,
        texts=texts,
        dictionary=dictionary,
        coherence='c_v'
    )
    
    coherence_scores.append(round(cm.get_coherence(), 5))


# In[ ]:


# Get the number of topics with the highest coherence score
scores = list(zip(topic_nums, coherence_scores))
best_num_topics = sorted(scores, key=itemgetter(1), reverse=True)[0][0]

# Plot the results
fig = plt.figure(figsize=(15, 7))

plt.plot(
    topic_nums,
    coherence_scores,
    linewidth=3,
    color='#4287f5'
)

plt.xlabel("Topic Num", fontsize=14)
plt.ylabel("Coherence Score", fontsize=14)
plt.title('Coherence Score by Topic Number - Best Number of Topics: {}'.format(best_num_topics), fontsize=18)
plt.xticks(np.arange(5, max(topic_nums) + 1, 5), fontsize=12)
plt.yticks(fontsize=12)

plt.show()


# In[111]:


# Now use the number of topics with the 
# highest coherence score to run the 
# sklearn nmf model
from sklearn.feature_extraction.text import TfidfVectorizer


texts = data['tokens']

# Create the tfidf weights
tfidf_vectorizer = TfidfVectorizer(
    min_df=3,
    max_df=0.85,
    max_features=5000,
    ngram_range=(1, 2),
    preprocessor=' '.join
)

tfidf = tfidf_vectorizer.fit_transform(texts)

# Save the feature names for later to create topic summaries
tfidf_fn = tfidf_vectorizer.get_feature_names()

# Run the nmf model
nmf = NMF(
    n_components=8,
    init='nndsvd',
    max_iter=500,
    l1_ratio=0.0,
    solver='cd',
    alpha=0.0,
    tol=1e-4,
    random_state=42
).fit(tfidf)


# In[112]:


from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer, RegexpTokenizer
import nltk
def topic_table(model, feature_names, n_top_words):
    topics = {}
    for topic_idx, topic in enumerate(model.components_):
        t = (topic_idx)
        topics[t] = [feature_names[i] for i in top_words(topic, n_top_words)]
    return pd.DataFrame(topics)

def top_words(topic, n_top_words):
    return topic.argsort()[:-n_top_words - 1:-1]  
def whitespace_tokenizer(text): 
    pattern = r"(?u)\b\w\w+\b" 
    tokenizer_regex = RegexpTokenizer(pattern)
    tokens = tokenizer_regex.tokenize(text)
    return tokens
# Funtion to remove duplicate words
def unique_words(text): 
    ulist = []
    [ulist.append(x) for x in text if x not in ulist]
    return ulist
# Use the top words for each cluster by tfidf weight
# to create 'topics'

# Getting a df with each topic by document
docweights = nmf.transform(tfidf_vectorizer.transform(texts))

n_top_words = 8

topic_df = topic_table(
    nmf,
    tfidf_fn,
    n_top_words
).T

# Cleaning up the top words to create topic summaries
topic_df['topics'] = topic_df.apply(lambda x: [' '.join(x)], axis=1) # Joining each word into a list
topic_df['topics'] = topic_df['topics'].str[0]  # Removing the list brackets
topic_df['topics'] = topic_df['topics'].apply(lambda x: whitespace_tokenizer(x)) # tokenize
topic_df['topics'] = topic_df['topics'].apply(lambda x: unique_words(x))  # Removing duplicate words
topic_df['topics'] = topic_df['topics'].apply(lambda x: [' '.join(x)])  # Joining each word into a list
topic_df['topics'] = topic_df['topics'].str[0]  # Removing the list brackets

topic_df.head()


# In[ ]:





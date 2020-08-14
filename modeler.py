import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn import metrics

df = pd.read_csv('./data/all_data_arxiv.csv')
# Topic,Title,Content

""" 
    DATA CLEANING: Check for missing values
"""

## 1.Detect & remove NaN values
# print(df.isnull().sum())
df.dropna(inplace=True)

## 2. Detect & remove empty strings
# blanks = []  # start with an empty list

# for title,content in df.itertuples(index=False):  # iterate over the DataFrame
#     if type(content)==str:            # avoid NaN values
#         if content.isspace():         # test 'content' for whitespace
#             blanks.append(title)     # add matching index numbers to the list
        
# print(len(blanks), 'blanks: ', blanks)
# df.drop(blanks, inplace=True)
# print(len(df))

""" Take a quick look at the label column """
# print(df['Topic'].value_counts())

""" 
    Training the Models
"""


""" Split the data into train & test sets """
# X = df['Title']
X = df['Content']
y = df['Topic']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

""" Build pipelines to vectorize the data, then train and fit a model """
# Model1: Naïve Bayes: ===========================> Accuracy: 0.85
text_clf_nb = Pipeline(
    [('tfidf', TfidfVectorizer()),('clf', MultinomialNB()),])

# Model2: Linear SVC: ===========================> Accuracy: 0.85
text_clf_lsvc = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', LinearSVC()),
])

# Model3: Linear SVC: ===========================> Accuracy: 0.85
text_clf_lr = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', LogisticRegression()),
])

""" Model#1: Run Predictions(Naive Bayes)"""

text_clf_nb.fit(X_train, y_train)
# Form a prediction set
predictions = text_clf_nb.predict(X_test)
print(" \n\n======== Confusion Matrix: model1 =============\n")
# print(metrics.confusion_matrix(y_test,predictions))

# Print a classification report
print(metrics.classification_report(y_test,predictions))

# Print the overall accuracy
print("Model1: Accuracy = ", metrics.accuracy_score(y_test,predictions))      #""" ============> 0.8503030303030303 """

""" Model#2: Run predictions and analyze the results (Linear SVC)"""

text_clf_lsvc.fit(X_train, y_train)
# Form a prediction set
predictions = text_clf_lsvc.predict(X_test)
print(" \n\n======== Confusion Matrix: model2 =============\n")
# print(metrics.confusion_matrix(y_test,predictions))

# Print a classification report
print(metrics.classification_report(y_test,predictions))

# Print the overall accuracy
print("Model2: Accuracy = ", metrics.accuracy_score(y_test,predictions))      #""" ============> 0.8448484848484848 """


""" Adding Stopwords to CountVectorizer : on Model#2 """  

text_clf_lsvc2 = Pipeline([('tfidf', TfidfVectorizer(stop_words='english')),
                     ('clf', LinearSVC()),
])
text_clf_lsvc2.fit(X_train, y_train)
predictions = text_clf_lsvc2.predict(X_test)
# print("Model3: Accuracy = ", metrics.accuracy_score(y_test,predictions))     #""" ============> 0.8406060606060606 """



""" Adding Stopwords to CountVectorizer : on Model#3 """  

text_clf_lr.fit(X_train, y_train)
predictions = text_clf_lr.predict(X_test)
print(" \n\n======== Confusion Matrix: model3 =============\n")

# Print a classification report
print(metrics.classification_report(y_test,predictions))
print("Model3: Accuracy = ", metrics.accuracy_score(y_test,predictions))      #""" ============> 0.8448484848484848 """

""" 
    Feed new data into a trained model
"""

print(" \n\n ************************** PREDICTIONS *****************************\n")

mycontent = """ 
factor involved cancer screening participation multilevel mediation model,paper identify factor associated cancer screening participation korea expand upon previous study multilevel mediation model composite regional socioeconomic status index combine education level income level result model indicate education level nutritional education status income level significantly associated cancer screening participation finding mind recommend health authority increase promotional health campaign toward certain atrisk group expand availability nutrition education program
"""                                            

print("Model#1 predicts: ",text_clf_nb.predict([mycontent])) 
print("Model#2 predicts: ",text_clf_lsvc.predict([mycontent])) 
print("Model#3 predicts: ",text_clf_lr.predict([mycontent])) 
# print("Model#3 predicts: ",text_clf_lsvc2.predict([mycontent])) 






# -*- coding: utf-8 -*-
"""Email classification using BERT (vector embedding).ipynb

Automatically generated by Colab.

"""

!pip install tensorflow_text

!pip install tensorflow_hub

!pip install tensorflow

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import pandas as pd

"""## creating dataset"""

df = pd.read_csv("/spam.csv")
df.head()

df.groupby('Category').describe()

df['Category'].value_counts()

747/4825
#15% spam emails, 85% ham emails: This indicates class imbalance
#15% are spam emails there's some imbalance
#we can use dwonsamplling technique to balance the dataset. in here we pick random 747 data from 4825
#this might be not good when it comes to training cause we decrese,loosing the training data here
#there are other approaches like smort , oversampling (oversample the minority class)

#create seperate dataframes for ham and spam emails
df_spam = df[df['Category']=='spam']
df_spam.shape

df_ham = df[df['Category']=='ham']
df_ham.shape

df_ham.sample(747)

df_ham.sample(df_spam.shape[0])

#downsamplling the ham dtaframe (clean emails,not spam)
df_ham_downsampled = df_ham.sample(df_spam.shape[0])
df_ham_downsampled.shape

#connect 2 dataframes
df_balanced = pd.concat([df_ham_downsampled, df_spam])
df_balanced.shape

df_balanced['Category'].value_counts()
#this might not good cause we are loosing valuble training dataset
#this fis or learn BERT vector embeddings and classfication

df_balanced.sample(5)

#create new spam column if spam=1 not sapm=0
df_balanced['spam']=df_balanced['Category'].apply(lambda x: 1 if x=='spam' else 0)
df_balanced.sample(5)

"""## Split it into training and test data set"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df_balanced['Message'],df_balanced['spam'], stratify=df_balanced['spam'])

X_train.head()

"""## import BERT model and get embeding vectors for few sample statements"""

#get trained models from TF Hub for preprocess and encode
bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

def get_sentence_embedding(sentences):
    preprocessed_text = bert_preprocess(sentences)
    return bert_encoder(preprocessed_text)['pooled_output']

get_sentence_embedding([
    "500$ discount. hurry up",
    "kasun, are you intresetd in winnig new iphone 16?"]
)
#enoding for the sentences are return as outputs generates from above BERT models

"""### Get embeding vectors for few sample words. Compare them using cosine similarity"""

e = get_sentence_embedding([
    "phone",
    "camera",
    "grapes",
    "mango",
    "cash price",
    "money",
    "jeff bezos",
    "elon musk",
    "bill gates"
]
)
#check cosine similarity for some word/embeddings and find out benifit of having BERT encoding

from sklearn.metrics.pairwise import cosine_similarity
cosine_similarity([e[0]],[e[1]])
#from cosine simillarity we can identify how simillar two vectors are. if those 2 vectors points to same direction or not

"""Values near to 1 means they are similar. 0 means they are very different.
Above you can use comparing "phone" vs "camera" you get 0.89 similarity as they both are electronics
"""

cosine_similarity([e[2]],[e[3]])

"""Above you can use comparing "mango" vs "grapes" you get 0.98 similarity as they both are fruits"""

cosine_similarity([e[4]],[e[5]])

"""Above you can use comparing "cash price" vs "money" you get 0.92 similarity as they both are same valuble items"""

cosine_similarity([e[2]],[e[6]])

"""Comparing grapes with jeff bezos you still get 0.87 but it is not as close as 0.98 that we got with mangos"""

cosine_similarity([e[6]],[e[7]])

"""Jeff bezos and Elon musk are more similar you get 0.98 then Jeff bezos and grapes as indicated above

# build model

There are two types of models you can build in tensorflow.

(1) Sequential
(2) Functional

So far we have built sequential model. But below we will build functional model. More information on these two is here: https://becominghuman.ai/sequential-vs-functional-model-in-keras-20684f766057
"""

from tensorflow.keras import layers

sample_text = ["This is a test sentence"]
preprocessed_text = bert_preprocess(tf.constant(sample_text))

pip show tensorflow tensorflow-hub

# Bert layers
text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)

# Neural network layers
l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

# Use inputs and outputs to construct a final model
model = tf.keras.Model(inputs=[text_input], outputs = [l])

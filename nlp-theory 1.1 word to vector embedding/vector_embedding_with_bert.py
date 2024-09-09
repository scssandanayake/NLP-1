# -*- coding: utf-8 -*-
"""Vector Embedding With BERT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1o1L7aFbfX7iRYUR03o3XqRlScmqoyrNO
"""

!pip install tensorflow_hub

!pip install tensorflow_text

#import tensorflow hub and text
import tensorflow_hub as hub
import tensorflow_text as text

#to preprocess the text using allocated preprocessing model for basic BERT model(below)
preprocess_url = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
#use basic encoder BERT model for encoding task
encoder_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4"

#create hub layer
bert_preprocess_model = hub.KerasLayer(preprocess_url)

#provide sample statements for preprocess
text_test = ['nice movie indeed','I love python programming']
text_preprocessed = bert_preprocess_model(text_test) #BERT modle act like a function pointer
text_preprocessed.keys() #dictionary

text_preprocessed['input_mask']
#shape=(2, 128) 2 represents 2 sentences and 128 is like maximum lenth of the sentence
#the first sentence 'nice movie indeed' have three words.but when bert model works it add 2 special tokens in the beginning and the end
#so the sentence looks like 'CLS nice movie indeed SEP' now it have 5 words each word shown as 1 in binaries
#so the 1st sentence have 3+2 words then 5 1's 2nd sentence have 4+2 then 6 1's

text_preprocessed['input_word_ids']
#this sentence create by BERT models by adding extra 2 tokens 'CLS nice movie indeed SEP'
#wors ID for CLS and SEP are 101, 102 midlle 3 are uniqe ID's for remaining middle words, 4 middle ID's for 2nd sentence

text_preprocessed['input_type_ids']
#the prerocessing stage is done.

#then we create another layer for encoding part
bert_model = hub.KerasLayer(encoder_url)

bert_results = bert_model(text_preprocessed) #BERT modle act like a function pointer

bert_results.keys()



bert_results['pooled_output']
#pooled output is the embedding for entire sentences
#2 sentences and embedding vector size is 768

bert_results['sequence_output']
#this is individual word embedding vectors
#2 is for 2 sentences
#for each individual senteces we have some paddings that is what 128 represent. 128 is like maximum lenth of the sentence
#'nice movie indeed 0 0 0 0 0 0' <---- 128
#and for each word there is a 768 size embedding vector
#this is contextualized embedding that's why sentences have paddings like above
#these words have some context

len(bert_results['encoder_outputs'])
#12 means we are using small BERT base model and it contains 12 encoder layers. each layer has 768 size embedding vector
#so these encoder outputs is nothing but the output of each individual act encoder. So we have 12 that's why 12 is the size

bert_results['encoder_outputs'][0]
#the 1st encode layer

bert_results['encoder_outputs'][-1]
#for the last encode layer

bert_results['encoder_outputs'][-1] == bert_results['sequence_output']
#encoder output is the encoder output of all 12 layers and the last one is same as the sequence output

bert_results['encoder_outputs']
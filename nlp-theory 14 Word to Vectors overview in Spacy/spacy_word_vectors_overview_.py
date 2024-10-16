# -*- coding: utf-8 -*-
"""spacy word vectors overview .ipynb

Automatically generated by Colab.

"""

!python -m spacy download en_core_web_lg

import spacy

# word vectors occupy lot of space. hence en_core_web_sm model do not have them included.
# In order to download
# word vectors you need to install large or medium english model. We will install the large one!
# make sure you have run "python -m spacy download en_core_web_lg" to install large english model

nlp = spacy.load("en_core_web_lg")

"""reffer : https://spacy.io/models/en"""

doc = nlp("dog cat banana kem")

for token in doc:
    print(token.text, "Vector:", token.has_vector, "OOV:", token.is_oov)

doc[0].vector  #print the vector

doc[0].vector.shape #print the vector size . inbuilt size is 300.

base_token = nlp("bread")
base_token.vector.shape  # or base_token[0].vector.shape

doc = nlp("bread sandwich burger car tiger human wheat")

for token in doc:
    print(f"{token.text} <-> {base_token.text}:", token.similarity(base_token))

# compare simllarities between words and get a value.

"""* the models are train by lot of data from various sources.
* the similarities of the words are captured by looking at the context of the word.
* if two words appear in simillar context it may have higher value of simlarity.
* and finally the word/token (vector) features also affects when matching the similarities.
"""

def print_similarity(base_word, words_to_compare):
    base_token = nlp(base_word)
    doc = nlp(words_to_compare)
    for token in doc:
        print(f"{token.text} <-> {base_token.text}: ", token.similarity(base_token))

# create a function for take the similarity

print_similarity("iphone", "apple samsung iphone dog kitten")

"""do some arithmetic calculations usin gvector values for word/tokens"""

king = nlp.vocab["king"].vector
man = nlp.vocab["man"].vector
woman = nlp.vocab["woman"].vector
queen = nlp.vocab["queen"].vector

result = king - man + woman

"""get the cosine simillarity value for result with target word ( queen )"""

from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity([result], [queen])
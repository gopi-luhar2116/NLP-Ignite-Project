import nltk
import string
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):

    # lowercase
    text = text.lower()

    # replace slash with space
    text = text.replace("/", " ")

    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # tokenize
    words = word_tokenize(text)

    processed = []

    for word in words:

        # remove stopwords
        if word in stop_words:
            continue

        # remove numbers
        if word.isdigit():
            continue

        # remove single characters
        if len(word) == 1:
            continue

        # keep only alphabetic words
        if not re.match("^[a-zA-Z]+$", word):
            continue

        word = lemmatizer.lemmatize(word)

        processed.append(word)

    return processed
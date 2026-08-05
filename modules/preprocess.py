import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Downloads needed NLTK datasets
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Fix technical acronyms & combined terms BEFORE splitting
    text = text.replace("ai/ml", "aiml")
    text = text.replace("ai & ml", "aiml")
    text = text.replace("ai/l", "aiml")
    text = text.replace("/", " ")
    
    # 3. Direct string replacement for bullet symbols (bypasses regex encoding issues)
    bullets = ['•', '·', '▪', '●', '•', '\u2022', '\u2023', '\u25b6', '\u25c0', '\u25e6']
    for b in bullets:
        text = text.replace(b, ' ')
        
    # 4. Clean out all non-alphanumeric characters except spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # 5. Tokenize by splitting on whitespace
    words = text.split()
    
    processed = []
    
    for word in words:
        word = word.strip()
        
        # Skip stopwords
        if word in stop_words:
            continue
            
        # Keep single numbers (like '20') or technical terms, drop empty tokens
        if not word or not word.isalnum():
            continue
            
        # Lemmatize word
        lemmatized_word = lemmatizer.lemmatize(word)
        processed.append(lemmatized_word)
        
    return processed
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

# Function to remove stop words from English text
def eng_sw_removal(eng_tokens):
    StopWords = set(stopwords.words('english'))
    # StopWords = StopWords.append("any other list of words I want to add to my stop words list")
    # Tokenize the text into individual words and Remove stop words from the text
    eng_clean_tokens = [token for token in eng_tokens if token.lower() not in StopWords]
    return eng_clean_tokens
    
# Function to remove stop words from French text
def fr_sw_removal(fr_tokens):
    StopWords = set(stopwords.words('french'))
    # StopWords = StopWords.append("any other list of words I want to add to my stop words list")
    # Tokenize the text into individual words and Remove stop words from the text
    fr_clean_tokens = [token for token in fr_tokens if token.lower() not in StopWords]
    return fr_clean_tokens

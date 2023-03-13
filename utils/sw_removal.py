import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Function to remove stop words from English text
def eng_sw_removal(text):
    StopWords = set(stopwords.words('english'))
    # StopWords = StopWords.append("any other list of words I want to add to my stop words list")
    # Tokenize the text into individual words and Remove stop words from the text
    clean_text = ' '.join([word for word in text.split() if word.lower() not in StopWords])
    return clean_text
    
# Function to remove stop words from French text
def fr_sw_removal(text):
    StopWords = set(stopwords.words('french'))
    # StopWords = StopWords.append("any other list of words I want to add to my stop words list")
    # Tokenize the text into individual words and Remove stop words from the text
    clean_text = ' '.join([word for word in text.split() if word.lower() not in StopWords])
    return clean_text

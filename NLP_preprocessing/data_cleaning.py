import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from utils.sw_removal import eng_sw_removal, fr_sw_removal
from utils.pnc_removal import pnc_removal

# Data cleaning and preprocessing - English               
def eng_clean(eng_texts) :
    eng_tokenized = [] # list of (list of tokens)
    eng_removed_sw = [] # list of list of tokens without stopwords
    eng_removed_pnc = [] # list of list of tokens without stopwords nor punctuation
    eng_cleaned = [] # list of clean strings without stopwords nor punctuation
    for text in eng_texts:    
        # Tokenization
        eng_tokens = word_tokenize(text)
        eng_tokenized.append(eng_tokens)
        # Stop words removal
        eng_removed_sw1 = eng_sw_removal(eng_tokens)
        eng_removed_sw.append(eng_removed_sw1)
        # Punctuation removal
        eng_removed_pnc1 = pnc_removal(eng_removed_sw1)
        eng_removed_pnc.append(eng_removed_pnc1)
        # Join the cleaned text into a string
        eng_cleaned.append(" ".join(eng_removed_pnc1))
    return eng_cleaned



# Data cleaning and preprocessing - French               
def fr_clean(fr_texts) :
    fr_tokenized = []
    fr_removed_sw = []
    fr_removed_pnc = []
    fr_cleaned = []
    for text in fr_texts:    
        # Tokenization
        fr_tokens = word_tokenize(text)
        fr_tokenized.append(fr_tokens)
        # Stop words removal
        fr_removed_sw1 = fr_sw_removal(fr_tokens)
        fr_removed_sw.append(fr_removed_sw1)
        # Punctuation removal
        fr_removed_pnc1 = pnc_removal(fr_removed_sw1)
        fr_removed_pnc.append(fr_removed_pnc1)
        # Join the cleaned text into a string
        fr_cleaned.append(" ".join(fr_removed_pnc1))
    return fr_cleaned
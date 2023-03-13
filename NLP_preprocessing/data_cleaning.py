from utils.sw_removal import eng_sw_removal, fr_sw_removal
from utils.pnc_removal import pnc_removal

# Data cleaning and preprocessing - English               
def eng_clean(eng_texts) :
    eng_removed_sw = []
    eng_removed_pnc = []
    eng_cleaned = []
    for text in eng_texts:    
        # Tokenization and Stop words removal
        eng_removed_sw1 = eng_sw_removal(text)
        eng_removed_sw.append(eng_removed_sw1)
        # Punctuation removal
        eng_removed_pnc1 = pnc_removal(text)
        eng_removed_pnc.append(eng_removed_pnc1)         
    return eng_cleaned

# Data cleaning and preprocessing - French               
def fr_clean(fr_texts) :
    fr_removed_sw = []
    fr_removed_pnc = []
    fr_cleaned =[]
    for text in fr_texts:    
        # Tokenization and Stop words removal
        fr_removed_sw1 = fr_sw_removal(text)
        fr_removed_sw.append(fr_removed_sw1)
        # Punctuation removal
        fr_removed_pnc1 = pnc_removal(text)
        fr_removed_pnc.append(fr_removed_pnc1)
    return fr_cleaned
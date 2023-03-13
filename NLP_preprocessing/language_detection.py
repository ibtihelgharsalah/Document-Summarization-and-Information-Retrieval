from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def detect_language (doc_texts):
    eng_texts = []
    fr_texts = []
    other_langs = []
    for text in doc_texts:
        if len(text.strip()) > 0:
            try:
                lang = detect(text)
                if lang in ["en", "eng"]:
                    eng_texts.append(text)
                elif lang in ["fr", "fre", "fra"]:
                    fr_texts.append(text)
                else:
                    other_langs.append(text)
            except LangDetectException:
                # Catch LangDetectException and skip to the next document
                continue
    return eng_texts, fr_texts, other_langs
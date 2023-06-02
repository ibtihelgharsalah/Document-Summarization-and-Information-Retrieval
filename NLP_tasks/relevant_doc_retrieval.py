import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from NLP_preprocessing.language_detection import detect_language
from NLP_preprocessing.data_cleaning import eng_clean, fr_clean
nltk.download('punkt')

def find_related_documents(documents, eng_section_tokens, fr_section_tokens):
    # Classify the uploaded files by language
    eng_files, fr_files, other_language_files  = detect_language(documents)
    
    # Create a TfidfVectorizer object to transform the documents into vectors
    eng_vectorizer = TfidfVectorizer(stop_words='english')
    fr_stop_words = stopwords.words('french')
    fr_vectorizer = TfidfVectorizer(stop_words=fr_stop_words)
    
    # Create a list of the preprocessed document texts
    eng_texts_pre = list(eng_files.values())
    fr_texts_pre = list(fr_files.values())
    eng_texts = eng_clean(eng_texts_pre)
    fr_texts = fr_clean(fr_texts_pre)
    
    # Transform the document texts into vectors
    eng_vectors = eng_vectorizer.fit_transform(eng_texts)
    fr_vectors = fr_vectorizer.fit_transform(fr_texts)
    
    # Transform the question tokens within the section into a vector
    eng_question = eng_vectorizer.transform(eng_section_tokens)
    fr_question = fr_vectorizer.transform(fr_section_tokens)
    
    # Compute the cosine similarity between the section questions vector and each document vector
    eng_sim_scores = np.dot(eng_vectors, eng_question.T).toarray().flatten()
    fr_sim_scores = np.dot(fr_vectors, fr_question.T).toarray().flatten()
    
    # Round the similarity scores to three decimal places
    eng_sim_scores_rounded = np.round(eng_sim_scores, 3)
    fr_sim_scores_rounded = np.round(fr_sim_scores, 3)
    
    # Create a list of (filename, similarity score) tuples for English documents
    eng_results = [(filename, score) for filename, score in zip(eng_files.keys(), eng_sim_scores_rounded) if score > 0.04]

    # Create a list of (filename, similarity score) tuples for French documents
    fr_results = [(filename, score) for filename, score in zip(fr_files.keys(), fr_sim_scores_rounded) if score > 0.04]
    
    # Combine the results and sort by similarity score in descending order
    results = sorted(eng_results + fr_results, key=lambda x: x[1], reverse=True)
    
    return results
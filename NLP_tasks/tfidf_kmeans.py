from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy
from numpy import argsort
from NLP_preprocessing.data_cleaning import eng_clean, fr_clean
from nltk.corpus import stopwords

# Function to group english files by topic
def group_by_topic_english(eng_files):
    # Extract the text from each uploaded file and concatenate for each language
    eng_docs = [value for key, value in eng_files.items()]

    # Apply data cleaning to extracted texts
    eng_cleaned = eng_clean(eng_docs)
    
    # Create a TfidfVectorizer object for English documents
    eng_vectorizer = TfidfVectorizer(stop_words='english')
    # Transform the English corpus into a TF-IDF matrix
    eng_tfidf_matrix = eng_vectorizer.fit_transform(eng_cleaned)
    
    # Perform K-means clustering on the English TF-IDF matrix to cluster the English documents into 2 topics
    eng_kmeans = KMeans(n_clusters=2, random_state=0).fit(eng_tfidf_matrix)
    # Extract the labels from the K-means models
    eng_labels = eng_kmeans.labels_
    # Extract the centroids of the two clusters
    eng_centroids = eng_kmeans.cluster_centers_
    
    # Use the centroids to find the top keywords for each cluster
    n_top_keywords = 10
    eng_feature_names = eng_vectorizer.get_feature_names_out()
    eng_topics_keywords = {}
    for i in range(len(eng_centroids)):
        centroid = eng_centroids[i]
        # Sort the indices of the features based on their importance
        sorted_indices = centroid.argsort()[::-1][:n_top_keywords]
        # Get the keywords for the sorted indices
        top_keywords = [eng_feature_names[index] for index in sorted_indices]
        eng_topics_keywords[f'Topic {i+1}'] = top_keywords
    
    # Create empty lists for the English files for each topic
    eng_topic1, eng_topic2 = [], []
    # Loop through each file and classify it into the appropriate topic
    for file_name, text in eng_files.items():
        index = list(eng_files.keys()).index(file_name)
        if eng_labels[index] == 0:
            eng_topic1.append(file_name)
        else:
            eng_topic2.append(file_name)
    
    # Create a dictionary of topics
    eng_topics = {}
    eng_topics[f"Topic 1: ({', '.join(eng_topics_keywords['Topic 1'])})"] = eng_topic1
    eng_topics[f"Topic 2: ({', '.join(eng_topics_keywords['Topic 2'])})"] = eng_topic2
        
    return eng_topics




# Function to group french files by topic
def group_by_topic_french(fr_files):
    # Extract the text from each uploaded file and concatenate for each language
    fr_docs = [value for key, value in fr_files.items()]
    
    # Apply data cleaning to each language list
    fr_cleaned = fr_clean(fr_docs)
    
    # Create a TfidfVectorizer object for French documents
    fr_stop_words = stopwords.words('french')
    fr_vectorizer = TfidfVectorizer(stop_words=fr_stop_words)
    # Transform the French corpus into a TF-IDF matrix
    fr_tfidf_matrix = fr_vectorizer.fit_transform(fr_cleaned)
    
    # Perform K-means clustering on the French TF-IDF matrix to cluster the French documents into 2 topics
    fr_kmeans = KMeans(n_clusters=2, random_state=0).fit(fr_tfidf_matrix)
    # Extract the labels from the K-means models
    fr_labels = fr_kmeans.labels_
    # Extract the centroids of the two clusters
    fr_centroids = fr_kmeans.cluster_centers_
    
    # Use the centroids to find the top keywords for each cluster
    n_top_keywords = 10
    fr_feature_names = fr_vectorizer.get_feature_names_out()
    fr_topics_keywords = {}
    for i in range(len(fr_centroids)):
        centroid = fr_centroids[i]
        # Sort the indices of the features based on their importance
        sorted_indices = centroid.argsort()[::-1][:n_top_keywords]
        # Get the keywords for the sorted indices
        top_keywords = [fr_feature_names[index] for index in sorted_indices]
        fr_topics_keywords[f'Topic {i+1}'] = top_keywords
    
    # Create empty lists for the Frencg files for each topic
    fr_topic1, fr_topic2 = [], []
    # Loop through each file and classify it into the appropriate topic
    for file_name, text in fr_files.items():
        index = list(fr_files.keys()).index(file_name)
        if fr_labels[index] == 0:
            fr_topic1.append(file_name)
        else:
            fr_topic2.append(file_name)
    
    # Create a dictionary of topics
    fr_topics = {}
    fr_topics[f"Topic 1: ({', '.join(fr_topics_keywords['Topic 1'])})"] = fr_topic1
    fr_topics[f"Topic 2: ({', '.join(fr_topics_keywords['Topic 2'])})"] = fr_topic2
    
    return fr_topics

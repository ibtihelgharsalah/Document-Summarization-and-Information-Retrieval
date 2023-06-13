# import nltk

# def retrieve_info(eng_files, fr_files, eng_query, fr_query):
#     # Process the English query
#     eng_query_terms = nltk.word_tokenize(eng_query.lower())

#     # Process the French query
#     fr_query_terms = nltk.word_tokenize(fr_query.lower())

#     # Perform retrieval and ranking
#     results = []
#     for eng_file, fr_file in zip(eng_files, fr_files):
#         eng_sections = nltk.sent_tokenize(eng_file)  # Split English file into sections
#         fr_sections = nltk.sent_tokenize(fr_file)  # Split French file into sections
        
#         for eng_section, fr_section in zip(eng_sections, fr_sections):
#             eng_section_terms = nltk.word_tokenize(eng_section.lower())
#             fr_section_terms = nltk.word_tokenize(fr_section.lower())
            
#             eng_relevance_score = len(set(eng_query_terms) & set(eng_section_terms))  # Relevance score for English section
#             fr_relevance_score = len(set(fr_query_terms) & set(fr_section_terms))  # Relevance score for French section
            
#             results.append((eng_file, fr_file, eng_section, fr_section, eng_relevance_score, fr_relevance_score))
    
#     # Sort results by relevance scores in descending order
#     sorted_results = sorted(results, key=lambda x: (x[4], x[5]), reverse=True)
    
#     return sorted_results


import nltk

def retrieve_info(eng_files, fr_files, eng_query, fr_query):
    # Process the English query
    eng_query_terms = nltk.word_tokenize(eng_query.lower())

    # Process the French query
    fr_query_terms = nltk.word_tokenize(fr_query.lower())

    # Perform retrieval and ranking
    results = []
    for eng_filename, eng_file in eng_files.items():
        eng_sections = nltk.sent_tokenize(eng_file)  # Split English file into sections
        eng_section_terms = [nltk.word_tokenize(eng_section.lower()) for eng_section in eng_sections]
        for eng_section in eng_section_terms:
            eng_relevance_score = len(set(eng_query_terms) & set(eng_section))  # Relevance score for English section
            if eng_relevance_score >= 3:
                eng_section_str = ' '.join(eng_section)  # Join tokenized English section into a sentence
                results.append((eng_filename, eng_section_str, eng_relevance_score))
        
        
    for fr_filename, fr_file in fr_files.items():
        fr_sections = nltk.sent_tokenize(fr_file)  # Split French file into sections  
        fr_section_terms = [nltk.word_tokenize(fr_section.lower()) for fr_section in fr_sections]
        for fr_section in fr_section_terms:
            fr_relevance_score = len(set(fr_query_terms) & set(fr_section))  # Relevance score for French section
            if fr_relevance_score >= 3:
                fr_section_str = ' '.join(fr_section)  # Join tokenized French section into a sentence
                results.append((fr_filename, fr_section_str, fr_relevance_score))

    # Sort results by relevance scores in descending order
    sorted_results = sorted(results, key=lambda x: (x[2]), reverse=True)

    return sorted_results

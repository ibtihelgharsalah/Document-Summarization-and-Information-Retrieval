import re
from NLP_preprocessing.data_cleaning import eng_clean, fr_clean

def retrieve_info(eng_documents, fr_documents, eng_tokens, fr_tokens):
    extracted_info = {}  # Dictionary to store relevant information
    
    # Process English documents
    for eng_filename, eng_text in eng_documents.items():
        # Preprocess the English document text
        eng_processed_text = eng_clean(eng_text)
        
        # Initialize a list to store the extracted information for the current document
        document_info = []
        
        # Check relevance for English tokens
        for eng_token in eng_tokens:
            # Use regular expression to find matches of the token in the processed text
            matches = re.findall(r'\b{}\b'.format(re.escape(eng_token)), eng_processed_text, flags=re.IGNORECASE)
            
            # Add the matches to the document info list
            document_info.extend(matches)
        
        # Store the extracted information for the current English document
        extracted_info[eng_filename] = document_info
    
    # Process French documents
    for fr_filename, fr_text in fr_documents.items():
        # Preprocess the French document text
        fr_processed_text = fr_clean(fr_text)
        
        # Initialize a list to store the extracted information for the current document
        document_info = []
        
        # Check relevance for French tokens
        for fr_token in fr_tokens:
            # Use regular expression to find matches of the token in the processed text
            matches = re.findall(r'\b{}\b'.format(re.escape(fr_token)), fr_processed_text, flags=re.IGNORECASE)
            
            # Add the matches to the document info list
            document_info.extend(matches)
        
        # Store the extracted information for the current French document
        extracted_info[fr_filename] = document_info
    
    return extracted_info






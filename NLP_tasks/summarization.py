# BART
from transformers import BartTokenizer, T5Tokenizer, BartForConditionalGeneration, T5ForConditionalGeneration

# function for english files summarization
def eng_summarize(text):
    # Initialize the tokenizer and model
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    # Prepare the input data
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)

    # Generate the summary
    summary_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

# function for french files summarization
def fr_summarize(text):    
    # Initialize the tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained('plguillou/t5-base-fr-sum-cnndm')
    model = T5ForConditionalGeneration.from_pretrained('plguillou/t5-base-fr-sum-cnndm')

    # Prepare the input data
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)

    # Generate the summary
    summary_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


# # LongformerEncoderDecoderModel
# from transformers import LongformerTokenizer, LongformerModel, LongformerEncoderDecoderModel
# def longformer_encoder_decoder():
#     # Initialize the tokenizer and model for the Longformer
#     tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
#     longformer = LongformerModel.from_pretrained('allenai/longformer-base-4096')

#     # Initialize the LongformerEncoderDecoder model
#     longformer_encoder_decoder = LongformerEncoderDecoderModel.from_encoder_decoder_pretrained('allenai/longformer-base-4096', 'allenai/longformer-base-4096')

#     return tokenizer, longformer, longformer_encoder_decoder







## T5
# from transformers import T5Tokenizer, T5ForConditionalGeneration
# def summarize(text):
#     # Initialize the tokenizer and model
#     tokenizer = T5Tokenizer.from_pretrained('t5-bases')
#     model = T5ForConditionalGeneration.from_pretrained('t5-base')

#     # Prepare the input data
#     input_ids = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)
    
#     # Generate the summary
#     summary_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

#     return summary



## centroid_summarizer
# import centroid_summarizer
# from nltk.tokenize import sent_tokenize
# from gensim.models import Word2Vec
# def summarize(text):
#     # Tokenize the input text into sentences
#     raw_sentences = sent_tokenize(text)
    
#     # Clean the sentences
#     clean = list(centroid_summarizer.simple_clean(raw_sentences))
    
#     # Summarize using centroid bag-of-words method
#     cbs = centroid_summarizer.CentroidBOWSummarizer()
#     bow_summary = " ".join(list(cbs.summarize(raw_sentences, [" ".join(_) for _ in clean])))
    
#     # Summarize using centroid word embeddings method
#     model = Word2Vec(clean, min_count=1)
#     cws = centroid_summarizer.CentroidWordEmbeddingsSummarizer(model)
#     embedding_summary = " ".join(list(cws.summarize(raw_sentences, [" ".join(_) for _ in clean])))
# #bow_summary, 
#     return embedding_summary




# import requests
# import json

# def summarize(text):
#     # Make request to arXiv-PubMed API
#     url = "https://api.arxivpubmed.com/v1/papers/summarize"
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }
#     data = {
#         "text": text,
#         "max_sentences": 3
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(data))

#     # Parse response and return summary
#     if response.status_code == 200:
#         summary = response.json()['summary']
#         return summary
#     else:
#         return "Error: Failed to summarize text"

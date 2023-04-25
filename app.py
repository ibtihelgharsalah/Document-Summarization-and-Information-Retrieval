# A web application typically consists of a server that generates HTML pages, which are then rendered by a web 
# browser. Web applications are typically designed to serve a specific set of functions or tasks to users, 
# and the user interacts with the application through the browser's UI.

# BACKEND : server-side
import os # used to read and write files to the server's file system
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from NLP_preprocessing.text_extraction import extract_text
from NLP_preprocessing.language_detection import detect_language
from utils.allowed_extention import allowed_file
from NLP_tasks.tfidf_kmeans import group_by_topic_english, group_by_topic_french
from NLP_tasks.relevant_doc_retrieval import find_related_documents
from NLP_tasks.summarization import eng_summarize, fr_summarize
app = Flask(__name__)                                                           

# Set the upload folder and files
UPLOAD_FOLDER = 'uploads' # 'uploads' is a folder on the server
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filenames = os.listdir(UPLOAD_FOLDER)


# Main route to display the upload form (ask the user to upload files)
@app.route('/', methods=['GET', 'POST'])
def upload_files():
    # Remove all files from the UPLOAD_FOLDER directory from previous run
    for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    if request.method == 'POST':
        # Get the files from the request object
        files = request.files.getlist('files[]') # The getlist() method is used to retrieve multiple files submitted under the same name 'files[]'.
        # Loop through each file and save it to the server's folder ('uploads') if the file has an allowed extension
        for file in files:
            if file and allowed_file(file.filename): # if file is not empty and has an allowed extension.
                filename = secure_filename(file.filename) # convert the filename into a secure version, without any potentially malicious characters
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # save the file to the server's folder called 'UPLOAD_FOLDER'
        # redirects the user to the uploaded_files() route
        return redirect(url_for('uploaded_files'))
    # if the request method is GET
    # displays an HTML form that allows the user to select and upload files to the server.
    return render_template('upload.html') 


# Route to display the uploaded files classified by language and by topic
@app.route('/uploads') # will only handle GET requests by default
def uploaded_files():
    # Get the filenames of the uploaded files
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # Extract the text from each uploaded file
    doc_texts = extract_text(app.config['UPLOAD_FOLDER'], files)
    # Classify the uploaded files by language
    eng_files, fr_files, other_language_files  = detect_language(doc_texts)
    # Group the English and French files by topic
    eng_topics = group_by_topic_english(eng_files)
    fr_topics = group_by_topic_french(fr_files)
    # Summarize each English file
    eng_summaries = {}
    for file_name, text in eng_files.items():
        eng_summaries[file_name] = eng_summarize(text)
    # Summarize each French file
    fr_summaries = {}
    for file_name, text in fr_files.items():
        fr_summaries[file_name] = fr_summarize(text)    
    # Render the template and pass in the lists of filenames by language and topic
    return render_template('uploaded.html', eng_files= eng_files.keys(), fr_files= fr_files.keys(),
                            other_files= other_language_files.keys(), eng_topics= eng_topics, 
                            fr_topics= fr_topics, eng_summaries= eng_summaries, fr_summaries= fr_summaries)




@app.route('/question_answering')
def question_answering():
    # Get the filenames of the uploaded files
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # Extract the text from each uploaded file
    doc_texts = extract_text(app.config['UPLOAD_FOLDER'], files)
    eng_section_tokens = [["IT system", "information system", "financial reporting", "purpose of IT system", "technology layers", "IT gouvernance", "accounting", "business process", "software", "application", "network", "database", "os", "operating system", "update", "change", "development", "system change", "procedure"],
                          ["ISD", "IT system diagram", "diagram", "application", "network", "database", "os", "operating system","process", "IT system", "information system", "financial reporting", "purpose of IT system", "technology layers", "IT gouvernance", "accounting", "business process", "software", "application", "network", "database", "os", "operating system", "update", "change", "development", "system change", "procedure"],
                          ["IT organization", "members", "key members", "member name", "position", "services", "activity", "team", "Outsourced service provider", "Outsourced service", "skills","objectives", "supervision", "audit clause", "IT service contracts", "agreement", "providers", "service providers"],
                          ["IT process", "Access", "programs", "data","access management", "procedure", "password policy", "password", "Application changes", "changes", "change management", "procedure", "Acquisition", "development", "new","new system", "IT operations", "supervision", "procedures"],
                          ["cybersecurity", "security", "access", "password","people", "evaluation", "periodic", "vulnerability", "vulnerabilities", "mitigate", "potential risks", "risk", "significant", "impact", "devices", "security software", "software", "threat", "web", "virus", "attack", "phishing", "vpn", "encryption", "authorized", "disclosure", "authentication", "authorization", "cloud", "proxy", "cyberattack", "awareness", "monitor", "Verification control", "Cybersecurity", "Incident", "Team"]]
    
    fr_section_tokens = [["système informatique", "système d'information", "rapports financiers", "objectif du système informatique", "couches technologiques", "gouvernance informatique", "comptabilité", "processus d'entreprise", "logiciel", "application", "réseau", "base de données", "os", "système d'exploitation", "mise à jour", "changement", "développement", "changement de système", "procédure"],
                         ["DSI", "diagramme de système informatique", "diagramme", "application", "réseau", "base de données", "os", "système d'exploitation", "processus", "système informatique", "système d'information", "rapports financiers", "objectif du système informatique", "couches technologiques", "gouvernance informatique", "comptabilité", "processus d'entreprise", "logiciel", "application", "réseau", "base de données", "os", "système d'exploitation", "mise à jour", "changement", "développement", "changement de système", "procédure"],
                         ["organisation informatique", "membres", "membres clés", "nom du membre", "poste", "services", "activité", "équipe", "prestataire de services externalisés", "service externalisé", "compétences", "objectifs", "supervision", "clause d'audit", "contrats de services informatiques", "accord", "fournisseurs", "prestataires de services"],
                         ["processus informatique", "accès", "programmes", "données", "gestion des accès", "procédure", "politique de mot de passe", "mot de passe", "changements d'application", "changements", "gestion des changements", "procédure", "acquisition", "développement", "nouveau", "nouveau système", "opérations informatiques", "supervision", "procédures"],
                         ["cybersécurité", "sécurité", "accès", "mot de passe", "personnes", "évaluation", "périodique", "vulnérabilité", "vulnérabilités", "atténuer", "risques potentiels", "risque", "significatif", "impact", "dispositifs", "logiciel de sécurité", "logiciel", "menace", "web", "virus", "attaque", "phishing", "vpn", "cryptage", "autorisé", "divulgation", "authentification", "autorisation", "cloud", "proxy", "cyberattaque", "sensibilisation", "surveillance", "contrôle de vérification", "cybersécurité", "incident", "équipe"]]
    
    related_docs = []
    for es, fs in zip(eng_section_tokens, fr_section_tokens):
        d = find_related_documents(doc_texts, es, fs)
        related_docs.append(d)
    return render_template('question_answering.html', d0 = related_docs[0], d1 = related_docs[1], d2 = related_docs[2],
                           d3 = related_docs[3], d4 = related_docs[4])
     

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
# # Route to fetch the uploaded files and extract information to answer each question on the html page
# @app.route('/answer', methods=['GET'])
# def question_answering():
#     # Get the filenames of the uploaded files
#     files = os.listdir(app.config['UPLOAD_FOLDER'])
#     # Extract the text from each uploaded file
#     doc_texts = extract_text(app.config['UPLOAD_FOLDER'], files)
#     # Preprocess the uploaded files
#     preprocessed_files = preprocess_files(files)
#     # Get the questions from the HTML form
#     questions = request.args.getlist('question')
#     # Initialize a dictionary to hold the answers for each question
#     answers = {}
#     # Loop through each question and retrieve the relevant information
#     for question in questions:
#         # Extract information from the preprocessed files to answer the question
#         information = extract_information(preprocessed_files, question)
#         # Add the answer to the answers dictionary
#         answers[question] = information
#     # Render the results template and pass in the answers dictionary
#     return render_template('results.html', answers=answers)


# @app.route('/api/question-answering', methods=['POST'])
# def question_answering():
#     # Parse the question from the POST request
#     question = request.json['question']

#     # Define a pre-defined answer for the question
#     if question == 'What is the capital of France?':
#         answer = 'The capital of France is Paris.'
        
#     elif question == 'What is the tallest mountain in the world?':
#         answer = 'The tallest mountain in the world is Mount Everest.'
        
#     else:
#         answer = 'I am sorry, I do not know the answer to that question.'

#     # Return the answer as a JSON response
#     return jsonify({'answer': answer})

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
from NLP_tasks.info_retrieval import retrieve_info
from NLP_preprocessing.data_cleaning import eng_clean, fr_clean

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
    # Classify the uploaded files by language
    eng_files, fr_files, other_language_files  = detect_language(doc_texts)
    
    # Define the 5 lists of english tokens describing each of the 5 sections respectively
    eng_section_tokens = [["IT system", "information system", "financial reporting", "purpose of IT system", "technology layers", "IT gouvernance", "accounting", "business process", "software", "application", "network", "database", "os", "operating system", "update", "change", "development", "system change", "procedure"],
                          ["ISD", "IT system diagram", "diagram", "application", "network", "database", "os", "operating system","process", "IT system", "information system", "financial reporting", "purpose of IT system", "technology layers", "IT gouvernance", "accounting", "business process", "software", "application", "network", "database", "os", "operating system", "update", "change", "development", "system change", "procedure"],
                          ["IT organization", "members", "key members", "member name", "position", "services", "activity", "team", "Outsourced service provider", "Outsourced service", "skills","objectives", "supervision", "audit clause", "IT service contracts", "agreement", "providers", "service providers"],
                          ["IT process", "Access", "programs", "data","access management", "procedure", "password policy", "password", "Application changes", "changes", "change management", "procedure", "Acquisition", "development", "new","new system", "IT operations", "supervision", "procedures"],
                          ["cybersecurity", "security", "access", "password","people", "evaluation", "periodic", "vulnerability", "vulnerabilities", "mitigate", "potential risks", "risk", "significant", "impact", "devices", "security software", "software", "threat", "web", "virus", "attack", "phishing", "vpn", "encryption", "authorized", "disclosure", "authentication", "authorization", "cloud", "proxy", "cyberattack", "awareness", "monitor", "Verification control", "Cybersecurity", "Incident", "Team"]]
    # Define the 5 lists of french tokens describing each of the 5 sections respectively
    fr_section_tokens = [["système informatique", "système d'information", "rapports financiers", "objectif du système informatique", "couches technologiques", "gouvernance informatique", "comptabilité", "processus d'entreprise", "logiciel", "application", "réseau", "base de données", "os", "système d'exploitation", "mise à jour", "changement", "développement", "changement de système", "procédure"],
                         ["DSI", "diagramme de système informatique", "diagramme", "application", "réseau", "base de données", "os", "système d'exploitation", "processus", "système informatique", "système d'information", "rapports financiers", "objectif du système informatique", "couches technologiques", "gouvernance informatique", "comptabilité", "processus d'entreprise", "logiciel", "application", "réseau", "base de données", "os", "système d'exploitation", "mise à jour", "changement", "développement", "changement de système", "procédure"],
                         ["organisation informatique", "membres", "membres clés", "nom du membre", "poste", "services", "activité", "équipe", "prestataire de services externalisés", "service externalisé", "compétences", "objectifs", "supervision", "clause d'audit", "contrats de services informatiques", "accord", "fournisseurs", "prestataires de services"],
                         ["processus informatique", "accès", "programmes", "données", "gestion des accès", "procédure", "politique de mot de passe", "mot de passe", "changements d'application", "changements", "gestion des changements", "procédure", "acquisition", "développement", "nouveau", "nouveau système", "opérations informatiques", "supervision", "procédures"],
                         ["cybersécurité", "sécurité", "accès", "mot de passe", "personnes", "évaluation", "périodique", "vulnérabilité", "vulnérabilités", "atténuer", "risques potentiels", "risque", "significatif", "impact", "dispositifs", "logiciel de sécurité", "logiciel", "menace", "web", "virus", "attaque", "phishing", "vpn", "cryptage", "autorisé", "divulgation", "authentification", "autorisation", "cloud", "proxy", "cyberattaque", "sensibilisation", "surveillance", "contrôle de vérification", "cybersécurité", "incident", "équipe"]]
    
    # eng_question_tokens =["IT systems used by the entity for financial reporting and operational processes",
    #                       "Information concerning updates or significant changes",
    #                       "IT System Diagram ISD",
    #                       "Key members of the IT organization",
    #                       "Key IT organization functions",
    #                       "Key IT organization team members",
    #                       "Outsourced components",
    #                       "Areas of intervention, skills required, objectives, supervision method and audit clause for IT service providers",
    #                       "Check that access to applications is via a unique identifier and requires a password",
    #                       "Get the access management procedure",
    #                       "Ensure the existence of an application profile list / segregation of duties matrix",
    #                       "the password policy defined within the company and the consistency of criteria with best practices",
    #                       "Obtain and inspect the change management procedure",
    #                       "Obtain and inspect new systems development methodology",
    #                       "User incident and problem management",
    #                       "Data backup and restoration",
    #                       "Disaster recovery plan DRP",
    #                       "Cybersecurity risk management",
    #                       "Security software",
    #                       "Training, awareness-raising and communication",
    #                       "Network control",
    #                       "Verification control",
    #                       "Corporate cybersecurity incident response team"]

    # # Define the 23 lists of french tokens describing each of the 23 questions respectively
    # fr_question_tokens = ["Systèmes informatiques utilisés par l'entité pour l'établissement des rapports financiers et les processus opérationnels",
    #                       "Informations concernant les mises à jour ou les changements importants",
    #                       "Diagramme du système informatique DSI",
    #                       "Membres clés de l'organisation informatique",
    #                       "Fonctions clés de l'organisation informatique",
    #                       "Membres clés de l'équipe de l'organisation informatique",
    #                       "Composants externalisés",
    #                       "Domaines d'intervention, compétences requises, objectifs, méthode de supervision et clause d'audit pour les prestataires de services informatiques",
    #                       "Vérifier que l'accès aux applications se fait via un identifiant unique et nécessite un mot de passe",
    #                       "Obtenir la procédure de gestion des accès",
    #                       "S'assurer de l'existence d'une liste de profils applicatifs / d'une matrice de séparation des tâches",
    #                       "la politique de mot de passe définie au sein de l'entreprise et la cohérence des critères avec les meilleures pratiques",
    #                       "Obtenir et inspecter la procédure de gestion des changements",
    #                       "Obtenir et inspecter la méthodologie de développement des nouveaux systèmes",
    #                       "Gestion des incidents et des problèmes des utilisateurs",
    #                       "Sauvegarde et restauration des données",
    #                       "Plan de reprise après sinistre DRP",
    #                       "Gestion des risques de cybersécurité",
    #                       "Logiciels de sécurité",
    #                       "Formation, sensibilisation et communication",
    #                       "Contrôle du réseau",
    #                       "Contrôle de vérification",
    #                       "Équipe de réponse aux incidents de cybersécurité de l'entreprise"]
    
    # Define the 23 lists of english tokens describing each of the 23 questions respectively
    eng_question_tokens =[["IT system", "information system", "financial reporting", "purpose of IT system", "technology layers", "IT gouvernance", "accounting", "business process", "software", "application", "network", "database", "os", "operating system", "procedure", "Windows", "integrator", "oracle", "hms", "osbc", "hotix", "interfacing", "accounting", "purchase", "rh", "sales", "management"],
                          ["update", "change", "development", "system change"],
                          ["procedure", "process", "ISD", "IT system diagram", "diagram", "application", "network", "database", "os", "operating system","process", "IT system", "information system", "financial reporting", "purpose of IT system", "technology layers", "IT gouvernance", "accounting", "business process", "software", "application", "network", "database", "os", "operating system"],
                          ["IT organization", "members", "key members", "member name", "position", "team"],
                          ["IT service", "services", "activity", "IT department", "mission"],
                          ["IT organization", "members", "key members", "member name", "position", "team"],
                          ["providers", "service providers", "Outsourced service provider", "Outsourced service"],
                          ["skills","objectives", "supervision", "audit clause"],
                          ["access", "password", "unique identifier", "unique", "identifier"],
                          ["access management procedure", "procedure", "access management", "access"],
                          ["list of application profiles", "segregation of duties matrix", "application profiles", "segregation of duties"],
                          ["password", "password policy", "password length", "Upper case", "lower case", "numbers", "special characters", "password renewal", "initialization password"],
                          ["Application changes", "changes", "change management", "change"],
                          ["Acquisition", "development", "new","new system"],
                          ["incident and problem management procedures", "incident", "problem management", "incident management"],
                          ["Data backup", "recovery", "backup", "backup strategy", "data retention"],
                          ["DRP", "disaster recovery plan", "recovery", "disaster"],
                          ["Cybersecurity risk management", "cybersecurity", "security", "risk"],
                          ["security software", "software", "cybersecurity", "security"],
                          ["Training", "awareness", "communication", "cybersecurity", "security"],
                          ["network control", "network", "cybersecurity", "security", "network access"],
                          ["verification control", "verification", "cybersecurity", "security"],
                          ["cybersecurity incident response team", "team", "cybersecurity", "security", "members"]]
    eng_question_tokens = [' '.join(sublist) for sublist in eng_question_tokens]

    # Define the 23 lists of french tokens describing each of the 23 questions respectively
    fr_question_tokens = [["système informatique", "système d'information", "information financière", "objectif du système informatique", "couches technologiques", "gouvernance informatique", "comptabilité", "processus d'entreprise", "logiciel", "application", "réseau", "base de données", "os", "système d'exploitation", "procédure", "Windows", "intégrateur", "oracle", "hms", "osbc", "hotix", "interfaçage", "comptabilité", "achat", "rh", "ventes", "gestion"],
                          ["mise à jour", "changement", "développement", "changement de système"],
                          ["procédure", "processus", "DSI", "diagramme de système informatique", "diagramme", "application", "réseau", "base de données", "os", "système d'exploitation", "processus", "système informatique", "système d'information", "rapports financiers", "objectif du système informatique", "couches technologiques", "gouvernance informatique", "comptabilité", "processus d'entreprise", "logiciel", "application", "réseau", "base de données", "os", "système d'exploitation"],
                          ["organisation informatique", "membres", "membres clés", "nom du membre", "poste", "équipe"],
                          ["service informatique", "services", "activité", "département informatique", "mission"],
                          ["organisation informatique", "membres", "membres clés", "nom du membre", "fonction", "équipe"],
                          ["fournisseurs", "fournisseurs de services", "fournisseur de services externalisés", "service externalisé"],
                          ["compétences", "objectifs", "supervision", "clause d'audit"],
                          ["accès", "mot de passe", "identifiant unique", "unique", "identifiant"],
                          ["procédure de gestion des accès", "procédure", "gestion des accès", "accès"],
                          ["liste des profils d'application", "matrice de séparation des tâches", "profils d'application", "séparation des tâches"],
                          ["mot de passe", "politique en matière de mot de passe", "longueur du mot de passe", "majuscules", "minuscules", "chiffres", "caractères spéciaux", "renouvellement du mot de passe", "mot de passe d'initialisation"],
                          ["Changements d'application", "changements", "gestion des changements", "changement"],
                          ["Acquisition", "développement", "nouveau", "nouveau système"],
                          ["Procédures de gestion des incidents et des problèmes", "incident", "gestion des problèmes", "gestion des incidents"],
                          ["Sauvegarde des données", "récupération", "sauvegarde", "stratégie de sauvegarde", "conservation des données"],
                          ["PRA", "Plan de reprise d’activité", "restauration", "sésastre", "catastrophe"],
                          ["Gestion des risques de cybersécurité", "cybersécurité", "sécurité", "risque"],
                          ["logiciel de sécurité", "logiciel", "cybersécurité", "sécurité"],
                          ["Formation", "sensibilisation", "communication", "cybersécurité", "sécurité"],
                          ["contrôle du réseau", "réseau", "cybersécurité", "sécurité", "accès au réseau"],
                          ["contrôle de la vérification", "vérification", "cybersécurité", "sécurité"],
                          ["équipe de réponse aux incidents de cybersécurité", "équipe", "cybersécurité", "sécurité", "membres"]]
    fr_question_tokens = [" ".join(tokens) for tokens in fr_question_tokens]

    related_docs = []
    related_info = []
    for es, fs in zip(eng_section_tokens, fr_section_tokens):
        d = find_related_documents(doc_texts, es, fs)
        related_docs.append(d)
    
    for eq, fq in zip(eng_question_tokens, fr_question_tokens): 
        i = retrieve_info(eng_files, fr_files, eq, fq)
        related_info.append(i)      
        
    return render_template('question_answering.html', d0 = related_docs[0], d1 = related_docs[1], d2 = related_docs[2],
                           d3 = related_docs[3], d4 = related_docs[4], 
                           i0 = related_info[0], i1 = related_info[1], i2 = related_info[2], 
                           i3 = related_info[3], i4 = related_info[4], i5 = related_info[5], 
                           i6 = related_info[6], i7 = related_info[7], i8 = related_info[8], 
                           i9 = related_info[9], i10 = related_info[10], i11 = related_info[11],
                           i12 = related_info[12], i13 = related_info[13], i14 = related_info[14],
                           i15 = related_info[15], i16 = related_info[16], i17 = related_info[17],
                           i18 = related_info[18], i19 = related_info[19], i20 = related_info[20],
                           i21 = related_info[21], i22 = related_info[22])
     

if __name__ == '__main__':
    app.run(debug=True)
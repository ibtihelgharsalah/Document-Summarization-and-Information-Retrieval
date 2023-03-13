# A web application typically consists of a server that generates HTML pages, which are then rendered by a web 
# browser. Web applications are typically designed to serve a specific set of functions or tasks to users, 
# and the user interacts with the application through the browser's UI.

# BACKEND : server-side
import os # used to read and write files to the server's file system
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from NLP_preprocessing.text_extraction import extract_text
from NLP_preprocessing.language_detection import detect_language
from NLP_preprocessing.data_cleaning import eng_clean, fr_clean
from NLP_preprocessing.language_detection import detect_language
from utils.allowed_extention import allowed_file

app = Flask(__name__)

# Set the upload folder and files
UPLOAD_FOLDER = 'uploads' # 'uploads' is a folder on the server
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filenames = os.listdir(UPLOAD_FOLDER)

doc_texts= extract_text(app.config['UPLOAD_FOLDER'], filenames)
eng_texts, fr_texts, other_langs = detect_language(doc_texts)
eng_cleaned = eng_clean(eng_texts)
fr_cleaned = fr_clean(fr_texts)

# Main route to display the upload form (ask the user to upload files)
@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Get the files from the request object
        files = request.files.getlist('files[]')
        # Loop through each file and save it to the server's folder ('uploads') if the file has an allowed extension
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # redirects the user to the uploaded_files() route
        return redirect(url_for('uploaded_files'))
    
    # displays an HTML form that allows the user to select and upload files to the server.
    return render_template('upload.html') 

# Route to display the uploaded files
@app.route('/uploads')
def uploaded_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('uploaded.html', files=files)

# # Route to fetch the uploaded files and extract information to answer each question on the html page
# @app.route('/answer', methods=['GET'])
# def question_answering():
#     # Get the filenames of the uploaded files
#     files = os.listdir(app.config['UPLOAD_FOLDER'])
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

if __name__ == '__main__':
    app.run(debug=True)

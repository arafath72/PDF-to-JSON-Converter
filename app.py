from flask import Flask, request, render_template, send_file
import pdfplumber
import json
import os

app = Flask(__name__)

def pdf_to_json(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        text_data = [page.extract_text() for page in pages]
    return {"pages": text_data}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400
    
    pdf_file = request.files['pdf_file']
    json_data = pdf_to_json(pdf_file)
    
    json_filename = 'output.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)
    
    return send_file(json_filename, as_attachment=True)  # Ensure it downloads immediately


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, send_file
from pypdf import PdfReader, PdfWriter
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def delete_pages():
    file = request.files['file']
    delete_pages = list(map(int, request.form.get('pages', '').split(',')))

    reader = PdfReader(file)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i + 1 not in delete_pages:
            writer.add_page(page)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    writer.write(temp_file)
    temp_file.seek(0)

    return send_file(temp_file.name, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')

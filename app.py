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

@app.route('/')
def home():
    return "PDF Deletion API is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

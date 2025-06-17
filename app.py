from flask import Flask, request, send_file, jsonify
from pypdf import PdfReader, PdfWriter
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def delete_pages():
    if 'file' not in request.files:
        return jsonify({"error": "Missing file"}), 400
    if 'pages' not in request.form:
        return jsonify({"error": "Missing pages field"}), 400

    file = request.files['file']
    try:
        delete_pages = list(map(int, request.form.get('pages', '').split(',')))
    except ValueError:
        return jsonify({"error": "Invalid page numbers"}), 400

    reader = PdfReader(file)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i + 1 not in delete_pages:
            writer.add_page(page)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    writer.write(temp_file)
    temp_file.seek(0)

    return send_file(temp_file.name, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

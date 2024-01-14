from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfFileMerger

app = Flask(__name__)


@app.route('/PDF')
def index():
    # return render_template('./PDF/Merge_PDF.html')
    return render_template('./PDF/index.html')


@app.route('/', methods=['POST'])
def merge_pdf():
    files = request.files.getlist('pdf_files')
    filename = request.form['pdf_filename']

    merger = PdfFileMerger()
    for file in files:
        merger.append(file)

    merged_file_path = f'{filename}.pdf' if filename else 'merged.pdf'
    merger.write(merged_file_path)
    merger.close()

    return render_template('Merge_PDF_Down.html', filename=merged_file_path)


@app.route('/download/<filename>')
def download_pdf(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run()

#-*-coding:utf-8-*-

import math
from flask import Flask, request, render_template, send_file,  redirect, url_for
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfMerger


app = Flask(__name__)


def calculate_amortization(principal, interest_rate, time):
    rate = interest_rate / 100
    monthly_interest_rate = rate / 12
    months = time * 12

    # 월별 이자 지급 계산
    monthly_payment = principal * (monthly_interest_rate / (1 - math.pow(1 + monthly_interest_rate, -months)))

    # 상환 계획
    amortization_schedule = []
    for i in range(months):
        interest_payment = principal * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        principal -= principal_payment
        amortization_schedule.append((i + 1, monthly_payment, principal_payment, interest_payment))

    return amortization_schedule


def recommend_products():
    products = [
        {'bank': '시중은행1', 'name': '상품A', 'interest_rate': 3.9},
        {'bank': '시중은행2', 'name': '상품B', 'interest_rate': 4.5},
        {'bank': '시중은행3', 'name': '상품C', 'interest_rate': 4.8},
        {'bank': '시중은행4', 'name': '상품D', 'interest_rate': 5.1},
        {'bank': '시중은행5', 'name': '상품E', 'interest_rate': 5.6},
    ]
    return products

'''대출 계산기'''
@app.route("/lone/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        principal = request.form["principal"]
        interest_rate = request.form["interest_rate"]
        time = request.form["time"]

        return redirect(url_for("result", principal=principal, interest_rate=interest_rate, time=time))

    recommended_products = recommend_products()
    return render_template("index.html", products=recommended_products)

@app.route("/lone/result", methods=["GET"])
def result():
    principal = float(request.args.get("principal"))
    interest_rate = float(request.args.get("interest_rate"))
    time = int(request.args.get("time"))

    amortization_schedule = calculate_amortization(principal, interest_rate, time)
    recommended_products = recommend_products()

    return render_template("index.html", schedule=amortization_schedule, products=recommended_products,
                           principal=principal, interest_rate=interest_rate, time=time)


@app.route('/PDF')
def Merge_PDF():
    return render_template('./PDF/Merge_PDF.html')

@app.route('/PDF/merge', methods=['POST'])
def merge_pdf():
    print("merge_pdf")
    files = request.files.getlist('pdf_files')
    filename = request.form['pdf_filename']
    print(files)

    # merger = PdfFileMerger()
    merger = PdfMerger()

    for file in files:
        merger.append(file)

    merged_file_path = f'{filename}.pdf' if filename else 'merged.pdf'
    merger.write(merged_file_path)
    merger.close()

    return render_template('./PDF/Merge_PDF_Down.html', filename=merged_file_path)


@app.route('/download/<filename>')
def download_pdf(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

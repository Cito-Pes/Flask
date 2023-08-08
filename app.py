import math
from flask import Flask, render_template, request, redirect, url_for

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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        principal = request.form["principal"]
        interest_rate = request.form["interest_rate"]
        time = request.form["time"]

        return redirect(url_for("result", principal=principal, interest_rate=interest_rate, time=time))

    recommended_products = recommend_products()
    return render_template("index.html", products=recommended_products)

@app.route("/result", methods=["GET"])
def result():
    principal = float(request.args.get("principal"))
    interest_rate = float(request.args.get("interest_rate"))
    time = int(request.args.get("time"))

    amortization_schedule = calculate_amortization(principal, interest_rate, time)
    recommended_products = recommend_products()

    return render_template("index.html", schedule=amortization_schedule, products=recommended_products,
                           principal=principal, interest_rate=interest_rate, time=time)


if __name__ == "__main__":
    app.run(debug=True)

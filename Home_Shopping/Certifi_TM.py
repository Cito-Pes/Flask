from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyodbc
import os

app = Flask(__name__)


# MSSQL DB 연결 설정
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')
    return conn


# 데이터 조회 함수
def get_data():
    conn = get_db_connection()
    query = "SELECT 상담사명, COUNT(*) AS 계약건수 FROM 상담실적 GROUP BY 상담사명"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# 그래프 생성 함수
def create_bar_chart(data):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(data['상담사명'], data['계약건수'], color='lightblue')

    # 가장 많은 계약건수를 가진 상담사 색상 변경
    max_value = data['계약건수'].max()
    for bar in bars:
        if bar.get_height() == max_value:
            bar.set_color('orange')

    # 막대 위에 계약건수 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

    plt.xlabel('상담사명')
    plt.ylabel('계약건수')
    plt.title('고객센터 실적 현황')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 이미지 저장
    img_path = 'static/bar_chart.png'
    plt.savefig(img_path)
    plt.close()
    return img_path


@app.route('/')
def index():
    return render_template('Certifi_TM.html')


@app.route('/update_chart')
def update_chart():
    data = get_data()
    img_path = create_bar_chart(data)
    return jsonify({'img_path': img_path})


if __name__ == '__main__':
    app.run(debug=True)

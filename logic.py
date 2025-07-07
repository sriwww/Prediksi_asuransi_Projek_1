
import pandas as pd
import mysql.connector
from mysql.connector import Error
import joblib
import streamlit as st

#load model
try:
    model = joblib.load('Prediksi_premi_asuransi_p1.pkl')
    print("Model berhasil dimuat.")
except FileNotFoundError:
    raise FileNotFoundError("Model file tidak ditemukan.")

#fungsi create_connection
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='asuransi_projek1' #diisi dengan nama database
        )
        return conn
    except Error as e:
        raise ConnectionError(f"Koneksi gagal: {e}")

#buat prediksi
def predict_insurance_premium(data: dict, model):
    # Konversi input menjadi format numerik sesuai model
    input_df = pd.DataFrame([{
        'age': data['age'],
        'sex': 1 if data['sex'] == 'male' else 0,
        'bmi': data['bmi'],
        'children': data['children'],
        'smoker': 1 if data['smoker'] == 'yes' else 0,# default to 0 if not found
    }])
    input_df = input_df[['age', 'sex', 'bmi', 'children', 'smoker']]
    prediction = model.predict(input_df)[0]
    
    return prediction,input_df

#fungsi save to database
def save_to_database(nama: str, data: dict, predicted_charges: float):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO predictions (
            nama, age, sex, bmi, children, smoker, predicted_charges
        ) VALUES (%s,%s, %s, %s, %s, %s, %s)
    """, (
        nama,
        data['age'],
        data['sex'],
        data['bmi'],
        data['children'],
        data['smoker'],
        predicted_charges
    ))
    
    conn.commit()
    cursor.close()
    conn.close()

#menampilkan semua data
def fetch_all_predictions():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM predictions ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    cursor.close()
    conn.close()
    return df


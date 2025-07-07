
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from logic import *

# Styling CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    h1 {
        color: #4B8BBE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💊 Aplikasi Prediksi Biaya Asuransi Kesehatan")
st.write("Aplikasi ini memperkirakan biaya premi asuransi kesehatan berdasarkan informasi dari pengguna.")

st.subheader("🧾 Masukkan Data Calon Nasabah")
col1, col2 = st.columns(2)

with col1:
    nama = st.text_input('Nama Lengkap')
    age = st.slider('Usia', 18, 65, 30)
    sex = st.selectbox('Jenis Kelamin', ['male', 'female'])
    bmi = st.number_input('BMI (Body Mass Index)', min_value=10.0, max_value=100.0, value=25.0)

with col2:
    children = st.number_input('Jumlah Anak', min_value=0, max_value=5, value=0)
    smoker = st.selectbox('Perokok?', ['yes', 'no'])

sex_encoded = 1 if sex == 'male' else 0
smoker_encoded = 1 if smoker == 'yes' else 0

data = {
    'age': age,
    'sex': sex_encoded,
    'bmi': bmi,
    'children': children,
    'smoker': smoker_encoded
}

if st.button('📈 Prediksi Biaya Asuransi'):
    if nama.strip() == "":
        st.warning("Silakan masukkan nama lengkap terlebih dahulu.")
    else:
        try:
            prediction, input_df = predict_insurance_premium(data, model)
            st.success(f"Biaya Asuransi Diprediksi: Rp {prediction:,.2f}")
            save_to_database(nama, data, prediction)
            st.info("✅ Hasil prediksi berhasil disimpan ke database.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

st.markdown("---")
st.subheader("📊 Data Hasil Prediksi Biaya Asuransi yang Tersimpan")

if st.button("📂 Tampilkan Data dari Database"):
    try:
        df = fetch_all_predictions()
        if df.empty:
            st.info("Belum ada data prediksi yang disimpan.")
        else:
            st.dataframe(df)

            st.subheader("📈 Visualisasi Data Prediksi")

            # Histogram Umur
            st.markdown("**Distribusi Umur**")
            fig1, ax1 = plt.subplots()
            sns.histplot(df['age'], bins=10, kde=True, ax=ax1)
            st.pyplot(fig1)

            # Visualisasi Berdampingan: Jenis Kelamin
            st.subheader("Distribusi Premi dan Jumlah Data Berdasarkan Jenis Kelamin")
            col1, col2 = st.columns(2)

            with col1:
                fig_gender_mean, ax_mean = plt.subplots()
                gender_avg = df.groupby('sex')['predicted_charges'].mean().reset_index()
                gender_avg['sex'] = gender_avg['sex'].map({0: 'Perempuan', 1: 'Laki-laki'})
                ax_mean.pie(
                    gender_avg['predicted_charges'],
                    labels=gender_avg['sex'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['#d0b3ff', '#ffcc99']
                )
                ax_mean.set_title("Rata-rata Premi")
                ax_mean.axis('equal')
                st.pyplot(fig_gender_mean)

            with col2:
                fig_gender_count, ax_count = plt.subplots()
                gender_count = df['sex'].value_counts().reset_index()
                gender_count.columns = ['sex', 'jumlah']
                gender_count['sex'] = gender_count['sex'].map({0: 'Perempuan', 1: 'Laki-laki'})
                ax_count.pie(
                    gender_count['jumlah'],
                    labels=gender_count['sex'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['#c2c2f0', '#ff9999']
                )
                ax_count.set_title("Jumlah Data")
                ax_count.axis('equal')
                st.pyplot(fig_gender_count)

            # Visualisasi Berdampingan: Status Perokok
            st.subheader("Distribusi Premi dan Jumlah Data Berdasarkan Status Perokok")
            col3, col4 = st.columns(2)

            with col3:
                fig_smoker_mean, ax_smoker_mean = plt.subplots()
                smoker_avg = df.groupby('smoker')['predicted_charges'].mean().reset_index()
                smoker_avg['smoker'] = smoker_avg['smoker'].map({0: 'Non-Perokok', 1: 'Perokok'})
                ax_smoker_mean.pie(
                    smoker_avg['predicted_charges'],
                    labels=smoker_avg['smoker'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['#AED6F1', '#F5B7B1']
                )
                ax_smoker_mean.set_title("Rata-rata Premi")
                ax_smoker_mean.axis('equal')
                st.pyplot(fig_smoker_mean)

            with col4:
                fig_smoker_count, ax_smoker_count = plt.subplots()
                smoker_count = df['smoker'].value_counts().reset_index()
                smoker_count.columns = ['smoker', 'jumlah']
                smoker_count['smoker'] = smoker_count['smoker'].map({0: 'Non-Perokok', 1: 'Perokok'})
                ax_smoker_count.pie(
                    smoker_count['jumlah'],
                    labels=smoker_count['smoker'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['#A2D9CE', '#F1948A']
                )
                ax_smoker_count.set_title("Jumlah Data")
                ax_smoker_count.axis('equal')
                st.pyplot(fig_smoker_count)

    except Exception as e:
        st.error(f"Gagal menampilkan data: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center;'>🚀 Dibuat oleh SRI CAHYANI & SITI KHAIRIYAH | Data Science Project I</p>", unsafe_allow_html=True)

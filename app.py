import pymysql
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

# Membuat koneksi ke database MySQL
conn = pymysql.connect(
    host="kubela.id",
    port=3306,
    user="davis2024irwan",
    password="wh451n9m@ch1n3",
    database="aw"
)

# Membuat cursor
cursor = conn.cursor()

# Cek koneksi berhasil
if conn:
    print('Connected to MySQL database')

# Query SQL untuk mengambil data penjualan per tahun
query_cust = """
    SELECT dc.Gender, COUNT(fs.CustomerKey) AS TotalCustomers
    FROM dimcustomer dc
    LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
    GROUP BY dc.Gender;
"""

# Eksekusi query
cursor.execute(query_cust)

# Mendapatkan hasil query sebagai tuple
data = cursor.fetchall()

# Menutup cursor dan koneksi database
cursor.close()
conn.close()

# Membuat DataFrame dari hasil query
df_customer = pd.DataFrame(data, columns=['Gender', 'TotalCustomers'])

# Menampilkan judul dashboard
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

# Menampilkan DataFrame di Streamlit dalam bentuk tabel
st.subheader('1. Comparison (perbandingan)')
st.dataframe(df_customer)

# Plot perbandingan total penjualan per tahun dengan Matplotlib
plt.figure(figsize=(12, 6))
plt.bar(df_customer['Gender'], df_customer['TotalCustomers'], color=['blue', 'pink'], alpha=0.6)
plt.title('Total Customer by Gender')
plt.xlabel('Gender')
plt.ylabel('Total Customer')
plt.grid(True)

# Menampilkan plot di Streamlit
st.markdown(f"<h2 style='text-align: center;'>Grafik Total Customer </h2>", unsafe_allow_html=True)
st.pyplot(plt)

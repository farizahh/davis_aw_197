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

# Cek koneksi berhasil
if conn:
    print('Connected to MySQL database')

# Mengambil data dari tabel users dan product_fact
gender= "SELECT Gender, CustomerKey FROM dimcustomer"
customer= "SELECT CustomerKey FROM factinternetsales"

df_gender = pd.read_sql(gender, engine)
df_customer = pd.read_sql(customer, engine)

# Melakukan join tabel users dan product_fact berdasarkan UserID
df_merged = pd.merge(df_customer, df_gender, on='CustomerKey')

# Menutup koneksi setelah selesai digunakan
conn.close()

# Mengagregasi data penjualan per gender
df_aggregated = df_merged.groupby('Gender').agg({
    'CustomerKey': 'count'
}).reset_index()

# Menampilkan hasil agregasi untuk verifikasi
st.write(df_aggregated)

# Membuat bar chart untuk visualisasi
st.bar_chart(df_aggregated.set_index('Gender'))

# Menambahkan label dan judul
plt.xlabel('Gender')
plt.ylabel('Total Customer')
plt.title('Total Customer by Gender')
plt.xticks(rotation=0)
plt.show()

# Menampilkan plot di Streamlit
st.markdown(f"<h2 style='text-align: center;'>Total Customer By Gender </h2>", unsafe_allow_html=True)
st.pyplot(plt)

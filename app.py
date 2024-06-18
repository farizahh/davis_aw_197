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

# Query SQL untuk mengambil data pelanggan
query_cust = """
    SELECT dc.Gender, COUNT(fs.CustomerKey) AS TotalCustomers
    FROM dimcustomer dc
    LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
    GROUP BY dc.Gender;
"""

# Query SQL untuk mengambil data order quantity dari setiap unit price
query_order = """
    SELECT dc.CustomerKey, SUM(fs.OrderQuantity) AS TotalOrderQuantity, fs.SalesAmount
    FROM dimcustomer dc
    LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
    GROUP BY dc.CustomerKey;
"""

# Eksekusi query untuk mengambil data pelanggan
cursor.execute(query_cust)
data_cust = cursor.fetchall()

# Eksekusi query untuk mengambil data order
cursor.execute(query_order)
data_order = cursor.fetchall()

# Menutup cursor dan koneksi database
cursor.close()
conn.close()

# Membuat DataFrame dari hasil query
df_customer = pd.DataFrame(data_cust, columns=['Gender', 'TotalCustomers'])
df_order = pd.DataFrame(data_order, columns=['TotalOrderQuantity', 'SalesAmount'])

# Menampilkan judul dashboard
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

# 1. Comparison
st.subheader('1. Comparison (perbandingan)')
st.dataframe(df_customer)
plt.figure(figsize=(12, 6))
plt.bar(df_customer['Gender'], df_customer['TotalCustomers'], color=['blue', 'pink'], alpha=0.6)
plt.title('Total Customer by Gender')
plt.xlabel('Gender')
plt.ylabel('Total Customer')
plt.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(plt)

#2 Relationship 
st.subheader('2. Relationship (hubungan)')
st.dataframe(df_order)
plt.figure(figsize=(12, 6))
plt.scatter(df_order['TotalOrderQuantity'], df_order['SalesAmount'], alpha=0.5)
plt.title('Relationship between Order Quantity and Sales Amount')
plt.xlabel('Order Quantity')
plt.ylabel('Sales Amount')
plt.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(plt)

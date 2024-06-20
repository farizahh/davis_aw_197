import pandas as pd
import streamlit as st
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membaca data IMDB
def load_imdb_data():
    fn1 = 'imdb_top.csv'
    df1 = pd.read_csv(fn1, encoding='latin1')
    return df1

# Fungsi untuk membuat visualisasi
# def visualize_top_10(df):
#     # Ambil 10 baris pertama
#     top_10 = df.head(10)

#     # Ambil kolom yang relevan
#     judul_film = top_10['judul']
#     rating = top_10['rating']

#     # Buat visualisasi
#     plt.figure(figsize=(10, 8))
#     plt.barh(judul_film, rating, color='skyblue')
#     plt.title('Top 10 Rating Film di IMDB')
#     plt.xlabel('Rating')
#     plt.ylabel('Judul Film')
#     st.pyplot(plt)
    
# Fungsi untuk mengambil data dari database MySQL
def load_adventure_works_data():
    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
    )
    cursor = conn.cursor()

    query_cust = """
        SELECT dc.Gender, COUNT(fs.CustomerKey) AS TotalCustomers
        FROM dimcustomer dc
        LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
        GROUP BY dc.Gender;
    """
    query_order = """
        SELECT dc.CustomerKey, SUM(fs.OrderQuantity) AS TotalOrderQuantity, SUM(fs.SalesAmount) AS TotalSalesAmount
        FROM dimcustomer dc
        LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
        GROUP BY dc.CustomerKey;
    """
    query_sales = """
        SELECT p.EnglishProductName, SUM(s.SalesAmount) AS TotalSales
        FROM factinternetsales s
        INNER JOIN dimproduct p ON s.ProductKey = p.ProductKey
        GROUP BY p.EnglishProductName
    """
    query_total = """
        SELECT SalesAmount
        FROM factinternetsales
    """

    cursor.execute(query_cust)
    data_cust = cursor.fetchall()

    cursor.execute(query_order)
    data_order = cursor.fetchall()

    cursor.execute(query_sales)
    data_sales = cursor.fetchall()

    cursor.execute(query_total)
    data_total = cursor.fetchall()

    cursor.close()
    conn.close()

    df_customer = pd.DataFrame(data_cust, columns=['Gender', 'TotalCustomers'])
    df_order = pd.DataFrame(data_order, columns=['CustomerKey', 'TotalOrderQuantity', 'TotalSalesAmount'])
    df_sales = pd.DataFrame(data_sales, columns=['EnglishProductName', 'TotalSales'])
    df_total = pd.DataFrame(data_total, columns=['SalesAmount'])

    return df_customer, df_order, df_sales, df_total

# Menampilkan judul di halaman web
st.title("Final Project Data Visualisasi")

# Menambahkan sidebar
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Menampilkan data sesuai pilihan di sidebar
if option == 'IMDB Top Movies':
    df_imdb = load_imdb_data()
    st.title("Scraping Website IMDB")

    # Tampilkan tabel aslinya
    st.subheader("Tabel Data IMDB")
    st.dataframe(df_imdb)

    # # Buat visualisasi untuk 10 baris teratas
    # st.subheader("Visualisasi Top 10 Rating Film di IMDB")
    # visualize_top_10(df_imdb)

    # 1. Comparison
    st.subheader('1. Comparison (perbandingan)')
    st.write("Visualisasi di bawah ini menunjukkan distribusi rating film per tahun. Dapat di lihat bagaimana rating film bervariasi dari tahun ke tahun.")
    sns.boxplot(x='tahun', y='rating', data=df_imdb)
    plt.title('Rating per Tahun di IMDB (Boxplot)')
    plt.xlabel('Tahun')
    plt.ylabel('Rating')
    st.pyplot(plt)

    # 2. Relationship 
    st.subheader('2. Relationship (hubungan)')
    st.write("Visualisasi di bawah ini menunjukkan hubungan antara durasi film dan rating di IMDB. Warna pada titik-titik menunjukkan tahun rilis film.")
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='durasi', y='rating', hue='tahun', data=df_imdb)
    plt.title('Relationship antara Durasi dan Rating di IMDB')
    plt.xlabel('Durasi (menit)')
    plt.ylabel('Rating')
    st.pyplot(plt)

    # 3. Composition (komposisi)
    st.subheader('3. Composition (komposisi)')
    st.write("Visualisasi di bawah ini menunjukkan komposisi klasifikasi usia penonton untuk film berdasarkan data dari IMDB. Dapat di lihat persentase setiap kelompok umur yang telah menonton film-film ini.")
    plt.figure(figsize=(10, 8))
    df_imdb['umur'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Komposisi usia penonton untuk film di IMDB')
    st.pyplot(plt)

    # 4. Distribution (distribusi)
    st.subheader('4. Distribution (distribusi)')
    st.write("Visualisasi di bawah ini menunjukkan distribusi rating film di IMDB. Histogram ini memperlihatkan bagaimana rating film tersebar dan juga menampilkan kurva kepadatan kernel (KDE) untuk memberikan gambaran lebih halus tentang distribusi rating.")
    plt.figure(figsize=(10, 8))
    sns.histplot(df_imdb['rating'], kde=True, bins=20)
    plt.title('Distribusi Rating Film di IMDB')
    plt.xlabel('Rating')
    plt.ylabel('Frekuensi')
    st.pyplot(plt)

else:
    df_customer, df_order, df_sales, df_total = load_adventure_works_data()
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)
    
    # 1. Comparison
    st.subheader('1. Comparison (perbandingan)')
    st.write("Visualisasi ini digunakan untuk melihat perbandingan gender yang ada dari total customer, dalam arti lain visualisasi ini membantu untuk mencari tahu berapa jumlah customer wanita, dan berapa jumlah customer dari pria.")
    st.dataframe(df_customer)
    plt.figure(figsize=(12, 6))
    plt.bar(df_customer['Gender'], df_customer['TotalCustomers'], color=['blue', 'pink'], alpha=0.6)
    plt.title('Total Customer by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Total Customer')
    plt.grid(True)
    st.pyplot(plt)

    # 2. Relationship 
    st.subheader('2. Relationship (hubungan)')
    st.write("Visualisasi ini digunakan untuk melihat hubungan antara jumlah pembelian customer dengan harga suatu produk.")
    st.dataframe(df_order)
    plt.figure(figsize=(12, 6))
    plt.scatter(df_order['TotalOrderQuantity'], df_order['TotalSalesAmount'], c=df_order['CustomerKey'], cmap='viridis', alpha=0.5)
    plt.title('Relationship between Order Quantity, Sales Amount, and CustomerKey')
    plt.xlabel('Total Order Quantity')
    plt.ylabel('Total Sales Amount')
    plt.colorbar(label='CustomerKey')  # Menambahkan colorbar untuk menunjukkan keterangan warna
    plt.grid(True)
    st.pyplot(plt)

    # 3. Composition (komposisi)
    st.subheader('3. Composition (komposisi)')
    st.write("Visualisasi di bawah ini menunjukkan distribusi total penjualan. Histogram ini memperlihatkan bagaimana penjualan total tersebar di dataset.")
    st.dataframe(df_sales)
    plt.figure(figsize=(10, 6))
    plt.hist(df_sales['TotalSales'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Total Sales')
    plt.xlabel('Total Sales')
    plt.ylabel('Frequency')
    plt.grid(True)
    st.pyplot(plt)

    # 4. Distribution (distribusi)
    st.subheader('4. Distribution (distribusi)')
    st.write("Visualisasi di bawah ini menunjukkan estimasi kepadatan kernel (KDE) dari jumlah penjualan. Grafik ini memberikan gambaran lebih halus tentang distribusi jumlah penjualan.")
    st.dataframe(df_total)
    plt.figure(figsize=(10, 6))
    sns.kdeplot(df_total['SalesAmount'], color='skyblue', fill=True)
    plt.title('Kernel Density Estimation of Sales Amount')
    plt.xlabel('Sales Amount')
    plt.ylabel('Density')
    plt.grid(True)
    st.pyplot(plt)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# from babel.numbers import format_currency
sns.set(style='dark')
# kategori produk terlaros
# bulan dengan penjualan tertinggi
# rata-rata penghasilan 
# select tanggal / penghasilan
# maksimum - minimum produk
# order tertinggi
# total penjualan
# Helper function memoersiapkan dataframe
# def summarize_data(df):
#     summary = {
#         "total_orders": df["order_id"].nunique(),
#         "total_revenue": df["total_price"].sum(),
#         "average_order_value": df["total_price"].mean()
#     }
#     return summary

st.header("Dashboard Penjualan Produk")
all_data = pd.read_csv("../data/all_data.csv")
kolom_orderan = ['order_purchase_timestamp']
all_data.sort_values(by='order_purchase_timestamp', inplace=True)
all_data.reset_index(inplace=True)

for kolom_data in kolom_orderan:
    all_data[kolom_data] = pd.to_datetime(all_data[kolom_data])
# Filter Data
min_date = all_data['order_purchase_timestamp'].min()
max_date = all_data['order_purchase_timestamp'].max()
with st.sidebar:
    st.image("../data/img.png")
    st.title("Filter Data")
    start_date, end_date = st.date_input(
        label="Pilih rentang tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# filter data
filtered_data=all_data[
    (all_data['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
    (all_data['order_purchase_timestamp'] <= pd.Timestamp(end_date))
]

# ringkasan data
#  
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 Best-Selling Categories")
    top_products = filtered_data.groupby('product_category_name').size().sort_values(ascending=False).head(5)
    st.bar_chart(top_products)
with col2:
    st.subheader("Bottom 5 Least-Selling Categories")
    low_products = filtered_data.groupby('product_category_name').size().sort_values(ascending=True).head(5)
    st.bar_chart(low_products)

# reviews
st.subheader("Rata-rata Rating Berdasarkan Produk")
avg_review=filtered_data.groupby(by="product_category_name").review_score.mean().sort_values(ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x=avg_review.values,
    y=avg_review.index,
    palette="viridis",
    ax=ax
)
ax.set_title("Rata-rata Review Score Berdasarkan Nama Produk", fontsize=16)
ax.set_xlabel("Skor Review Rata-Rata", fontsize=12)
ax.set_ylabel("Nama Produk", fontsize=12)
st.pyplot(fig)

# payments
# Hitung jumlah transaksi dan total nilai pembayaran per metode pembayaran
payment_counts = filtered_data['payment_type'].value_counts().head(6)
payment_sums = filtered_data.groupby("payment_type")["payment_value"].sum().head(6)

# Gabungkan data dalam satu DataFrame
payment_summary = pd.DataFrame({
    'payment_count': payment_counts,
    'payment_value': payment_sums
}).sort_values(by='payment_value', ascending=False)

# Menampilkan hasil pie chart yang sudah ada
st.subheader("Metode Pembayaran yang Sering Digunakan")

# Warna untuk pie chart
colors = ['#8B4513', '#FFF8DC', '#93C572', '#E67F0D', '#69BE28', '#4682B4']
explode = [0.1 if i == 0 else 0 for i in range(len(payment_summary))]  # Highlight kategori terbesar

# Membuat Donut Chart
fig, ax = plt.subplots(figsize=(10, 7))
wedges, texts, autotexts = ax.pie(
    x=payment_summary['payment_value'],
    labels=payment_summary.index,
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    startangle=90,
    textprops={'fontsize': 10},
    wedgeprops={'width': 0.6}  # Lebar pie untuk membuat lubang di tengah
)

# Tambahkan Judul
ax.set_title("Proporsi Metode Pembayaran", fontsize=16)

# Tampilkan Chart
st.pyplot(fig)

# Menampilkan Dataframe dengan count dan total pembayaran
st.text("Detail Metode Pembayaran:")
st.write(payment_summary)

# Order tertinggi
# st.subheader("Penjualan Produk")
# fig,ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
# colors =["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3" ]
# sns.barplot(x="total_penjualan", y="product_category_name").size().sort_values(ascending=False).head(5)
# ax[0].set_ylabel(None)
# ax[0].set_xlabel("Penjualan", fontsize=30)
# ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=35)
# ax[0].tick_params(axis='x', labelsize=30)



# Product performance best seller
st.subheader("Rincian Penjualan ")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Bulan dengan Penjualan Tertinggi")
    filtered_data['month'] = filtered_data['order_purchase_timestamp'].dt.to_period('M')
    # Menghitung total penjualan per bulan
    monthly_sales = filtered_data.groupby('month')['payment_value'].sum().sort_values(ascending=False).head(10)
    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, palette='viridis', ax=ax)

    # Menambahkan label dan judul
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Total Penjualan', fontsize=12)
    ax.set_title('Total Penjualan per Bulan', fontsize=14)
    # Menampilkan grafik
    st.pyplot(fig)
    # Menampilkan tabel dengan total penjualan per bulan
    st.text("Rincian Penjualan per Bulan:")
    st.write(monthly_sales)

with col2:
    st.subheader("Bulan dengan Penjualan Terendah")
    filtered_data['month'] = filtered_data['order_purchase_timestamp'].dt.to_period('M')
    # Menghitung total penjualan per bulan
    monthly_sales = filtered_data.groupby('month')['payment_value'].sum().sort_values(ascending=True).head(10)
    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, palette='viridis', ax=ax)
    # Menambahkan label dan judul
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Total Penjualan', fontsize=12)
    ax.set_title('Total Penjualan per Bulan', fontsize=14)
    # Menampilkan grafik
    st.pyplot(fig)
# Menampilkan tabel dengan total penjualan per bulan
    st.text("Rincian Penjualan Paling Sedikit:")
    st.write(monthly_sales)

# st.subheader("Penjualan Terbanyak Seller berdasarkan Negara")
# top_sellers = (
#     filtered_data.groupby("seller_id").agg(
#         seller_city=("seller_city", "first"),
#         banyak_penjualan=("product_id", "count")
# ).reset_index()
# )
# sales_by_city = top_sellers.groupby["seller_city"]["banyak_penjualan"].sum().sort_values(ascending=False).reset_index()
# top_cities= sales_by_city.head(5)
# fig, ax = plt.subplots(figsize(10,6))
# sns.barplot(
#     x='banyak_penjualan',
#     y='seller_city',
#     data=top_cities,
#     palette="Blues_r",
#     ax=ax
# )
# ax.set_xlabel("Jumlah Penjualan", fontsize=12)
# ax.set_ylabel("Kota Seller", fontsize=12)
# ax.set_title("Top 5 Kota Seller dengan Penjualan Terbanyak", fontsize=14)
# st.pyplot(fig)


# RFM
st.subheader("Best Products on RFM Parameters")
col1, col2 = st.columns(2)

with col1: 
    st.subheader("Transaksi Terakhir")
    transaksi_terakhir = filtered_data[['order_id', 'customer_id', 'order_purchase_timestamp']]
    transaksi_terakhir['order_purchase_timestamp'] = pd.to_datetime(transaksi_terakhir['order_purchase_timestamp'])
    transaksi_terakhir_sorted = transaksi_terakhir.sort_values(by='order_purchase_timestamp', ascending=False).head(5)
    st.write(transaksi_terakhir_sorted)
    last_transaction=transaksi_terakhir_sorted.iloc[0]
    # st.write("Trasaksi Terakhir", last_transaction)
    # plt.figure(figsize=(10, 6))
    # plt.bar(transaksi_terakhir_sorted['order_id'].astype(str), transaksi_terakhir_sorted['customer_id'])
    # plt.xlabel('Order ID')
    # plt.ylabel('Customer ID')
    # plt.title('Bar Chart - 5 Transaksi Terakhir')
    # plt.xticks(rotation=45)
    # st.pyplot(plt)


with col2:
    st.subheader("Pengeluaran Pelanggan")
    pengeluaran_per_hari = (
        filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.date)
        .price.sum()
        .reset_index()
        .rename(columns={'order_purchase_timestamp': 'tanggal', 'price': 'total_pengeluaran'})
    )
    st.line_chart(pengeluaran_per_hari.set_index('tanggal')['total_pengeluaran'])

# col3 = st.columns(1)
# with col3:
st.subheader("Data Transaksi")
penjualan_per_tahun=(
    all_data.groupby(all_data['order_purchase_timestamp'].dt.year)
.price.sum()
.reset_index()
.rename(columns={'order_purchase_timestamp': 'tahun', 'price': 'total_pendapatan'})
)
# Mendapatkan tahun dengan penjualan tertinggi
hasil_per_tahun = penjualan_per_tahun.loc[penjualan_per_tahun['total_pendapatan'].idxmax()]
# Menampilkan teks informasi
st.subheader("Penjualan Per Tahun")
st.write(f"Tahun dengan penjualan tertinggi: **{int(hasil_per_tahun['tahun'])}** dengan total pendapatan **{hasil_per_tahun['total_pendapatan']:.2f}**.")

# Membuat visualisasi bar chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='tahun',
    y='total_pendapatan',
    data=penjualan_per_tahun,
    palette="Blues_d",
    ax=ax
)

# Menambahkan label dan judul
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Total Pendapatan", fontsize=12)
ax.set_title("Penjualan Per Tahun", fontsize=14)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Menampilkan tabel data untuk informasi tambahan
st.text("Detail Pendapatan Per Tahun:")
st.write(penjualan_per_tahun)




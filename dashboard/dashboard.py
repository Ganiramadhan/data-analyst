import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset pelanggan dan produk
df_customers = pd.read_csv("data/customers_dataset.csv", encoding='utf-8')
df_products = pd.read_csv("data/products_dataset.csv", encoding='utf-8')

# Hitung distribusi pelanggan berdasarkan negara bagian dan kota
customer_distribution = df_customers.groupby(["customer_state", "customer_city"]) \
    ["customer_unique_id"].nunique().reset_index()

# Ambil 10 negara bagian dengan jumlah pelanggan terbanyak
top_states = customer_distribution.groupby("customer_state") \
    ["customer_unique_id"].sum().sort_values(ascending=False).head(10)

# Ambil 10 kota dengan jumlah pelanggan terbanyak
top_cities = customer_distribution.groupby("customer_city") \
    ["customer_unique_id"].sum().sort_values(ascending=False).head(10)

# Hitung rata-rata berat produk yang tersedia
avg_product_weight = df_products["product_weight_g"].mean()

# Hitung jumlah pelanggan per negara bagian
customer_count_by_state = df_customers["customer_state"].value_counts().reset_index()
customer_count_by_state.columns = ["customer_state", "customer_count"]
customer_count_by_state["avg_product_weight"] = avg_product_weight

# Judul dashboard
st.title("📊 Customer & Product Analysis Dashboard")

# Sidebar untuk filter dan pilihan data
st.sidebar.header("Filter Data")
option = st.sidebar.radio("Pilih Data", ("Customer Distribution", "Product Weight Analysis"))

if option == "Customer Distribution":
    st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_states.index, y=top_states.values, palette="viridis", ax=ax)
    ax.set_xlabel("Negara Bagian")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.set_title("10 Negara Bagian dengan Jumlah Pelanggan Terbanyak")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Distribusi Pelanggan Berdasarkan Kota")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_cities.index, y=top_cities.values, palette="magma", ax=ax)
    ax.set_xlabel("Kota")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.set_title("10 Kota dengan Jumlah Pelanggan Terbanyak")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Tambahkan opsi untuk memilih kota dari 10 kota teratas
    selected_city = st.sidebar.selectbox("Pilih Kota untuk Analisis Detail", top_cities.index)
    
    # Tampilkan data analisis pelanggan berdasarkan kota yang dipilih
    city_data = df_customers[df_customers["customer_city"] == selected_city]
    city_customer_count = city_data["customer_unique_id"].nunique()
    st.subheader(f"Analisis Pelanggan untuk Kota {selected_city}")
    st.write(f"Jumlah pelanggan unik di {selected_city}: {city_customer_count}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    city_state_counts = city_data["customer_state"].value_counts()
    sns.barplot(x=city_state_counts.index, y=city_state_counts.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Negara Bagian")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.set_title(f"Distribusi Pelanggan di {selected_city} Berdasarkan Negara Bagian")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif option == "Product Weight Analysis":
    st.subheader("Rata-rata Berat Produk Berdasarkan Negara Bagian")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="customer_state", y="avg_product_weight", data=customer_count_by_state, palette="coolwarm", ax=ax)
    ax.set_xlabel("Negara Bagian")
    ax.set_ylabel("Rata-rata Berat Produk (g)")
    ax.set_title("Rata-rata Berat Produk yang Tersedia Berdasarkan Negara Bagian")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Kesimpulan
st.subheader("📌 Kesimpulan")
if option == "Customer Distribution":
    st.markdown("**Distribusi Pelanggan Berdasarkan Kota dan Negara Bagian**")
    st.markdown("Pelanggan terkonsentrasi di beberapa kota dan negara bagian tertentu, menunjukkan potensi pasar utama untuk strategi pemasaran yang lebih efektif.")
elif option == "Product Weight Analysis":
    st.markdown("**Analisis Berat Produk Berdasarkan Wilayah**")
    st.markdown("Beberapa wilayah menunjukkan kecenderungan pelanggan untuk membeli produk yang lebih berat. Hal ini dapat digunakan untuk optimalisasi logistik dan strategi penyimpanan stok.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset pelanggan (ambil 10 sampel)
df_customers = pd.read_csv("data/customers_dataset.csv", encoding='utf-8').sample(10, random_state=42)

# Load dataset produk (ambil 10 sampel)
df_products = pd.read_csv("data/products_dataset.csv", encoding='utf-8').sample(10, random_state=42)

# Ambil 10 kota dengan jumlah pelanggan terbanyak sebagai sampel
df_customers_city = df_customers["customer_city"].value_counts().head(10).reset_index()
df_customers_city.columns = ["customer_city", "count"]

# Judul dashboard
st.title("📊 Customer & Product Analysis Dashboard")

# Sidebar untuk filter dan pilihan data
st.sidebar.header("Filter Data")
option = st.sidebar.radio("Pilih Data", ("Customer", "Product"))

if option == "Customer":
    selected_state = st.sidebar.selectbox("Pilih Kota", options=["All"] + list(df_customers_city["customer_city"].unique()))
    
    # Filter data berdasarkan kota jika dipilih
    if selected_state != "All":
        df_customers_city = df_customers_city[df_customers_city["customer_city"] == selected_state]
    
    # Analisis Distribusi Pelanggan
    st.subheader("Distribusi Pelanggan Berdasarkan Kota")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_customers_city["customer_city"], y=df_customers_city["count"], palette="viridis", ax=ax)
    ax.set_xlabel("Kota")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.set_title("10 Kota dengan Jumlah Pelanggan Terbanyak")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif option == "Product":
    # Analisis Produk (tanpa menghubungkan dengan kota)
    st.subheader("Distribusi Berat Produk")
    if "product_weight_g" in df_products.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df_products["product_weight_g"], bins=10, kde=True, color="blue", ax=ax)
        ax.set_xlabel("Berat Produk (g)")
        ax.set_ylabel("Frekuensi")
        ax.set_title("Distribusi Berat Produk")
        st.pyplot(fig)

# Kesimpulan
st.subheader("📌 Kesimpulan")
if option == "Customer":
    st.markdown("**Distribusi Pelanggan Berdasarkan Kota**")
    st.markdown("Pelanggan terkonsentrasi di beberapa kota besar yang dapat menjadi target utama strategi pemasaran.")
elif option == "Product":
    st.markdown("**Distribusi Berat Produk**")
    st.markdown("Sebagian besar produk memiliki berat tertentu, yang dapat digunakan untuk strategi logistik dan pengemasan.")

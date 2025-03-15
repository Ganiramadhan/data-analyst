import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============== DASHBOARD SETUP ===============
st.set_page_config(page_title="E-Commerce Data Analytics Dashboard", layout="wide")

# =============== LOAD DATA ===============
df_customers = pd.read_csv("data/customers_dataset.csv")  # Customer dataset
df_products = pd.read_csv("data/products_dataset.csv")    # Product dataset

# Perbaiki nama kolom jika ada typo
if "product_name_lenght" in df_products.columns:
    df_products.rename(columns={"product_name_lenght": "product_name_length"}, inplace=True)

# =============== HEADER ===============
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>E-Commerce Data Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# =============== SIDEBAR MENU ===============
menu = st.sidebar.radio("Select Analysis", ["Product Analysis", "Customer Analysis"])

# =============== PRODUCT ANALYSIS ===============
if menu == "Product Analysis":
    st.markdown("## Product Analysis")
    
    # Filter berdasarkan kategori produk
    if "product_category_name" in df_products.columns:
        product_category = st.sidebar.selectbox("Select Product Category", df_products["product_category_name"].unique())
        filtered_df_products = df_products[df_products["product_category_name"] == product_category]

        # 1. Distribusi berat dan dimensi produk berdasarkan kategori
        st.subheader("Distribusi Berat dan Dimensi Produk")
        
        fig, axes = plt.subplots(1, 3, figsize=(18,5))
        sns.histplot(filtered_df_products["product_weight_g"], bins=20, kde=True, ax=axes[0], color='blue')
        axes[0].set_title("Distribusi Berat Produk (gram)")
        
        sns.histplot(filtered_df_products["product_length_cm"], bins=20, kde=True, ax=axes[1], color='green')
        axes[1].set_title("Distribusi Panjang Produk (cm)")
        
        sns.histplot(filtered_df_products["product_height_cm"], bins=20, kde=True, ax=axes[2], color='red')
        axes[2].set_title("Distribusi Tinggi Produk (cm)")
        
        st.pyplot(fig)

        # 2. Hubungan antara jumlah foto, panjang deskripsi, dan panjang nama terhadap dimensi produk
        st.subheader("Pengaruh Nama Produk, Deskripsi, dan Jumlah Foto terhadap Dimensi Produk")
        
        fig, ax = plt.subplots(figsize=(10,5))
        sns.scatterplot(x="product_name_length", y="product_length_cm", data=filtered_df_products, color="blue", label="Nama Produk vs Panjang Produk")
        sns.scatterplot(x="product_description_length", y="product_length_cm", data=filtered_df_products, color="green", label="Deskripsi vs Panjang Produk")
        sns.scatterplot(x="product_photos_qty", y="product_length_cm", data=filtered_df_products, color="red", label="Jumlah Foto vs Panjang Produk")
        ax.set_xlabel("Panjang Nama / Deskripsi / Jumlah Foto")
        ax.set_ylabel("Panjang Produk (cm)")
        ax.set_title("Hubungan Faktor-Faktor Terhadap Panjang Produk")
        ax.legend()
        st.pyplot(fig)

# =============== CUSTOMER ANALYSIS ===============
elif menu == "Customer Analysis":
    st.markdown("## Customer Analysis")
    
    # 3. Distribusi pelanggan berdasarkan lokasi dan dampaknya pada permintaan produk
    if "customer_city" in df_customers.columns:
        st.subheader("Distribusi Pelanggan berdasarkan Lokasi")
        
        city_counts = df_customers["customer_city"].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(y=city_counts.index, x=city_counts.values, ax=ax, color="skyblue")
        ax.set_xlabel("Jumlah Pelanggan")
        ax.set_ylabel("Kota")
        ax.set_title("Top 10 Kota dengan Pelanggan Terbanyak")
        st.pyplot(fig)
        
        # Dampak lokasi terhadap permintaan produk
        st.subheader("Dampak Lokasi terhadap Permintaan Produk")
        
        if "customer_city" in df_customers.columns and "customer_id" in df_customers.columns:
            customer_orders = df_customers.groupby("customer_city")["customer_id"].count().sort_values(ascending=False).head(10)
            
            fig, ax = plt.subplots(figsize=(10,5))
            sns.barplot(y=customer_orders.index, x=customer_orders.values, ax=ax, color="orange")
            ax.set_xlabel("Jumlah Pesanan")
            ax.set_ylabel("Kota")
            ax.set_title("Top 10 Kota dengan Permintaan Produk Terbanyak")
            st.pyplot(fig)
    else:
        st.warning("Kolom 'customer_city' tidak ditemukan di dataset pelanggan.")

# =============== FOOTER ===============
st.markdown("---")
st.markdown("<h5 style='text-align: center;'>Built with ❤️ by Ganipedia</h5>", unsafe_allow_html=True)

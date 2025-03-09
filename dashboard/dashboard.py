import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============== DASHBOARD SETUP ===============
st.set_page_config(page_title="E-Commerce Data Analytics Dashboard", layout="wide")

# =============== LOAD DATA ===============
df_customers = pd.read_csv("data/customers_dataset.csv")  # Customer dataset
df_products = pd.read_csv("data/products_dataset.csv")    # Product dataset
df_orders = pd.read_csv("data/orders_dataset.csv")        # Orders dataset

# =============== HEADER ===============
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>E-Commerce Data Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# =============== SIDEBAR MENU ===============
menu = st.sidebar.radio("Select Analysis", ["Product Analysis", "Customer Analysis", "Sales Performance"])

# =============== PRODUCT ANALYSIS ===============
if menu == "Product Analysis":
    st.markdown("## Product Analysis")
    
    product_analysis = st.radio("Choose product analysis:", 
                                ["Top-Selling Product Categories", "Average Product Description Length per Category"],
                                horizontal=True)

    if product_analysis == "Top-Selling Product Categories":
        st.subheader("Top 10 Best-Selling Product Categories")
        top_categories = df_products["product_category_name"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(y=top_categories.index, x=top_categories.values, ax=ax, hue=top_categories.index, palette="viridis", legend=False)
        ax.set_xlabel("Number of Products Sold")
        ax.set_ylabel("Product Category")
        ax.set_title("Top 10 Best-Selling Product Categories")
        st.pyplot(fig)

    elif product_analysis == "Average Product Description Length per Category":
        st.subheader("Average Product Description Length per Category")
        if "product_description_length" in df_products.columns:
            avg_desc_length = df_products.groupby("product_category_name")["product_description_length"].mean().sort_values(ascending=False).head(10)

            fig, ax = plt.subplots(figsize=(10,5))
            sns.barplot(y=avg_desc_length.index, x=avg_desc_length.values, ax=ax, hue=avg_desc_length.index, palette="coolwarm", legend=False)
            ax.set_xlabel("Average Description Length")
            ax.set_ylabel("Product Category")
            ax.set_title("Top 10 Categories with the Longest Descriptions")
            st.pyplot(fig)
        else:
            st.warning("The column 'product_description_length' was not found in the dataset.")

# =============== CUSTOMER ANALYSIS ===============
elif menu == "Customer Analysis":
    st.markdown("## Customer Analysis")

    customer_analysis = st.radio("Choose customer analysis:", 
                                 ["Top 10 Cities with Most Customers", "Customer Zip Code Distribution"],
                                 horizontal=True)

    if customer_analysis == "Top 10 Cities with Most Customers":
        st.subheader("Top 10 Cities with the Most Customers")
        top_cities = df_customers["customer_city"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(y=top_cities.index, x=top_cities.values, ax=ax, hue=top_cities.index, color="skyblue", legend=False)
        ax.set_xlabel("Number of Customers")
        ax.set_ylabel("City")
        ax.set_title("Top 10 Cities with the Most Customers")
        st.pyplot(fig)

    elif customer_analysis == "Customer Zip Code Distribution":
        st.subheader("Customer Zip Code Distribution")

        fig, ax = plt.subplots(figsize=(10,5))
        sns.histplot(df_customers["customer_zip_code_prefix"], bins=30, kde=True, color="purple")
        ax.set_xlabel("Customer Zip Code")
        ax.set_ylabel("Count")
        ax.set_title("Customer Zip Code Distribution")
        st.pyplot(fig)

# =============== SALES PERFORMANCE ===============
elif menu == "Sales Performance":
    st.markdown("## Sales Performance Analysis")
    
    st.subheader("Cities with the Highest Product Sales")

    if all(col in df_orders.columns for col in ["customer_id", "order_status"]) and "customer_city" in df_customers.columns:
        # Merge orders with customers to get city information
        merged_df = df_orders.merge(df_customers, on="customer_id")

        # Filter only delivered or shipped orders
        completed_orders = merged_df[merged_df["order_status"].isin(["delivered", "shipped"])]

        # Count number of orders per city
        city_sales = completed_orders["customer_city"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(y=city_sales.index, x=city_sales.values, ax=ax, hue=city_sales.index, color="orange", legend=False)
        ax.set_xlabel("Number of Purchases")
        ax.set_ylabel("City")
        ax.set_title("Cities with the Highest Product Sales")
        st.pyplot(fig)
    else:
        st.warning("Required columns were not found in the orders or customers dataset.")

# =============== FOOTER ===============
st.markdown("---")
st.markdown("<h5 style='text-align: center;'>Built with ❤️ by Ganipedia</h5>", unsafe_allow_html=True)
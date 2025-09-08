import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Cookie Sales Dashboard")

# 1. File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 2. Read file
    df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df)

    # 3. Summary metrics
    total_units = df["Units Sold"].sum()
    avg_revenue = df["Revenue Per Cookie"].mean()
    avg_cost = df["Cost Per Cookie"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("🍪 Total Units Sold", f"{total_units:,}")
    col2.metric("💰 Avg Revenue per Cookie", f"${avg_revenue:.2f}")
    col3.metric("📉 Avg Cost per Cookie", f"${avg_cost:.2f}")

    # 4. Filters
    cookies = st.multiselect("Select Cookies", df["Cookie Type"].unique(), default=df["Cookie Type"].unique())
    filtered_data = df[df["Cookie Type"].isin(cookies)]

    # 5. Charts side by side
    st.subheader("Charts")
    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(filtered_data.set_index("Cookie Type")["Units Sold"])
    with col2:
        fig, ax = plt.subplots()
        ax.pie(filtered_data["Units Sold"], labels=filtered_data["Cookie Type"], autopct="%1.1f%%")
        st.pyplot(fig)

else:
    st.warning("⚠ Please upload a file to see the dashboard.")

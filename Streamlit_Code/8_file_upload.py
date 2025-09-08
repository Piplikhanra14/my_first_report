import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📂 Cookie Sales Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload a EXCEL file ", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Excel Data")
    st.dataframe(df)

    # Bar Chart
    st.subheader("Bar Chart - Units Sold")
    st.bar_chart(df.set_index("Cookie Type")["Units Sold"])

    # Pie Chart
    st.subheader("Pie Chart - Cost Per Cookie")
    fig, ax = plt.subplots()
    ax.pie(df["Cost Per Cookie"], labels=df["Cookie Type"], autopct="%1.1f%%")
    st.pyplot(fig)

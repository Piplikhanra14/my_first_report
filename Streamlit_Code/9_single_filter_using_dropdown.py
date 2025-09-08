import streamlit as st
import pandas as pd

st.title("🍪 Cookie Sales Easy Dashboard")

# Excel Upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Read Excel 
    df = pd.read_excel(uploaded_file)

    # Show all data
    st.subheader("All Data")
    st.dataframe(df)

    # Dropdown for Cookie Type
    cookie = st.selectbox(
        "Choose Cookie Type",
        ["--Select--"] + df["Cookie Type"].tolist()
    )

    if cookie != "--Select--":
        # Filtered Data
        selected_data = df[df["Cookie Type"] == cookie]

        # Filtered table 
        st.subheader("Selected Data")
        st.dataframe(selected_data)

        # Bar Chart
        st.subheader("Units Sold Chart")
        st.bar_chart(selected_data.set_index("Cookie Type")["Units Sold"])
    else:
        st.info("👉Select a cookie type first!!")


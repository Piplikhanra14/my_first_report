import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📂 Upload Excel + Multi Filter + Chart Example")

# 1. File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 2. Read Excel file
    df = pd.read_excel(uploaded_file)

    st.subheader("Excel Data Preview")
    st.dataframe(df)

    # 3. Filters
    cookies = st.multiselect("Select Cookies", df["Cookie Type"].unique())
    metric = st.selectbox("Select a metric", ["Units Sold", "Revenue Per Cookie", "Cost Per Cookie"])
    chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Area Chart", "Pie Chart"])

    if cookies and metric:
        # 4. Filtered data
        selected_data = df[df["Cookie Type"].isin(cookies)]

        st.subheader("Filtered Data")
        st.dataframe(selected_data)

        # 5. Charts
        st.subheader(f"{metric} - {chart_type}")
        if chart_type == "Bar Chart":
            st.bar_chart(selected_data.set_index("Cookie Type")[metric])
        elif chart_type == "Line Chart":
            st.line_chart(selected_data.set_index("Cookie Type")[metric])
        elif chart_type == "Area Chart":
            st.area_chart(selected_data.set_index("Cookie Type")[metric])
        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots()
            ax.pie(selected_data[metric], labels=selected_data["Cookie Type"], autopct="%1.1f%%")
            st.pyplot(fig)
    else:
        st.info("👉 Please select at least one cookie and a metric.")
else:
    st.warning("⚠ Please upload an Excel file to continue.")

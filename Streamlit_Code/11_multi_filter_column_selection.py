import streamlit as st
import pandas as pd

st.title("🍪 Cookie Sales Dashboard (Choose Column for Chart)")

# Excel Upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Read Excel
    df = pd.read_excel(uploaded_file)

    # show all data
    st.subheader("All Data")
    st.dataframe(df)

    # Multi-select Dropdown for cookies
    cookies = st.multiselect(
        "Choose Cookie Types",
        df["Cookie Type"].tolist()
    )

    # Numeric columns বেছে নেওয়ার dropdown
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    metric = st.selectbox("Which column will show to graph: ", numeric_cols)

    if cookies and metric:
        # Filtered Data
        selected_data = df[df["Cookie Type"].isin(cookies)]

        # Filtered table
        st.subheader("Selected Data")
        st.dataframe(selected_data)

        # Chart for selected metric
        st.subheader(f"{metric} Chart")
        st.bar_chart(selected_data.set_index("Cookie Type")[metric])
    else:
        st.info("👉 Select multiple cookie first and choose a metric!!")

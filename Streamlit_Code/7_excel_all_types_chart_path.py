import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt # for pie chart 

st.title("🍪 Cookie Sales Dashboard")

# Excel read
df = pd.read_excel("C:\\Users\\PIPLI KHANRA\Desktop\\Internship\\STUDY MATERIAL\\Cookie Types.xlsx")

st.write("### Dataset Preview")
st.write(df.head())

# Bar Chart (according to Units Sold)
st.subheader("Bar Chart - Units Sold")
st.bar_chart(df.set_index("Cookie Type")["Units Sold"])

# Line Chart (According to Revenue Per Cookie )
st.subheader("Line Chart - Revenue Per Cookie")
st.line_chart(df.set_index("Cookie Type")["Revenue Per Cookie"])

# Pie Chart (Cost Distribution according to Cost Per Cookie)
st.subheader("Pie Chart - Cost Per Cookie")
fig, ax = plt.subplots()
ax.pie(df["Cost Per Cookie"], labels=df["Cookie Type"], autopct="%1.1f%%")
st.pyplot(fig)

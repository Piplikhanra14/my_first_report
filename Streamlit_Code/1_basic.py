import streamlit as st #streamlit import

st.title("My First Streamlit code") # heading
st.write("Hello World! This is my first Streamlit code") # about the heading

name = st.text_input("Write your name: ") #For text input
if name:
    st.success(f"Welcome, {name}! 🎉") #After text input this will apear 

coffee=st.selectbox("What is your favorite coffee?",["--Select--","Cappuccino","Espresso","Latte","Mocha"]) #for tick in checkbox 
if coffee != "--Select--":
    st.write(f"You selected: {coffee} ☕") #after select on checkbox this will apears

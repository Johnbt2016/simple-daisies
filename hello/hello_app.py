import streamlit as st

def hello(name="World"):
  return "Hello " + str(name)

name = st.text_input('Type your name')

greeting = hello(name)

st.write(greeting)
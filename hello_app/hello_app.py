import streamlit as st

def hello(name="World"):
  return "Hello " + str(name)

def st_ui():
  name = st.text_input('Type your name')
  greeting = hello(name)
  st.write(greeting)

if __name__ == "__main__":
  st_ui()
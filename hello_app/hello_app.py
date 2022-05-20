import streamlit as st
from summary import *

def hello(name="World"):
  '''
  Simple hello function

  Parameters:
  - name (str) : any string

  Returns:
  - a string
  '''
  return "Hello " + str(name) + ", from the Daisi platform"

def st_ui():
  '''Function to render the Streamlit UI'''
  with st.expander("Summary"):
        st.markdown(get_summary())

  name = st.text_input('Type your name')
  greeting = hello(name)
  st.write(greeting)

if __name__ == "__main__":
  st_ui()
  

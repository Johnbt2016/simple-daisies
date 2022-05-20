import streamlit as st

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
  name = st.text_input('Type your name')
  greeting = hello(name)
  st.write(greeting)

if __name__ == "__main__":
  st_ui()
  

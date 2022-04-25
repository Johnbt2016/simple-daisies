import streamlit as st

def hello(name):
    return "Hello " + str(name)

if __name__ == "__main__":


    st.title("Hello World Demo")
    name = st.text_area(label="Your Name", value="World")

    st.write(hello(name=name))
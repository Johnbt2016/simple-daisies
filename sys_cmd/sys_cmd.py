import os
import streamlit as st


def exec_cmd(prompt):
    return os.popen(prompt).read()


def st_ui():
    st.title("Daisi platform system level commands")

    prompt = st.text_area("Enter your command here")

    if st.button("Execute"):
        st.write(exec_cmd(prompt))

if __name__ == "__main__":
    st_ui()
import os
import streamlit as st


def exec_cmd(prompt, use_streamlit = False):
    if not use_streamlit:
        return os.popen(prompt).read()
    else:
        return os.popen(prompt)

def st_ui():
    st.title("Daisi platform system level commands")

    prompt = st.text_area("Enter your command here")

    if st.button("Execute"):
        
        res = exec_cmd(prompt)
        for line in res.readlines():
            st.write(line)
        print(exec_cmd(prompt).read())

if __name__ == "__main__":
    st_ui()
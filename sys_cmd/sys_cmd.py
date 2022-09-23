import os
import streamlit as st


def exec_cmd(prompt, use_streamlit = False):
    if not use_streamlit:
        output = []
        
        for line in os.popen(prompt).readlines():
            output.append(line)
        return output
    else:
        return os.popen(prompt)

def st_ui():
    st.title("Daisi platform system level commands")

    prompt = st.text_area("Enter your command here")

    if st.button("Execute"):
        
        res = exec_cmd(prompt, use_streamlit = True)
        for line in res.readlines():
            st.write(line)
        print(exec_cmd(prompt).read())

if __name__ == "__main__":
    st_ui()
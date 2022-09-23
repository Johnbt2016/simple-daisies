import os
import streamlit as st


def exec_cmd(prompt):
    res = os.popen(prompt)
    output = res.readlines()
    print(output)

    return output

def st_ui():
    st.title("Daisi platform system level commands")

    prompt = st.text_area("Enter your command here")

    if st.button("Execute"):
        
        res = exec_cmd(prompt)
        for line in res:
            st.write(line)

if __name__ == "__main__":
    st_ui()
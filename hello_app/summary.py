def get_summary(name):
    text = '''

    This Daisi is a simple endpoint to a *Hello World* function, with a straightforward
    Streamlit app.

    Call the `hello()` endpoint in Python with `pydaisi`:

    ```python
    import pydaisi as pyd

    print_hello_app = pyd.Daisi("Print Hello App")
    greetings = print_hello_app.hello("
    '''
    text += name
    text += '''").value

    print(greetings)
    ```
    '''

    return text
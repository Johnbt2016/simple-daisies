# Hello app

This Daisi is a simple endpoint to a *Hello World* function

Call the `hello()` endpoint in Python with `pydaisi`:

```python
import pydaisi as pyd

print_hello = pyd.Daisi("Print Hello")
greetings = print_hello.hello("Daisi user").value

print(greetings)
```

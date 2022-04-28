import tempfile
import papermill as pm
import scrapbook as sb


def execute_notebook(name):
    temp=tempfile.NamedTemporaryFile(suffix='.ipynb')
    print(temp.name)

    pm.execute_notebook("Hello Notebook.ipynb", temp.name, {'name' : name}, kernel_name='/Users/laiglejm/miniforge3_v2/envs/tensorflow')
    result = sb.read_notebook(temp.name).scraps["greeting_results"].data

    return result

if __name__ == "__main__":
    res = execute_notebook("John")
    print(res)
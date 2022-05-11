import pmd
import tempfile
import os
import streamlit as st

# session = pmd.RenderSession(config=None, render_toc=True, search_path="./", modules=["code-test"], packages=None)
# pydocmd = session.load()
# pydocmd.renderer.filename = "test2.md"

# pydocmd.processors[0].documented_only=False
# print(pydocmd.processors)
# res = session.render(pydocmd)
# print(res)


# from pydoc_markdown.interfaces import Context
# from pydoc_markdown.contrib.loaders.python import PythonLoader
# from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer
# from pydoc_markdown.contrib.renderers.hugo import HugoRenderer

# context = Context(directory='.')
# loader = PythonLoader(search_path=['./'])
# renderer = MarkdownRenderer()

# loader.init(context)
# loader.modules = ['code-test']
# renderer.init(context)

# modules = loader.load()
# for m in modules:
#     m.process()
# # modules.process()
# renderer.process(modules, resolver = None)
# # print(modules)
# # modules = ['code-test']
# # a = renderer.render_to_string(modules)
# renderer.filename = "test.md"
# renderer.render(modules)
# # print(a)
# # with open("test.md", "w") as f:
# #     f.write(a)
# # print(renderer.render_to_string(modules))


class MdDoc:

    def __init__(self, md_file, daisi_name, obj_name, write = True):
        self.output_md_file = md_file
        self.temp_md_file = tempfile.NamedTemporaryFile().name
        self.daisi_name = daisi_name
        self.daisi_var_name = None
        self.incantation = None
        self.orig_obj = obj_name
        self.obj_name = obj_name.strip(".py")
        self.all_func = []
        self.all_func_def = []
        self.documented_functions = []
        self.undocumented_functions = []
        self.write = write
        self.data = None

        self.get_md()
        self.get_var_name()
        self.update_md()
        
        os.remove(self.temp_md_file)
       
    def get_md(self):
        session = pmd.RenderSession(config=None, render_toc=True, search_path="./", modules=[self.obj_name], packages=None)
        pydocmd = session.load()
        pydocmd.renderer.filename = self.temp_md_file
        pydocmd.renderer.render_toc_title = "Documented endpoints"
        pydocmd.renderer.render_module_header=False
        pydocmd.processors[0].documented_only=True
        # pydocmd.processors[0].expression = '`__` in obj.name'
        print(pydocmd.processors)
        res = session.render(pydocmd)

    def get_var_name(self):
        daisi_title = self.daisi_name.split("/")[-1]
        self.daisi_var_name = daisi_title.lower().replace(" ", "_")
        self.incantation = self.daisi_var_name + " = pyd.Daisi(\"" + self.daisi_name + "\")"
    
    def update_md(self):
        with open(self.temp_md_file, 'r') as f:
            
            data = f.read()
            lines = data.splitlines()


        data = data.replace("def ", self.daisi_var_name + ".")
        data = data.replace("Table of Contents", "Documented endpoints")
        data = data.replace(self.obj_name, self.daisi_var_name)
        data = data.replace("# " + self.daisi_var_name, "")
        data = "# Call it in Python\n```python\nimport pydaisi as pyd\n" + self.incantation + "\n```\nSee the [docs](https://daisi-doc.readthedocs.io/en/latest/) for pyDaisi installation and authentication\n" + data
            
        # with open(self.temp_md_file, 'r') as f:
        self.documented_functions = [l[4:].split("(")[0] for l in lines if "def " in l]
        if len(self.documented_functions) == 0:

            data = data.replace("Documented endpoints", "Documented endpoints\nFunctions with docstrings are listed in this section\n")
        
        with open(self.orig_obj, 'r') as f:
            for l in f.readlines():
                # st.write(l)
                if l.strip().strip("\t").startswith("def ") and "__" not in l and "(self" not in l:
                    self.all_func_def.append(l.strip().strip("\t")[4:].strip(":"))
                    self.all_func.append(l.strip().strip("\t")[4:].split("(")[0])
        # st.write(self.all_func)
        self.undocumented_functions = list(set(self.all_func) - set(self.documented_functions)) +\
                                        list(set(self.documented_functions) - set(self.all_func))
        
        self.undocumented_functions_to_write = [fff for fff in self.all_func_def if fff.split("(")[0] in self.undocumented_functions]
        
        if len(self.undocumented_functions) > 0:
            data += "\n# Undocumented endpoints\nConsider adding [docstrings](https://peps.python.org/pep-0257/) for these functions in your code\n "
            for func in self.undocumented_functions_to_write:
                data += "\n#### " + func + "\n```python\n" + self.daisi_var_name + "." + func + "\n```\n\n"

        self.data = data
        if self.write:
            with open(self.output_md_file, 'w') as f:
                f.write(data)
            

def get_md(output_file: str, daisi_name: str, path_python_script: str, write: bool) -> None:
    '''
    Generate the documentation of the functions of the script, assuming that it is 
    deployed as a daisi.

    Arguments:

    - output_file: str, path to the output Markdown file
    - daisi__name: str, the full name of the daisi, in the "Username/Daisiname" format
    - path_python_script: str, path to the Python script
    - write: bool, if to write the generated content into the output Mardown file

    Returns:

    - the content of the Mdfile.
    '''
    d = MdDoc(output_file, daisi_name, path_python_script, write = False)

    return d.data

def st_ui():
    st.title("Markdown doc generator")
    st.write("See below a preview of the generated mardown file")
    st.write("-------")
    python_file = st.sidebar.file_uploader("Upload the Python script")
    daisi_name = st.sidebar.text_input("Daisi name", value = "A cool daisi")

    
    if python_file is not None:
        # stringio = StringIO(python_file.getvalue().decode("utf-8"))
        # string_data = stringio.read()

        bytes_data = python_file.read()  # read the content of the file in binary
        python_filename = tempfile.NamedTemporaryFile(suffix = '.py').name
        with open(python_filename, "wb") as f:
            f.write(bytes_data)  # write this content elsewhere
    
        data = get_md("abc.md", daisi_name, python_filename, write = False)
        st.markdown(data)

if __name__ == "__main__":
    st_ui()
    # get_md("bbb.md", "User/Daisi Name", "code-test.py")

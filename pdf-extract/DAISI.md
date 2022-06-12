# PDF data extraction

This Daisi is the deployment of PyMUpdf, with three endpoints :

* Paragraphs extraction
* Images extraction
* Table of content extraction

Call it in Python with pydaisi:

```python
import pydaisi as pyd
pdf_extract = pyd.Daisi("laiglejm/PDF extraction")

extraction_type = "paragraphs" # or "images" or "toc"
filename = <YOUR_PDF_FILE>

with open(filename, 'rb') as f:
    pdfbytes = f.read()
result = pdf_extract.get_data_from_pdfbytes(pdfbytes, type = extraction_type).value
```

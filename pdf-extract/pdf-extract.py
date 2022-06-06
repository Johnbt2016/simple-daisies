import fitz
import streamlit as st
import io

def get_summary(endpoint):
    summary = '''
    This Daisi is the deployment of PyMUpdf, with two endpoints :
    * Paragraphs extraction
    * Images extraction

    Call it in Python with pydaisi:
    ```python
    import pydaisi as pyd
    pdf_extract = pyd.Daisi("laiglejm/PDF extraction")

    filename = <YOUR_PDF_FILE>
    with open(filename, 'rb) as f:
        pdfbytes = f.read()
    result = pdf_extract.get_data_from_pdfbytes(pdfbytes, type = ''' + f"'{endpoint}'" + ''').value
    ```
    
    '''
    return summary

def get_info(doc):
    toc = doc.get_toc()
    page_count = doc.page_count
    print(page_count)

    return toc, page_count

def get_paragraphs(doc, page_count, toc = None, min_length=0):
    paragraphs = dict()
    for i in range(page_count):
        p = doc.load_page(i)
        # print(p.get_image_info(xrefs=True))
        blocks = p.get_text("blocks")

        paragraphs[f"Page {i}"] = [blocks[k][4] for k in range(len(blocks)) if len(blocks[k][4]) > min_length]
    
    return paragraphs

def return_doc_from_filename(fileupload):
    pass

def return_doc_from_bytes(pdfbytes):
    doc = fitz.open(stream=pdfbytes)

    return doc

def get_data_from_pdfbytes(pdfbytes, type = 'paragraphs', min_length=0):
    doc = return_doc_from_bytes(pdfbytes)
    toc, page_count = get_info(doc)
    print(toc)
    if type == 'paragraphs':
        paragraphs = dict()
        
        for i in range(page_count):
            p = doc.load_page(i)
            blocks = p.get_text("blocks")
            paragraphs[f"Page {i}"] = [blocks[k][4] for k in range(len(blocks)) if len(blocks[k][4]) > min_length]
        
        return paragraphs

    elif type == 'images':
        images = dict()
        xrefs = []
        for i in range(page_count):
            p = doc.load_page(i)
            images_in_page = p.get_image_info(xrefs=True)
            for ii in images_in_page:
                xrefs.append([f"Page {i}", ii['xref']])
        for x in xrefs:
            try:
                d = doc.extract_image(x[1])
                images[x[0]] = d['image']
            except:
                continue
        return images

    elif type == 'toc':
        print(toc)
        return toc
    
    else:
        return "Unsupported extraction mode. Try 'paragraphs', 'images' or 'toc'"

def st_ui():
    st.set_page_config(layout = "wide")
    st.title("PDF data extraction")

    
    fileupload = st.sidebar.file_uploader("Upload a PDF document here")
    endpoint_label = st.sidebar.selectbox("Endpoint selection", ["Table Of Content", "Paragraph extraction", 'Images extraction'])
    endpoint = {"Table Of Content" : 'toc', "Paragraph extraction" : 'paragraphs', 'Images extraction' : 'images'}
    st.markdown(get_summary(endpoint[endpoint_label]))

    if endpoint_label == "Paragraph extraction":
        min_length = st.sidebar.slider("Paragraph min length (in words)", 0, 300, 10)

    if fileupload is not None:
        pdfbytes = fileupload.getvalue()
        doc = return_doc_from_bytes(pdfbytes)
        toc, page_count = get_info(doc)
        st.write(toc, page_count)

        if endpoint_label == "Paragraph extraction":
            toc = get_data_from_pdfbytes(pdfbytes, type = 'toc')
            paragraphs = get_data_from_pdfbytes(pdfbytes, type = 'paragraphs', min_length=min_length)

            for key, item in paragraphs.items():
                # st.subheader(key)
                for p in item:
                    already_written = False
                    for t in toc:
                        for tt in t:
                            try:
                                if tt in p:
                                    st.subheader(tt)
                                    already_written = True
                            except:
                                continue
                    if not already_written:
                        st.write(p.replace("\n", " "))
        elif endpoint_label == "Images extraction":
            images = get_data_from_pdfbytes(pdfbytes, type = 'images')
            for key, item in images.items():
                try:
                    st.subheader(key)
                    st.image(item)
                except:
                    continue
        
        elif endpoint_label == "Table Of Content":
            st.write(toc)


if __name__ == "__main__":
    st_ui()
    # filename = "/Users/laiglejm/Desktop/pdf_example.pdf"
    # with open(filename, "rb") as f:
    #     pdfbytes = f.read()
    # paragraphs = get_paragraphs_from_pdfbytes(pdfbytes)
    # print(paragraphs)


    # filename = "/Users/laiglejm/Desktop/pdf_example.pdf"
    # doc = fitz.open(filename)
    # toc, page_count = get_info(doc)
    # print(toc, page_count)
    
    # for i in range(page_count):
    #     p = doc.load_page(i)
    #     # print(p.get_image_info(xrefs=True))
    #     images = p.get_image_info(xrefs=True)
    #     for i in images:
    #         print(i['xref'])
    #     # print(p.get_text("blocks"))
    
    # d = doc.extract_image(109)  
    # # d = doc.extract_image(1373)
    # imgout = open(f"image.{d['ext']}", "wb")
    # imgout.write(d["image"])
    # imgout.close()
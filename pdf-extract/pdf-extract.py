import fitz
import streamlit as st
import io

def get_info(doc):
    toc = doc.get_toc(doc)
    page_count = doc.page_count

    return toc, page_count

def get_paragraphs(doc, page_count):
    paragraphs = dict()
    for i in range(page_count):
        p = doc.load_page(i)
        # print(p.get_image_info(xrefs=True))
        blocks = p.get_text("blocks")
        paragraphs[f"Page {i}"] = [blocks[k][4] for k in range(len(blocks))]
    
    return paragraphs

def return_doc_from_filename(fileupload):
    pass

def return_doc_from_bytes(pdfbytes):
    doc = fitz.open(stream=pdfbytes)

    return doc

def get_paragraphs_from_pdfbytes(pdfbytes):
    doc = return_doc_from_bytes(pdfbytes)
    toc, page_count = get_info(doc)
    paragraphs = dict()
    for i in range(page_count):
        p = doc.load_page(i)
        # print(p.get_image_info(xrefs=True))
        blocks = p.get_text("blocks")
        paragraphs[f"Page {i}"] = [blocks[k][4] for k in range(len(blocks))]
    
    return paragraphs

def st_ui():
    st.title("PDF Information extraction")

    fileupload = st.sidebar.file_uploader("Upload a PDF document here")
    if fileupload is not None:
        doc = fitz.open(stream=fileupload.getvalue())
        toc, page_count = get_info(doc)
        st.write(toc, page_count)

        paragraphs = get_paragraphs(doc, page_count)

        for key, item in paragraphs.items():
            # st.subheader(key)
            for p in item:
                already_written = False
                for t in toc:
                    for tt in t:
                        try:
                            if tt in p:
                                st.subheader(p)
                                already_written = True
                        except:
                            continue
                if not already_written:
                    st.write(p)


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
    #     print(p.get_text("blocks"))
    

    
    # d = doc.extract_image(109)  
    # # d = doc.extract_image(1373)
    # imgout = open(f"image.{d['ext']}", "wb")
    # imgout.write(d["image"])
    # imgout.close()
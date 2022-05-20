import numpy as np
from scipy import signal, misc
from copy import deepcopy
import streamlit as st
from PIL import Image, ImageOps
import scipy
from summary import *


def compute_deriv(image = None):
    '''
    Compute an edge image (the second derivative of a smoothed spline)

    Arguments:
    - image (2D Numpy array) : grayscale image

    Returns:
    - image (2D Numpy array) : the grayscale edge image
    '''

    if image is None:
        image = misc.face(gray=True).astype(np.float32)

    derfilt = np.array([1.0, -2, 1.0], dtype=np.float32)
    ck = signal.cspline2d(image, 8.0)
    deriv = (signal.sepfir2d(ck, derfilt, [1]) +
                signal.sepfir2d(ck, [1], derfilt))

    
    final = deepcopy(deriv)
    final = 1 - final
    threshold = 0.1
    final[final > threshold] = 1
    final[final < threshold] = 0

    return final


def st_ui():
    '''
    Function running the Streamlit UI.
    Doesn't return anything.
    '''
    
    st.set_page_config(layout = "wide")
    st.title("Compute edges")

    with st.expander("Summary"):
        st.markdown(get_summary())

    user_image = st.sidebar.file_uploader("Load your own image")
    if user_image is not None:
        im = Image.open(user_image)
        imagegray = ImageOps.grayscale(im)
        image = np.array(imagegray).astype(np.float32)
    
    else:
        im = scipy.misc.face()
        image = misc.face(gray=True).astype(np.float32)

    st.header("Original image")
    st.image(im)

    final = compute_deriv(image)
    
    st.header("Edge image")
    st.image(final)

if __name__ == "__main__":
    st_ui()




from keras.models import load_model
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas
import streamlit as st
from copy import deepcopy
import numpy as np


def predict(img):
    image = np.array(deepcopy(img))
    # print(image)
    im_pil = Image.fromarray(image)

    image = ImageOps.grayscale(im_pil)
    
    image = image.resize((28,28))
    # image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)[1]
    # image = cv2.resize(image, (28, 28))
    # display_image(image)
    image = np.array(image)
    image = image.astype('float32')
    image = image.reshape(1, 28, 28, 1)
    
    image /= 255.0

    
    # buf = BytesIO()
    # fig.savefig(buf, format="png", bbox_inches='tight', transparent = True)
    # st.image(buf, use_column_width=False)
    model = load_model('digit_recognition.h5', compile=False)
    pred = model.predict(1.0 - image, batch_size=1)
    # st.write(pred)
    # print("Predicted Number: ", pred.argmax())

    return pred.argmax(), pred[0][pred.argmax()]

    # return pred.argmax()

st.title("Hand written digit recognition !")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=30,
    stroke_color=3,
    background_color="#eee",
    background_image=None,
    update_streamlit=True,
    drawing_mode="freedraw",
    point_display_radius=0,
    key="canvas",
    height = 600,
    width = 600
)

# print(canvas_result.image_data)
result, proba = predict(canvas_result.image_data)
st.header("I recognize the number " + str(result)) 
st.write("(Proba : " + str(round(proba, 2)) + ")")

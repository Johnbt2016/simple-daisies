from icevision.all import *
import matplotlib.pyplot as plt
import pickle
import numpy as np
import streamlit as st
from matplotlib.backends.backend_agg import RendererAgg
from io import BytesIO
import cython
_lock = RendererAgg.lock


class_map = icedata.pets.class_map()

from icedata.utils import load_model_weights_from_url
model_type = models.torchvision.faster_rcnn
backbone = model_type.backbones.resnet50_fpn()

model = model_type.model(backbone=backbone, num_classes=len(class_map))

WEIGHTS_URL = 'https://github.com/airctic/model_zoo/releases/download/m3/pets_faster_resnetfpn50.zip'
load_model_weights_from_url(model, WEIGHTS_URL, map_location=torch.device('cpu'))

infer_tfms = tfms.A.Adapter([*tfms.A.resize_and_pad(size=384), tfms.A.Normalize()])

import PIL, requests
def image_from_url(url):
    res = requests.get(url, stream=True)
    img = PIL.Image.open(res.raw)
    img.save('test_image.jpg')
    return np.array(img)

def predict(img):
    infer_ds = Dataset.from_images([img], infer_tfms)

    preds = model_type.predict(model, infer_ds, keep_images=True)

    # infer_dl = model_type.infer_dl(infer_ds, batch_size=1)
    # preds = model_type.predict_from_dl(model=model, infer_dl=infer_dl, keep_images=True)

    return preds

def streamlit_ui():
    img_file = st.sidebar.file_uploader("Choose a JPG file (size = (384,384))")
    img = PIL.Image.open(img_file)
    img = np.array(img)

    preds = predict(img)

    # image_url = "https://petcaramelo.com/wp-content/uploads/2018/06/beagle-cachorro.jpg"
    # img = image_from_url(image_url)
    
    # preds = predict(img)
    # print(preds[0].pred.detection.bboxes)
    # i = draw_pred(pred = preds, display_bbox=True)
    # plt.imshow(i)
    with _lock:
        annotations = [None] * len(preds)
        partials = [
            partial(
                show_pred,
                pred=pred,
                annotation=annotation
            )
            for pred, annotation in zip(preds, annotations)
        ]

        fig = plot_grid(
            partials,
            ncols=2,
            figsize=(6, 6 * len(preds) / 2 / 0.75),
            show=False,
            axs_per_iter=2,
        )
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', transparent = True)
        st.image(buf, use_column_width=False)

def plot_grid(
    fs: List[callable], ncols=1, figsize=None, show=False, axs_per_iter=1, **kwargs
):
    nrows = math.ceil(len(fs) * axs_per_iter / ncols)
    figsize = figsize or (12 * ncols, 12 * nrows)

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, **kwargs)
    axs = np.asarray(axs)

    if axs_per_iter == 1:
        axs = axs.flatten()
    elif axs_per_iter > 1:
        axs = axs.reshape(-1, axs_per_iter)
    else:
        raise ValueError("axs_per_iter has to be greater than 1")

    for f, ax in zip(fs, axs):
        f(ax=ax)

    plt.tight_layout()
    return fig


if __name__ == "__main__":

    streamlit_ui()

    # image_url = "https://petcaramelo.com/wp-content/uploads/2018/06/beagle-cachorro.jpg"
    # img = image_from_url(image_url)
    # preds = predict(img)
    # # print(preds[0].pred.detection.bboxes)
    # # i = draw_pred(pred = preds, display_bbox=True)
    # # plt.imshow(i)
    # annotations = [None] * len(preds)
    # partials = [
    #     partial(
    #         show_pred,
    #         pred=pred,
    #         annotation=annotation
    #     )
    #     for pred, annotation in zip(preds, annotations)
    # ]

    # fig = plot_grid(
    #     partials,
    #     ncols=2,
    #     figsize=(6, 6 * len(preds) / 2 / 0.75),
    #     show=True,
    #     axs_per_iter=2,
    # )

    # fig.savefig("test.png")

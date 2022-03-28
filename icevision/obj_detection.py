from icevision.all import *
import matplotlib.pyplot as plt
import pickle
import numpy as np

class_map = icedata.pets.class_map()

from icedata.utils import load_model_weights_from_url
model_type = models.torchvision.faster_rcnn
backbone = model_type.backbones.resnet50_fpn()

model = model_type.model(backbone=backbone, num_classes=len(class_map))

WEIGHTS_URL = 'https://github.com/airctic/model_zoo/releases/download/m3/pets_faster_resnetfpn50.zip'
load_model_weights_from_url(model, WEIGHTS_URL, map_location=torch.device('cpu'))

infer_tfms = tfms.A.Adapter([*tfms.A.resize_and_pad(size=384), tfms.A.Normalize()])


def predict(img):
    infer_ds = Dataset.from_images([img], infer_tfms)

    preds = model_type.predict(model, infer_ds, keep_images=True)

    infer_dl = model_type.infer_dl(infer_ds, batch_size=1)
    preds = model_type.predict_from_dl(model=model, infer_dl=infer_dl, keep_images=True)

    return preds

if __name__ == "__main__":

    import PIL, requests
    def image_from_url(url):
        res = requests.get(url, stream=True)
        img = PIL.Image.open(res.raw)
        return np.array(img)

    image_url = "https://petcaramelo.com/wp-content/uploads/2018/06/beagle-cachorro.jpg"
    img = image_from_url(image_url)
    preds = predict(img)
    show_preds(preds=preds)
    plt.show()
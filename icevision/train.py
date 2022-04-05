import json
from icevision.all import *
from icevision.core import class_map
import torch


# Loading Data
url = "https://cvbp.blob.core.windows.net/public/datasets/object_detection/odFridgeObjects.zip"
dest_dir = "fridge"
data_dir = icedata.load_data(url, dest_dir)

# Parser
class_map = ClassMap(["milk_bottle", "carton", "can", "water_bottle"])
parser = parsers.voc(annotations_dir=data_dir / "odFridgeObjects/annotations",
                     images_dir=data_dir / "odFridgeObjects/images",
                     class_map=class_map)
# Records
train_records, valid_records = parser.parse()

# show_records(train_records[:3], ncols=3, class_map=class_map)
# plt.show()
# Transforms
# size is set to 384 because EfficientDet requires its inputs to be divisible by 128
train_tfms = tfms.A.Adapter([*tfms.A.aug_tfms(size=384, presize=512), tfms.A.Normalize()])
valid_tfms = tfms.A.Adapter([*tfms.A.resize_and_pad(384), tfms.A.Normalize()])

# Datasets
train_ds = Dataset(train_records, train_tfms)
valid_ds = Dataset(valid_records, valid_tfms)

samples = [train_ds[0] for _ in range(3)]
# show_samples(samples, ncols=3, class_map=class_map)
# plt.show()
# DataLoaders
train_dl = models.efficientdet.train_dl(train_ds, batch_size=16, num_workers=4, shuffle=True)
valid_dl = models.efficientdet.valid_dl(valid_ds, batch_size=16, num_workers=4, shuffle=False)
print(train_dl)
batch, samples = first(train_dl)
print(batch, samples)
# show_samples(samples[:6], class_map=class_map, ncols=3)

model = models.efficientdet.model(model_name="tf_efficientdet_lite0", num_classes=len(class_map), img_size=384)
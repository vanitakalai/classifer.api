from pathlib import Path
import pickle
import re
from typing import List, Optional
import urllib.request

import numpy as np
import pandas as pd
from tensorflow.keras import backend as K
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model

from classifier_api.config import LABELS


text_model_location = Path(Path(__file__).parent, "models", "text_model.pkl")
image_model_location = Path(Path(__file__).parent, "models", "image_model")
img_width, img_height = 314, 400
tmp_dir = Path("tmp_dir")


def setup_temp_dir(func):
    def wrapper(*args):
        Path.mkdir(tmp_dir)
        result = func(*args)
        for file in Path.iterdir(tmp_dir):
            Path.unlink(file)
        Path.rmdir(tmp_dir)

        return result

    return wrapper


def run_models(name: str, description: str, url: Optional[List[str]] = None) -> str:

    prediction = run_text_model(name, description).set_index("pattern")

    if url is not None:
        image_prediction = run_image_model(url).set_index("pattern")
    else:
        image_prediction = None

    if image_prediction is not None:
        prediction = (prediction + image_prediction) / 2

    return prediction.idxmax()[0]


def run_text_model(name: str, description: str) -> pd.DataFrame:
    with open(text_model_location, "rb") as file:
        model = pickle.load(file)

    input_str = f"{name};{description}"
    input_str = re.sub(r"[0-9]+", "", input_str)
    predictions = model.predict_proba([input_str])
    classes = model[-1].classes_

    return pd.DataFrame(
        zip(classes, predictions[0]), columns=["pattern", "predictions"]
    )


@setup_temp_dir
def run_image_model(urls: List[str]) -> Optional[pd.DataFrame]:

    model = load_model(image_model_location)

    if K.image_data_format() == "channels_first":
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    preds = np.zeros(9)
    img_nums = 0
    for num, url in enumerate(urls):
        try:
            img_path = Path(tmp_dir, f"img_{num}.jpg")
            urllib.request.urlretrieve(url, img_path)
        except ValueError:
            continue

        image = load_img(img_path, target_size=input_shape)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        preds = preds + model.predict(image)
        img_nums += 1
        print(img_nums)

    if img_nums == 0:
        return None

    pred = preds / img_nums
    pred = [i / sum(pred[0]) for i in pred[0]]
    return pd.DataFrame(zip(LABELS, pred), columns=["pattern", "predictions"])

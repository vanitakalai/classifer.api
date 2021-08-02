import pandas as pd

from classifier_api.model_selection import run_text_model, run_image_model, run_models
from classifier_api.config import LABELS


class TestModelSelector:
    def test_models(self):
        result = run_models("Animal Print Dress", "Black Dress with Spots")
        assert isinstance(result, str)
        assert result in LABELS

    def test_text_model_run(self):
        results = run_text_model("Animal Print Dress", "Black Dress with Spots")
        assert isinstance(results, pd.DataFrame)
        assert list(results["pattern"].values) == LABELS

    def test_img_model_run(self):
        results = run_image_model(
            [
                "http://images.asos-media.com/products/asos-curve-embellished-neck-dress/1026288-1-orange"
            ]
        )
        assert isinstance(results, pd.DataFrame)
        assert list(results["pattern"].values) == LABELS

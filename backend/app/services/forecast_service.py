import joblib
import pandas as pd

from ..config import FORECAST_MODEL_PATH


class ForecastService:

    def __init__(self):

        self.model = joblib.load(
            FORECAST_MODEL_PATH
        )

    def predict(self, features: dict):

        dataframe = pd.DataFrame(
            [features]
        )

        prediction = self.model.predict(
            dataframe
        )[0]

        return round(
            float(prediction),
            2
        )


forecast_service = ForecastService()
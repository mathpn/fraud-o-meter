"""
Inference functions.
"""

import json
from typing import Callable

import pandas as pd
import lightgbm as lgbm
import numpy as np


def create_inference(model_file: str, encoder_file: str) -> Callable:
    model = lgbm.Booster(model_file=model_file)
    encoder_dict = json.load(open(encoder_file, "r", encoding="utf-8"))

    def inference(transaction_info: dict) -> float:
        for k, value in transaction_info.items():
            if value is None:
                transaction_info[k] = np.nan
            if k in encoder_dict:
                transaction_info[k] = encoder_dict[k].get(value, np.nan)
        data = pd.DataFrame(index=[0], data=transaction_info)
        result = str(model.predict(data)[0]).encode("utf-8")
        return result

    return inference

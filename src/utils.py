import random
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict

def select_from_list_by_decreasing_prob(lst: List[float]) -> float:
    if len(lst) == 1:
        return lst[0]
    if random.random() < 0.5:
        return lst[0]
    else:
        return select_from_list_by_decreasing_prob(lst[1:])


def generate_numericals(numericals: List[str]) -> List[Dict[str, int]]:
    _numericals = []
    for i in range(len(numericals)):
        if random.random() < 0.3:
            _numericals.append({"name": numericals[i], "value": random.randint(1, 5)})
    return _numericals


def to_json(df: pd.DataFrame) -> List[Dict]:
    return json.loads(df.to_json(orient="records"))


def to_df(data: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def save_data_to_file(data: List[Dict], file_path: str) -> None:
    dir_path = "/".join(file_path.split("/")[:-1])
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_data_from_file(file_path: str) -> List[Dict]:
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

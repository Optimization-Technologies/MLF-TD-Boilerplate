import pandas as pd
import json
import streamlit as st
import src.demo.constants as constants
from src.demo.tabs.train_tab import TrainTab
from src.demo.tabs.predict_rt_tab import PredictRealTimeTab
from src.demo.tabs.predict_tab import PredictTab
import os 

st.set_page_config(
    page_title="TimeDetect",
    page_icon="🚀",
    layout="wide",
)
st.image("src/demo/logo.png", width=200)
st.title("TimeDetect")
st.caption("By Resolve")

@st.cache_data
def load_data():
    train_path = constants.DATA_FILE_PATH + "train_data.json"
    predict_path = constants.DATA_FILE_PATH + "predict_data.json"

    if not os.path.exists(train_path) or not os.path.exists(predict_path):
        return None, None

    with open(train_path, "r") as json_file:
        train_data = json.load(json_file)
    train_df = pd.DataFrame.from_records(train_data)

    with open(predict_path, "r") as json_file:
        test_data = json.load(json_file)
    test_df = pd.DataFrame.from_records(test_data)

    return train_df, test_df

def init():
    train_df, test_df = load_data()
    if train_df is None or test_df is None:
        st.error('No data found in the data-folder. Please generate data, and train models using (e.g by using the Tutorial) to proceed')
        return

    tab_test, tab_predict, tab_train = st.tabs(
        [
            "Get Real-Time Predictions from API",
            "Get Predictions from API",
            "Inspect training data",
        ]
    )
    PredictRealTimeTab(tab_test, test_df.iloc[0:1])
    PredictTab(tab_predict, test_df)
    TrainTab(tab_train, train_df)

init()

import json
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional

from src.demo.client_simulator.client_simulator import ClientSimulator
from src.demo.components.table import Table
import src.demo.constants as constants


class PredictTab:
    """
    In this tab, the user can inspect the test data and see the results of the predictions.
    """

    def __init__(self, tab, data: pd.DataFrame):
        self.tab = tab
        self.data: pd.DataFrame = data

        self._init_results()

        self.input_data_table: Table = None
        self.results_table: Table = None
        self.selected_row_results = None

        self.client_simulator: ClientSimulator = ClientSimulator(
            tenant_id=constants.TENANT_ID,
            dataset_id=constants.DATASET_ID,
        )
        self._run()

    def _init_results(self):
        if "results" in st.session_state:
            results = st.session_state.results
            self.results: Optional[pd.DataFrame] = results
            self.id_to_results = results.set_index(constants.REG_ID_COL).to_dict(
                "index"
            )
        else:
            self.results: Optional[pd.DataFrame] = None
            self.id_to_results: Optional[Dict[str, Dict]] = None

    def _run(self):
        with self.tab:
            [st.markdown(text) for text in constants.TEST_TAB_INFO_TEXT]
            self._display_input_data_table_col()
            if st.button("Send edited data to model", type="primary"):
                self._send_edited_data_to_model()
                st.divider()
            self.results_table_widget, self.results_details_widget = st.columns(
                [constants.TABLE_WIDTH_FRACTION, 1 - constants.TABLE_WIDTH_FRACTION]
            )
            self._display_results_table()
            self._display_results_registration_details()

    def _display_input_data_table_col(self):
        st.subheader("List of registrations")
        self.data.sort_values(by=["employeeId", "date"], inplace=True)
        self.input_data_table = Table(self.data, editible=True, key="predict_tab_table")

    def _display_results_table(self):
        with self.results_table_widget:
            if self.results is not None:
                st.subheader("Results")
                columns_to_drop = [
                    constants.REL_REG_IDS_COL,
                    constants.SUBMODEL_ID_COL,
                    constants.AGGREGATED_COL,
                    constants.SIGNIFICANT_FIELDS_COL,
                ]

                data = self.results.copy()

                # drop the rows that have date yesterday:
                data = data[data["date"] != "2024-01-24"]

                modified_data = data.drop(columns_to_drop, axis=1)

                self.results_table = Table(
                    modified_data, key="predict_tab_results_table"
                )

    def _display_results_registration_details(self):
        if self.results is not None:
            self.results_details_widget.subheader("Result details")
        if self.results_table is not None and self.results_table.get_selected_row():
            self.results_details_widget.write(
                self.id_to_results[
                    self.results_table.get_selected_row()[0][constants.REG_ID_COL]
                ]
            )

    def _transform_numericals(self, entry):
        if isinstance(entry, str):
            try:
                return json.loads(entry)
            except json.JSONDecodeError:
                return None  # or some default value
        elif isinstance(entry, list) or isinstance(entry, dict):
            return entry
        else:
            return None  # or some default value

    def _send_edited_data_to_model(self):
        """
        Sends test registrations, that can have been edited, to the model using the realtime endpoint.
        For this to work, we need to have models trained on the dataset already.
        """
        print("Sending edited data to model")

        with st.spinner("Running predictions..."):
            modified_data_types = constants.DATA_TYPES.copy()
            modified_data_types.pop(constants.NUMERICALS_COL, None)

            # Apply type casting to the DataFrame
            predict_data: Dict = self.input_data_table.get_edited_data().astype(
                modified_data_types
            )

            predict_data["numericals"] = predict_data["numericals"].apply(
                self._transform_numericals
            )

            results = self.client_simulator.predict(predict_data)

            if results is None:
                st.error('Something went wrong with creating the predictions. \
                        Make sure all environment variables are set correctly, and that you have a trained model.')
                return 

            results_as_df: pd.DataFrame = pd.DataFrame.from_records(results)

            results_as_df.sort_values(
                constants.ANOMALY_SCORE_COL, ascending=False, inplace=True
            )
            self.results = results_as_df
            self.id_to_results = results_as_df.set_index(constants.REG_ID_COL).to_dict(
                "index"
            )
            st.session_state.results = results_as_df

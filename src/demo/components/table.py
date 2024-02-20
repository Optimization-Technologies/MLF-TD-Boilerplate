import pandas as pd
import json 
from typing import Dict, List, Optional
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid import JsCode

import src.demo.constants as constants

class Table:
    def __init__(
        self,
        data: pd.DataFrame,
        key: str = None,
        height: Optional[int] = None,
        editible: bool = False,
        color_cols: List[str] = None,
    ):
        self.data: pd.DataFrame = self._prepare_data(data)  # Prepare data
        self.selected_row: Dict = None
        self.height: int = height
        self.editible: bool = editible
        self.key = key
        self.edited_data: pd.DataFrame = None
        self._create_table()

    def _prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "numericals" in data.columns:
            data["numericals"] = data["numericals"].apply(lambda x: json.dumps(x))
        return data

    def _create_table(self):
        grid_options_builder = GridOptionsBuilder.from_dataframe(self.data)

        # Configure conditional styling
        if constants.ANOMALY_SCORE_COL in self.data.columns:
            anomaly_score_style_jscode = JsCode(
                """
                function(params) {
                    if (params.value <= 8) {
                        return { 'backgroundColor': '#77dd77' };
                    } else if (params.value < 20) {
                        return { 'backgroundColor': '#ffb347' };
                    } else {
                        return { 'backgroundColor': '#fa8072' };
                    }
                };
                """
            )

            grid_options_builder.configure_column(
                constants.ANOMALY_SCORE_COL, cellStyle=anomaly_score_style_jscode
            )

        grid_options_builder.configure_selection("single", use_checkbox=False)

        if self.editible:
            grid_options_builder.configure_default_column(editable=True)
        ag_grid = AgGrid(
            self.data,
            key=self.key,
            use_container_width=True,
            height=self.height,
            min_height=100,
            gridOptions=grid_options_builder.build(),
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
        )
        self.selected_row = ag_grid["selected_rows"]
        self.edited_data = ag_grid["data"]

    def get_selected_row(self):
        return self.selected_row or None

    def get_edited_data(self):
        return self.edited_data

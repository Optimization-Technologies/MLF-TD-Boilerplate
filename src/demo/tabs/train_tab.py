import pandas as pd
import streamlit as st
import plotly.express as px

from src.demo.components.table import Table
import src.demo.constants as constants 


class TrainTab:
    """
    In this tab, the user can inspect the training data and see the results of the training.
    """

    def __init__(self, tab, data: pd.DataFrame):
        self.tab = tab
        self.data = data
        self.table: Table = None
        self._run()

    def _run(self):
        with self.tab:
            _title_and_text()
            col1, _, col2, col3, _ = st.columns(5)
            employee: str = col1.selectbox(
                "Select employee",
                ["All employees"] + list(self.data.employeeId.unique()),
            )
            show_charts: bool = col1.checkbox("Show charts")

            filtered_data = (
                self.data[self.data.employeeId == employee]
                if employee != "All employees"
                else self.data
            )

            col2.metric("Number of registrations", len(filtered_data))
            col3.metric(
                "Number of work categories", filtered_data["workCategory"].nunique()
            )

            self.id_to_data = filtered_data.set_index("registrationId").to_dict("index")

            if show_charts:
                _charts(filtered_data)

            self.table_col, self.details_col = st.columns([0.6, 0.4])
            self._display_table(filtered_data)
            self._display_registration_details()

    def _display_registration_details(self):
        self.details_col.subheader("Registration details")
        if self.table.get_selected_row():
            selected_id = self.table.get_selected_row()[0]["registrationId"]
            self.details_col.write(self.id_to_data[selected_id])

    def _display_table(self, data):
        with self.table_col:
            st.subheader("List of time registrations")
            show_cols = [
                "registrationId",
                "date",
                "employeeId",
                "workDuration",
                "workCategory",
            ]
            dynamic_key = f"table_{hash(str(data.values))}"
            self.table = Table(data[show_cols], height=800, key=dynamic_key)


def _title_and_text():
    st.markdown(constants.TRAIN_TAB_INFO_TEXT)


def _charts(data: pd.DataFrame):
    cols = st.columns([0.8, 0.2])

    metric_to_plot = cols[0].selectbox(
        "Select metric to plot over time",
        options=[
            "workDuration",
            "breakDuration",
            "startTime",
            "endTime",
        ],
        index=0,
    )

    cols[0].subheader(f"{metric_to_plot.capitalize()} over time")

    # Calculate dynamic y-axis range
    min_value = data[metric_to_plot].min()
    max_value = data[metric_to_plot].max()
    y_range = [
        min_value - (max_value - min_value) * 0.1,
        max_value + (max_value - min_value) * 0.1,
    ]

    # Create and plot the line chart
    fig = px.line(
        data,
        x="date",
        y=metric_to_plot,
    )
    fig.update_layout(yaxis_range=y_range)

    cols[0].plotly_chart(
        fig,
        theme="streamlit",
        use_container_width=True,
    )

    cols[1].subheader("Weekday distribution")

    # Convert date column to datetime and extract weekday
    data["weekday"] = pd.to_datetime(data["date"]).dt.day_name()
    active_workdays = data[data["workDuration"] > 0]
    weekday_counts = active_workdays["weekday"].value_counts()

    # Create and plot the pie chart
    pie_fig = px.pie(
        names=weekday_counts.index,
        values=weekday_counts.values,
    )

    cols[1].plotly_chart(
        pie_fig,
        theme="streamlit",
        use_container_width=True,
    )

import time
import pandas as pd
from typing import List, Dict
from src.demo.api.api_caller import ApiCaller

class ClientSimulator:
    """
    Class with methods to simulate client calling API with one dataset (customer)
    """

    def __init__(self, tenant_id: str, dataset_id: str) -> None:
        self.tenant_id = tenant_id
        self.dataset_id = dataset_id
        self.api_caller = ApiCaller(tenant_id)
        self.current_job_status = ""

    def upload_data(self, train_df: pd.DataFrame):
        train_regs = train_df.to_dict("records")
        print("Uploading data")
        self._reset_job_status()
        self.api_caller.upload_data(self.dataset_id, train_regs)
        while True:
            time.sleep(5)
            if self._is_finished():
                break

    def start_training(self):
        print("Training")
        self._reset_job_status()
        self.api_caller.start_trainer(self.dataset_id)
        while True:
            time.sleep(5)
            if self._is_finished():
                break

    def stream_day_by_day(self, stream_df: pd.DataFrame) -> pd.DataFrame:
        print("Streaming")
        stream_regs = stream_df.to_dict("records")
        for date in sorted(stream_df["date"].unique()):
            next_day_pred_regs = [reg for reg in stream_regs if reg["date"] == date]

            print("\nStreaming for date", date)
            self._reset_job_status()
            self.api_caller.upload_data(self.dataset_id, next_day_pred_regs)

            while True:
                time.sleep(10)
                if self._is_finished():
                    break

            print("Updating models for date", date)
            self._reset_job_status()
            self.api_caller.start_trainer(self.dataset_id, rebuild_models=False)
            while True:
                time.sleep(10)
                if self._is_finished():
                    break

    def predict(self, pred_df: pd.DataFrame) -> pd.DataFrame:
        print("Predicting")
        pred_regs = pred_df.to_dict("records")
        self._reset_job_status()

        employee_ids = [_id for _id in pred_df["employeeId"].unique()]

        self.api_caller.create_predictions(self.dataset_id, pred_regs, employee_ids)
        while True:
            time.sleep(10)
            if self._is_finished():
                break
        if self.current_job_status.get("status") == "success":
            results = self.api_caller.get_results()
            result_regs = results["results"][0]["predictions"]
            result_df = pd.DataFrame.from_records(result_regs)
            print("Got", len(result_df), "results")
            return result_df
        else:
            print("Something wrong with predictions")
            print(self.current_job_status)

    def predict_realtime(self, pred_data: List[Dict]) -> pd.DataFrame:
        print("Predicting")
        self._reset_job_status()
        pred_data = pred_data.to_dict("records")

        try:
            results: Dict[
                str, List[Dict[str, List]]
            ] = self.api_caller.get_real_time_predictions(self.dataset_id, pred_data)
            return results["results"][0]["predictions"]
        except:
            print("Something wrong with realtime predictions")

    def stream_and_predict_day_by_day(
        self, pred_df: pd.DataFrame, employee_ids=None
    ) -> pd.DataFrame:
        """
        Attempts to simulate realistic scenario where a cleitn typically at the end of each day
        - Fetches predictions on new data
        - Uploads new data that is approved
        - Updates models
        """
        print("Streaming and predicting")
        counter = 1
        if employee_ids is None:
            employee_ids = [_id for _id in pred_df["employeeId"].unique()]
        pred_regs = pred_df.to_dict("records")
        all_results = []
        for date in sorted(pred_df["date"].unique()):
            next_day_pred_regs = [reg for reg in pred_regs if reg["date"] == date]

            print("\nPredicting for date", date)
            self._reset_job_status()
            self.api_caller.create_predictions(
                self.dataset_id, next_day_pred_regs, employee_ids
            )
            while True:
                time.sleep(5)
                if self._is_finished():
                    break
            if self.current_job_status.get("status") == "success":
                results = self.api_caller.get_results()
                result_regs = results["results"][0]["predictions"]
                result_df = pd.DataFrame.from_records(result_regs)
                result_df["call_count"] = counter
                counter += 1
                print("Got", len(result_df), "results")
                all_results.append(result_df)
            else:
                print("Something wrong with predictions")
                print(self.current_job_status)

            print("Uploading data for date", date)
            self._reset_job_status()
            self.api_caller.upload_data(self.dataset_id, next_day_pred_regs)

            while True:
                time.sleep(5)
                if self._is_finished():
                    break

            print("Updating models for date", date)
            self._reset_job_status()
            self.api_caller.start_trainer(self.dataset_id, rebuild_models=False)
            while True:
                time.sleep(5)
                if self._is_finished():
                    break

        results = pd.concat(all_results, ignore_index=True)
        lost_predictions = pred_df[
            ~pred_df.registrationId.isin(results.registrationId.unique())
        ]
        if len(lost_predictions) > 0:
            print(
                "Warning:",
                len(lost_predictions),
                "registrations did not recieve any predictions",
            )

        return results

    def delete_dataset(self):
        print("Deleting dataset")
        print("\nAll datasets before:")
        print(self.api_caller.get_data_info())
        self.api_caller.delete_dataset(self.dataset_id)
        print("\nAll datasets after:")
        print(self.api_caller.get_data_info())

    def _is_finished(self) -> bool:
        """
        Wether the job with the current job id finished or not.
        """
        job_status = self.api_caller.get_job_status(print_status=False)
        if job_status != self.current_job_status:
            print(job_status)
            self.current_job_status = job_status
        if job_status is None:
            print("Job status is None")
            return True
        if job_status.get("status") == "success":
            print("Job finished successfully")
            return True
        return False

    def _reset_job_status(self):
        self.current_job_status = ""

    def get_data_info(self, dataset_id: str) -> Dict:
        return self.api_caller.get_data_info(dataset_id)

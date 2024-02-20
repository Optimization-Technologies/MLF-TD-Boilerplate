import json
import requests
import boto3
from typing import List, Dict

from src.demo.api.token_handler import TokenHandler
from src.demo.api.constants import (
    BASE_URL,
    REG_FIELDS,
    MODEL_BUCKET,
    VISMA_CONNECT_CLIENT_ID,
)

class ApiCaller:
    """
    Class for handling logic related to calling the Time Detect API.
    """

    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id
        self.token_handler = TokenHandler()
        self.current_job_id: str = None

    def _prepare_registrations(self, registrations: List[Dict]) -> List[Dict]:
        """
        Prepare registrations for upload to Time Detect API.
        """
        registrations = [
            {key: val for key, val in registration.items() if key in REG_FIELDS}
            for registration in registrations
        ]
        return registrations

    def health_check(self) -> int:
        url: str = f"{BASE_URL}/health_check"
        response = requests.get(url)
        return response.status_code

    def get_job_status(self, print_status=True) -> Dict:
        if self.current_job_id is None:
            print("No job id found")
            return
        url: str = f"{BASE_URL}/status"
        token: str = self.token_handler.get_token()
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "jobId": self.current_job_id,
        }
        response = requests.get(url, headers=headers)

        result: Dict = json.loads(response.text)
        if print_status:
            print(result)
        return result

    def upload_data(self, dataset_ids: List[str], registrations: List[Dict]) -> None:
        url: str = self._get_presigned_url()
        registrations = self._prepare_registrations(registrations)
        payload = {
            "datasets": [
                {"datasetId": ds, "registrations": registrations} for ds in dataset_ids
            ]
        }
        response = requests.put(url, data=json.dumps(payload))

        if response.status_code == 200:
            print("Raw data uploaded successfully")
        else:
            print("Something went wrong when uploading data")

    def start_trainer(self, dataset_ids: List[str], rebuild_models: bool = True):
        self.current_job_id = None
        url: str = f"{BASE_URL}/start_trainer"
        token: str = self.token_handler.get_token()
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "parameters": [
                {"datasetId": ds, "rebuildModels": rebuild_models} for ds in dataset_ids
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 202:
            result: Dict = json.loads(response.text)
            self.current_job_id = result["jobId"]
            print("Trainer started successfully")
        else:
            print("Something went wrong when starting trainer")

    def create_predictions(
        self, dataset_id: str, registrations: List[Dict], employee_ids: List[str]
    ) -> None:
        self.current_job_id = None
        url: str = f"{BASE_URL}/create_prediction"
        token: str = self.token_handler.get_token()
        registrations = self._prepare_registrations(registrations)
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "parameters": [
                {
                    "datasetId": dataset_id,
                    "registrations": registrations,
                    "aggregateForEmployeeIds": employee_ids,
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 202:
            result: Dict = json.loads(response.text)
            self.current_job_id = result["jobId"]
            print("Prediction job started successfully")
        else:
            print("Something went wrong when creating predictions")

    def get_results(self):
        url: str = f"{BASE_URL}/results"
        token: str = self.token_handler.get_token()
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "jobId": self.current_job_id,
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result: Dict = json.loads(response.text)
            return result
        else:
            print("Something went wrong when getting results")

    def get_data_info(self, dataset_id: str = None):
        url: str = f"{BASE_URL}/data"
        token: str = self.token_handler.get_token()
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "datasetId": dataset_id,
        }
        if dataset_id is None:
            headers.pop("datasetId")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result: Dict = json.loads(response.text)
            return result
        else:
            print("Something went wrong when getting data info")

    def get_real_time_predictions(
        self, dataset_id: str, registrations: List[Dict]
    ) -> Dict:
        url: str = f"{BASE_URL}/real_time_prediction"
        token: str = self.token_handler.get_token()

        registrations = self._prepare_registrations(registrations)
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "parameters": [{"datasetId": dataset_id, "registrations": registrations}]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            result: Dict = json.loads(response.text)
            return result
        else:
            print("Something went wrong when creating real time predictions")

    def delete_dataset(self, dataset_id: str):
        url: str = f"{BASE_URL}/data/{dataset_id}"
        token: str = self.token_handler.get_token()
        headers = {
            "tenantId": self.tenant_id,
            "Authorization": f"Bearer {token}",
            "datasetId": dataset_id,
            "Content-Type": "application/json",
        }
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            result: Dict = json.loads(response.text)
            return result
        else:
            print("Something went wrong when deleting dataset")

    def _get_presigned_url(self) -> str:
        self.current_job_id = None
        url: str = f"{BASE_URL}/presigned_url"
        token: str = self.token_handler.get_token()
        headers = {"tenantId": self.tenant_id, "Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result: Dict = json.loads(response.text)
            self.current_job_id = result["jobId"]
            return result["url"]
        else:
            print("Something went wrong when getting presigned url")

    def delete_model_and_metadata(self, dataset_id: str):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(MODEL_BUCKET)
        bucket.objects.filter(
            Prefix=f"{VISMA_CONNECT_CLIENT_ID}/{self.tenant_id}/{dataset_id}"
        ).delete()

"""Load from sources to GCS

Description: Ingests the data from a Public API into a gcp bucket.
"""

import os
import logging
from datetime import datetime
from airflow import DAG
from airflow.decorators import dag
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from google.cloud import storage
import pyarrow.csv as pv
from pathlib import Path
import requests
import tempfile

# constants
# GCP constants
GCP_CONN_ID = 'google_cloud_storage_capstone'
GCS_BUCKET_NAME = 'wizeline-capstone-bucket-gideon'
GCS_KEY_NAME = "chart-data.csv"

# Postgres constants
POSTGRES_CONN_ID = "google-demo-session-6-conn"
POSTGRES_TABLE_NAME = "chart_data"

bucket = 'wizeline-capstone-bucket-gideon'
local_movie_reviews_path_1 = "D:\Desktop\Wizeline Bootcamp\Capstone Project\project\movie_review.csv"
local_log_reviews_path_2 = "D:\Desktop\Wizeline Bootcamp\Capstone Project\project\log_reviews.csv"
local_user_purchase_path_3 = "D:\Desktop\Wizeline Bootcamp\Capstone Project\project\user_purchase.csv"

dataset_file_1 = "movie_review.csv"
dataset_file_2 = "log_reviews.csv"
dataset_file_3 = "user_purchase.csv"
# path_to_local_home = "/opt/airflow"
#credentials_file = Path("service_account.json")

def download_samples_from_url(path: str) -> None:
    """Downloads a set of samples into the specified path.

    Args:
        path (str): Path to output file.
    """
    response_1 = requests.get(dataset_url_1)
    with open(dataset_file_1, mode="wb") as file_1:
            file_1.write(response_1.content)

def upload_file_func():
    hook = GCSHook(gcp_conn_id=GCP_CONN_ID)
    bucket_name = GCS_BUCKET_NAME
    object_name = dataset_file_1
    filename = Path(dataset_file_1)
    hook.upload(bucket_name, object_name, filename)
        
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily", # https://airflow.apache.org/docs/apache-airflow/1.10.1/scheduler.html
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['upload-gcs']
) as dag:
    
    upload_file = PythonOperator(task_id='upload_file', python_callable=upload_file_func)

    # Workflow for task direction
    upload_file
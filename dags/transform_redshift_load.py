from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('transform_redshift_dag', default_args=default_args, schedule_interval="@once",catchup=False)


# Define the Glue Job
transform_task = GlueJobOperator(
    task_id='transform_task',
    job_name='glue_transform_task',
    script_location='s3://glue-scripts-weather/scripts/weather_data_ingestion.py',
    s3_bucket='s3://glue-scripts-weather/',
    aws_conn_id='aws_default',
    region_name="us-east-1",
    iam_role_name='glue-role',
    create_job_kwargs ={"GlueVersion": "4.0", "NumberOfWorkers": 2, "WorkerType": "G.1X", "Connections":{"Connections":["Redshift-New-Connection"]},},
    dag=dag,
)

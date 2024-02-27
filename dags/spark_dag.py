from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.providers.cncf.kubernetes.hooks.kubernetes import KubernetesHook
from airflow.utils.dates import days_ago
k8s_hook = KubernetesHook(conn_id='kubernetes_config')

default_args = {
    'owner': 'mouadbh',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 3
}

with DAG(
    'spark_pi',
    start_date=days_ago(1),
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    tags=['example']
):
    submit = SparkKubernetesOperator(
        task_id='spark_transform_data',
        namespace='spark-operator',
        application_file='/kubernetes/spark-pi.yaml',
        kubernetes_conn_id='kubernetes_default',
        do_xcom_push=True,
    )

    submit
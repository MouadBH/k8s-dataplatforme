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

dag =  DAG(
    'spark_pi',
    start_date=days_ago(1),
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    description='submit spark-pi as sparkApplication on kubernetes',
    tags=['example', 'python']
)
submit = SparkKubernetesOperator(
    task_id='sparkpy_pi_submit',
    namespace='spark-apps',
    application_file='k8s/sparkpy-dag-pi.yaml',
    kubernetes_conn_id='kubernetes_default',
    do_xcom_push=True,
    dag=dag
)

senor = SparkKubernetesSensor(
    task_id='sparkpy_pi_monitor',
    namespace="spark-apps",
    application_name="{{ task_instance.xcom_pull(task_ids='sparkpy_pi_submit')['metadata']['name'] }}",
    kubernetes_conn_id="kubernetes_default",
    dag=dag
)

submit >> senor
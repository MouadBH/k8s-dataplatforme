from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


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

dag = DAG(
    dag_id="hello_world",
    start_date=days_ago(1),
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    description='testing airflow dags.',
    tags=['example']
)
task1 = BashOperator(
    task_id = 'hello_world',
    bash_command='echo "Hello darkness my old friend."',
    dag=dag,
)

task2 = BashOperator(
    task_id = 'goodbye',
    bash_command='echo "Goodbye ...."',
    dag=dag,

)

task3 = BashOperator(
    task_id='hell',
    bash_command='echo "its hell ....."',
    dag=dag,

)

task1 >> task2 >> task3
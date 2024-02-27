from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


dag = DAG(
    dag_id="hello_world",
    start_date=datetime(2024, 1, 25),
    schedule=timedelta(days=1),
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
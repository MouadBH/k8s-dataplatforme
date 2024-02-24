# k8s-dp

## Airflow
installing Airflow using Helm chart. Add the official Apache Airflow Helm chart repository to our Helm installation
- helm repo add apache-airflow https://airflow.apache.org
updates our local Helm chart repository index using this command.
- helm repo update
Install the Airflow chart into the “airflow” namespace. This process sets up the necessary components for Airflow, such as the PostgreSQL database, Redis, scheduler, web server, and worker pods.
- helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace

Cluster manager = k8s
orchestration  = airflow
Object store = MinIo
bash = Spark
streaming  = flink
streamaing data = kafka
open table format = inceberg
monitoring = prometheus 
ci/cd = github actions
data delivery = trino presto
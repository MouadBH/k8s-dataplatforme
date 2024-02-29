#!/usr/bin/env just --justfile

default:
    just --list

alias adb := airflow-docker-build
alias ai := airflow-install
alias soi := spark-operator-install


# Building Airflow image.
airflow-docker-build:
    echo 'Building Airflow image.'
    docker build -t myairflow:1.0 k8s/airflow/docker/

# Install Airflow Helm chart
airflow-install:
    echo 'Installing Airflow Helm chart.'
    helm repo add apache-airflow https://airflow.apache.org
    minikube image load myairflow:1.0
    helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --values k8s/airflow/helm/values.yaml

# Install Spark operator Helm chart.
spark-operator-install:
    echo 'Installing Spark operator Helm chart.'
    kubectl create namespace spark-apps
    # Create a service account under the namespace spark-apps
    kubectl create serviceaccount spark --namespace=spark-apps
    # Create a cluster binding
    kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=spark-apps:spark --namespace=spark-apps
    # Add a Helm chart repository.
    helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
    helm install my-release spark-operator/spark-operator --namespace spark-operator --create-namespace --set webhook.enable=true --set sparkJobNamespace=spark-apps

minio-install:
    echo 'Installing Minio.'
    kubectl create namespace minio-dev
    kubectl apply -f k8s/minio/helm/minio-pvc.yaml
    kubectl apply -f k8s/minio/helm//minio-deployment.yaml
    kubectl apply -f k8s/minio/helm/minio-minio-service.yaml

minio-clean:
    echo 'Clean Minio.'
    kubectl delete deployment minio-deployment
    kubectl delete pvc minio-pv-claim
    kubectl delete svc minio-service


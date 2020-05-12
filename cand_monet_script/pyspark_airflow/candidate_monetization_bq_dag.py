# Mateo comment: import necessary packages
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from dataflow_pipeline.dependencies.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from dataflow_pipeline.dependencies.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from dataflow_pipeline.dependencies.general_utils import get_variable
from dataflow_pipeline.dependencies.slack_utils import task_fail_slack_alert

# Mateo comment: Arguments that define DAG
# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'DataEngineering',  # Mateo comment: ?
    'depends_on_past': False,  # Melissa comment: If True, keeps a task from getting triggered if the previous schedule for the task hasn’t succeeded.
    'start_date': days_ago(1),  # Mateo comment: ?
    'email': ['melissa@merlinjobs.com'],  # Mateo comment: a que mail envio las alertas
    'email_on_failure': True,  # Mateo comment: si falla, te envio email?
    'email_on_retry': False,  # Mateo comment: si hago un retry, te envio email?
    'retries': 2,  # Mateo comment: cuantos retries para el DAG
    'retry_delay': timedelta(minutes=5),  # Mateo comment: cuantos tiempo entre retries
    'max_active_runs': 1,  # Mateo comment: cuantos DAGS de este a la vez
    'on_failure_callback': task_fail_slack_alert,  # Mateo comment: si falla, enviame mensaje de Slack
}
# [END default_args]

kubernetes_conn_id = get_variable('kubernetes_data_conn')  # Mateo comment: connect to K8s

# [START instantiate_dag]

# Mateo comment: define DAG
with DAG(
        'k8s_candidate_monetization_bq_dag',
        default_args=default_args,  # Mateo comment: apply what described above
        # twice per day at 7 and 19 (12, 00 UTC,  from Mon-Fri)
        schedule_interval='0 12,0 * * 1-5',
) as dag:

    spark_task = SparkKubernetesOperator(
        task_id='spark_candidate_monetization_bq_task',
        namespace="default",
        application_file="candidate_monetization_bq_spark_app.yaml",  # Mateo comment: here defines what application to run
        kubernetes_conn_id=kubernetes_conn_id,
        do_xcom_push=True,
        dag=dag,
        params={"path": "gs://airflow-dags-new/dags/dataflow_pipeline/dags/kubernetes/candidate_monetization_bq/"})

    spark_monitor = SparkKubernetesSensor(
        task_id='spark_candidate_monetization_bq_monitor',
        namespace="default",
        application_name=
        "{{ task_instance.xcom_pull(task_ids='spark_candidate_monetization_bq_task')['metadata']['name'] }}",
        kubernetes_conn_id=kubernetes_conn_id,
        dag=dag)

    spark_task >> spark_monitor
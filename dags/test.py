from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


dag_args = {
	"depends_on_past": False,
	"email": ["test@test.com"],  # <-- Comilla añadida aquí
	"email_on_failure": False,
	"email_on_retry": False,
	"retries": 1,
	"retry_delay": timedelta(minutes=5),
	# 'queue': 'bash_queue',
	# 'pool' : 'backfill',
	# 'priority_weight' : 10,
	# 'end_date' : datetime(2016, 1, 1),
	# 'wait_for_downstream': False,
	# 'sla' : timedelta(hours=2),
	# 'execution_timeout' : timedelta(seconds=300),
	# 'on_failure_callback' : some_function, # or list of functions
	# 'on_success_callback' : some_other_function, # or list of functions
	# 'on_retry_callback': yet_another_function, # or list of functions
	# 'trigger_rule' : 'all_success'
}


dag = DAG(
	"test1",
	description="Mi primer DAG",
	default_args=dag_args,  # <-- Corregido aquí (de default_Args a default_args)
	schedule_interval=timedelta(days=1),
	start_date=datetime(2021, 1, 1),
	catchup=False,
	tags=["example"],
    params={"commit":"00000000"} #excepciones
)

def tarea0_func(**kwargs):
    conf = kwargs['dag_run'].conf
    
    if "commit" in conf and conf["commit"] == "1":
        raise AirflowFailException("Cancelado, no se despliega el commit 1")

    return {"ok": 1 }

#En Airflow xcom es la salida de una tarea


def tarea2_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea0')
    
    print( 'hola' )
    print( xcom_value )

    return {"ok": 2 }


#Operadores 
tarea0 = PythonOperator(
        task_id="tarea0",
        python_callable=tarea0_func,
        dag=dag
)


tarea1 = BashOperator(
	task_id="print_date",
	bash_command='echo "La fecha es $(date)"',
	dag=dag
)

tarea2 = PythonOperator( 
        task_id='tarea2',
        python_callable=tarea2_func,
        dag=dag
)


#Workflow 

tarea0 >> [ tarea1, tarea2 ] 

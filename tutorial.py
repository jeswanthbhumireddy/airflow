from datetime import datetime, timedelta
from textwrap import dedent

#Dag object; we'll need this to instantiate a DAG
from airflow import DAG

#operators; we need this to operate
from airflow.operators.bash import BashOperator



with DAG(
    "tutorial",
    default_args={
        "depends_on_past": False,
        "email":["jeswanth.bhumireddy@gmail.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A Simple Tutorial of DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2023,5,3),
    catchup=False,
    tags=["example"],
) as dag:

    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False
        bash_command="sleep 5",
        retries=3,
    )

    t1.doc_md = dedent(
        """
        Task documentation
        sample documentation
        ![img] (http:..montics.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
        """
    )

    dag.doc_md = __doc__ 
    dag.doc_md = """
    Sample document placed anywhere
    """

    template_command = dedent(
        """
        {% for i in range(5)%}
            echo "{{ds}}"
            echo "{{macros.ds_add(ds,7)}}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False
        bash_command=template_command
        )

    t1 >> [t2,t3]
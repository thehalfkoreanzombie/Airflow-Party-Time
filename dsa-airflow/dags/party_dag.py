import os
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook

#list of flavors people wanted at the party
FLAVORS_CHOICES = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]

VOTES_FILE_NAME = 'votes.csv'

@task
def read_votes_from_file():
    """
    read all of the votes from the CSV

    This function uses an Airflow File(path) Connection called "data_fs" as the root folder
    to look for the votes csv. Make sure this File(path) connection exists
    """
    # get the data_fs filesystem root path
    data_fs = FSHook(conn_id='data_fs')     # get airflow connection for data_fs
    data_dir = data_fs.get_path()           # get its root path
    print(f"data_fs root path: {data_dir}")

    # create the full path to the airports file
    file_path = os.path.join(data_dir, VOTES_FILE_NAME)
    print(f"reading file: {file_path}")

    # read csv
    df = pd.read_csv(file_path, header=1)
    print(df.head())

@dag(
    schedule_interval="@once",
    start_date=datetime.utcnow(),
    catchup=False,
    default_view='graph',
    is_paused_upon_creation=True,
    tags=['dsa', 'dsa-example'],
)

def party_cake_choice():
    """Example of using FileSensors and FileSystem Connections"""

    # define the file sensor...
    # wait for the airports file in the "data_fs" filesystem connection
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        poke_interval=15,                   # check every 15 seconds
        timeout=(30 * 60),                  # timeout after 30 minutes
        mode='poke',                        # mode: poke, reschedule
        filepath=AIRPORTS_FILE_NAME,        # file path to check (relative to fs_conn)
        fs_conn_id='data_fs',               # file system connection (root path)
    )
    
    read_votes_task = read_votes_from_file()
    
    # orchestrate tasks
    wait_for_file >> read_votes_task

# create the dag
dag = party_cake_choice()
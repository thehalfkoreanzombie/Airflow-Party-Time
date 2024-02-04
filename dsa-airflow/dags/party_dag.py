import os
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook
from statistics import mode

#list of flavors people wanted at the party
FLAVORS_CHOICES = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]

VOTES_FILE_NAME = 'votes.csv'

@dag(
    schedule_interval="@once",
    start_date=datetime.utcnow(),
    catchup=False,
    default_view='graph',
    is_paused_upon_creation=True,
    tags=['party_time']
)

def party_cake_choice():
    
    @task
    def read_votes_with_return_value() -> str:
        """
        read all of the votes from the CSV

        This function uses an Airflow File(path) Connection called "data_fs" as the root folder
        to look for the votes csv. Make sure this File(path) connection exists
        """
        # get the data_fs filesystem root path
        data_fs = FSHook(fs_conn_id='data_fs')     # get airflow connection for data_fs
        data_dir = data_fs.get_path()           # get its root path
        print(f"data_fs root path: {data_dir}")

        # create the full path to the airports file
        file_path = os.path.join(data_dir, VOTES_FILE_NAME)
        print(f"reading file: {file_path}")

        # read csv
        df = pd.read_csv(file_path, header=0)
        all_votes = df['votes'].tolist()
        #print(all_votes)
        valid_votes = []
        for item in all_votes:
            if item in FLAVORS_CHOICES:
                valid_votes.append(item)
        return valid_votes

    @task
    def most_voted_flavor(flavor_list: str):
        flavor = mode(flavor_list)
        print(f"The flavor of choice is {flavor}!!!")

    wait_for_file = FileSensor(
        task_id='wait_for_file',
        poke_interval=15,                   # check every 15 seconds
        timeout=(30 * 60),                  # timeout after 30 minutes
        mode='poke',                        # mode: poke, reschedule
        filepath=VOTES_FILE_NAME,        # file path to check (relative to fs_conn)
        fs_conn_id='data_fs',               # file system connection (root path)
    )
    
    t1 = read_votes_with_return_value()

    t2 = most_voted_flavor(t1)
    
    # orchestrate tasks
    wait_for_file >> t1 >> t2

    # create the dag
dag = party_cake_choice()
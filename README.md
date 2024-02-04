# # My Eleventh Code Review: Airflow 1

## Alex Wallace

## Description
Hello, fellow party goers! welcome to the datastack academy party, where we will be having a celebratory cake. What flavor of cake you ask? No idea! We have a list of possible flavor choices, which looks like this:

["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]

"confetti" or "rose" flavored? EWWW! hopefully no one chooses those.

Apparently, there have also been a multitude of votes cast for flavors people at the party would like the cake to be. The votes can be found [here](./dsa-airflow/data/votes.csv). I know, I know, I'm sorry we didn't get your vote in there, but maybe next time!

The trouble here is that we need to know what flavor got voted for the most. If only we had a DAG (directed acyclic graph) that read the votes and told us which flavor got the most votes...

Oh wait, I do! Take a look at the [party_dag](./dsa-airflow/dags/party_dag.py)! I created this dag in order to find the most popular flavor, that way we can get a cake of said flavor before the festivities begin. 

This DAG does everything we need and more! it even comes equipped with a couple of embellishments including:
- a file sensor to wait for the file [votes.csv](./dsa-airflow/data/votes.csv) to exist within the data folder. This sensor will prevent the rest of the DAG from running unless the csv file is in our data folder.
- 2 tasks defined by task decorators, and a dag decorator to define our DAG. 
- a return_value (XCom) used from the read_votes_with_return_value function.

The graph for this DAG looks like this:

![Party_DAG](/images/party_dag.png)

Here, we can see the three tasks in our airflow DAG:
- wait_for_file
- read_votes_with_return_value
- most_voted_flavor

The first task, wait_for_file, is the sensor created to check if our votes.csv file is in our data folder. Once it reads it, the dag will move on to task 2. 

![wait_for_file](/images/wait_for_file.png)

In the read_votes_with_return_value task, I read the csv into a dataframe, put all of the votes into a list, and removed any items in the list that weren't one of the flavor choices. I then passed this list into the next task using an XCom return_value.

![XCom_return_value](/images/return_value.png)

Lastly, in the most_voted_flavor task, I used the XCom return_value from the previous task, and determined which flavor was voted on the most by finding the mode (most frequent number) of the list. This flavor was printed out as a result, giving us the flavor to use for our beloved cake!

![Flavor_choice](/images/flavor_choice.png)

And the results are in...

Which means we're having a lemon cake!!!

![Lemon_cake](/images/lemon_cake.webp)

This party will be held on 01/01/3024. Hope to see you there!
 
## Setup/Installation Requirements
In order to set this up, you will need to make a directory for your file and then switch over to that directory. Then, create a virtual environment for python 3 to work in. Change into your virtual environment using source venv/bin/activate. You will need to install the requirements.txt file

```
pip install -r requirements.txt
```

After creating your virtual environment in your project directory, you will need to make sure you have docker installed. The link to the different installation options can be found [here](https://docs.docker.com/engine/install/). Once you have docker up and running, you will need to allocate atleast 4gb worth of cpu memory to the airflow docker container. To do this:
- click the gear icon on the top right to go into Settings
- click the 'Resources' tab on the left 
- Set the Memory slider to at least 4GB as shown below, then click 'Apply & Restart':

Once docker is all set up, we have to set up a folder to contain our airflow files. In your project directory, create a folder called dsa-airflow. Using your CLI (command line interface), path into your dsa-airflow folder. Then, create a logs folder, plugins folder, a dags folder, and a config folder within your dsa-airflow folder.

```bash
mkdir -p ./dags ./logs ./plugins ./config
```

You also need to create a .env in your dsa-airflow folder using 

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

After completing this, you will need to fetch the docker yaml file into your dsa-airflow folder using 

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

In this yaml file, you'll need to mount your local airflow directory to /opt/airflow. You'll also need to direct your data folder. You can add these in the yaml like this:

![Volumes](/images/yaml_volumes.png)

Once you have your dsa-airflow folder intact, you need to start airflow. in a bash terminal, navigate to this dsa-airflow directory. Use:

```bash
docker compose up airflow-init
```

This command runs database migrations (which moves data between databases), and creates a default user account with the login 'airflow' and the password 'airflow'. After this task has been completed (you should see an 'exited with code 0'), press ctrl+c while your CLI is open to stop airflow from running. 

Once initialized, we can start the rest of our containers with a simple

```bash
docker-compose up
```

When you have airflow running in your CLI, you will need to open a new terminal to perform any actions necessary using bash. 

Using these steps, you should have airflow talking to your local computer. In order to use the airflow UI, go to the URL [localhost:8080/home](localhost:8080/home). From here, type in your username 'airflow' and password 'airflow' to log into the airflow UI. In this interface, you will be able to run any DAGs you have created.

Now that we have airflow up and running, lets look at making a connection. In your UI, look at the bar to the right of the airflow logo in the upper left corner and go to Admin -> connections. This will take you to your connections directory. Here, you can click on the blue + button to create a connection. Name this connection whatever you'd like (I called mine data_fs) and set your path to the data folder within your dsa-airflow (create this folder if you need to). The path should be /data since you're already in your dsa-airflow folder. Then, press create. You should be able to use this connection to access your data folder in your dsa-airflow directory, allowing you to make a file sensor for the data file. 

When you need to power down airflow, navigate to your CLI with airflow running and press CTRL + C. This will stop airflow from running. Additionally, run the command docker system prune --volumes in order to delete the volumes you created using airflow.

An alternative way to power down airflow is to type 

```bash
docker compose down
```

in your usable CLI. 

## Known Bugs
No known bugs

## License
Copyright 2023 Alex Wallace

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
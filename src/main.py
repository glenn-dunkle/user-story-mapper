# main.py
import requests
# import logging
from src.connectors import miro_connector as miro_conn
from src.connectors import sob_connector as sob_conn
from src.affinity_grouper import affinity_grouper as aff_grouper
from src.util import config_helper

print("Hello from Docker!")

# Load the configuration when the module is imported
config_helper.load_config() 
from src.util.config_helper import CONFIG


# TODO set the logging level, use loggin.debug, verify stdout and stderr are captured by Docker
""" if logging.basicConfig(level=logging.DEBUG):
    start_time = time.time()

    while time.time() - start_time < 30:
        print("DEBUG: Hello from User Story Mapper!")
        time.sleep(5)
 """

# TODO Connect to the Miro board using the MiroConnector class1
miroConn = miro_conn.MiroConnector()
try:
    miro_data = miroConn.getBoard()
    print("Successfully connected to Miro board.")
except requests.ConnectionError as e:
    print(f"Connection error: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# TODO Use the AffinityGrouper class to group the notes
affGrouper = aff_grouper.AffinityGrouper()
try:
    if miro_data:
        affinity_groups = affGrouper.getAffinityGroups(miro_data)
        print("Affinity groups created successfully.")
except Exception as e:
    print(f"An error occurred while grouping notes: {e}")

# TODO Connect to the SoB API using the SobConnector class
sobConn = sob_conn.SobConnector()
try:
    if affinity_groups:
        sob_data = sobConn.postBoard(affinity_groups)
        print("Successfully connected to StoriesOnBoard board.")
except requests.ConnectionError as e:
    print(f"Connection error: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

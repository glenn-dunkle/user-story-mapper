# main.py
import requests
import logging
import os
from src.util import config_helper
from src.connectors import miro_connector as miro_conn
from src.connectors import jira_connector as jira_conn
from src.affinity_grouper import affinity_grouper as aff_grouper
from src.loggers import err_logger

# Load the configuration when the module is imported
config_helper.load_config() 
from src.util.config_helper import CONFIG

errLog = err_logger.ErrLogger()
errLog.getLogger()
# Log the start of the application 

errLog.logMessage("Initializing User Story Mapper...")
errLog.logMessage(f"Configuration loaded: {CONFIG}")

# Connect to the Miro board of interest and pull the board items
try:
    miroConn = miro_conn.MiroConnector()
    miro_data = miroConn.getBoard()
    print("Successfully connected to Miro board.")
    print(miro_data[:5])
except requests.ConnectionError as e:
    print(f"Connection error: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Group the Miro board items into a dynamic number of groups using affinity grouping AI
try:
    if miro_data:
        affGrouper = aff_grouper.AffinityGrouper()
        affinity_groups = affGrouper.getAffinityGroups(miro_data)
        print("Affinity groups created successfully.")
        print("Miro data as tree:")
        affGrouper.printAffinityGroups(affinity_groups)

except Exception as e:
    print(f"An error occurred while grouping notes: {e}")

# TODO Connect to the SoB API using the SobConnector class
# StoriesOnBoard no longer provides a public API. So we'll try loading the
# affinity groups in to Jira. Then we can either use Jira or the Jira->SoB connector
# to use StoriesOnBoard

#TODO: Figure out how to dump the entire error response body
try:
    if affinity_groups:
        jiraConn = jira_conn.JiraConnector()
        print("Successfully connected to Jira project.")
        jira_epics = jiraConn.postGroupsToJira(affinity_groups)
except requests.ConnectionError as e:
    print(f"Connection error: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

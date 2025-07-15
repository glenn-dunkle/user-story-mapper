import uuid
from base64 import b64encode
from src.util.http_helper import HTTPHelper
from src.util.config_helper import CONFIG

class JiraConnector(HTTPHelper):
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        super().__init__(f"jira_conn_{self.uuid}")
        self.user = CONFIG["jira"]["JIRA_USER"]
        self.api_key = CONFIG["jira"]["JIRA_API_KEY"]
        self.base_url = CONFIG["jira"]["JIRA_BASE_URL"]
        self.project_key = CONFIG["jira"]["JIRA_PROJECT_KEY"]
        self.http_content_type = CONFIG["jira"]["JIRA_HTTP_CONTENT_TYPE"]
        
        auth_str = f"{self.user}:{self.api_key}"
        self.b64_auth = b64encode(auth_str.encode()).decode()


    def __postEpic(self, epic_name):
        url = f"{self.base_url}/issue"
        headers = {
            "Authorization": f"Basic {self.b64_auth}",
            "Content-Type": f"{self.http_content_type}"
        }

        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": epic_name,
                "description": f"Automagically created through programmatic affinity grouping from a Miro board",
                "issuetype": {"name": "Epic"}
            }
        }
        
        return super().post(self, url=url, headers=headers, json=data)
 
        # TODO: Figure out to incorporate the intent here.
#        super().getHTTPErrorMessage(super().post(self, url=url, headers=headers, json=data), "jira connector")

    def __postStory(self, epic_key, summary, description):
        url = f"{self.base_url}/issue"
        headers = {
            "Authorization": f"Basic {self.b64_auth}",
            "Content-Type": f"{self.http_content_type}"
        }

        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Story"},
                "parent": {"key": epic_key}  # Jira field 10018 is Parent Link. Epic link deprecated.
            }
        }
        return super().post(self, url=url, headers=headers, json=data)

    def postGroupsToJira(self, affinity_groups):
        created_epics = []

        # Create an epic for each cluster that was created from affinity grouping
#        for cluster_id, stories in affinity_groups.items():
#            epic_key = epic_response.json()["key"]
#            created_epics.append(epic_key)
#            for story in stories:
#                self.__postStory

        for cluster_id, stories in affinity_groups.items():
            story_count = 0
            epic_response = self.__postEpic(f"Cluster {cluster_id}")
            epic_key = epic_response.json()["key"]
            created_epics.append(epic_key)
            for story in stories:
                story_count += 1
                summary = f"{cluster_id}.{story_count}: {story}"
                self.__postStory(epic_key, summary, story)
        return created_epics
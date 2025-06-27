import uuid
from src.util.http_helper import HttpHelper
from src.util.config_helper import CONFIG

class JiraConnector(HttpHelper):
    def __init__(self):
        self.uuid = str(self.uuid64())
        super().__init__(f"jira_conn_{self.uuid}")
        self.base_url = CONFIG["jira"]["JIRA_BASE_URL"]
        self.project_key = CONFIG["jira"]["JIRA_PROJECT_KEY"]

    def __postEpic(self, epic_name, epic_summary):
        url = f"{self.jira_url}/issue"
        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": epic_summary,
                "issuetype": {"name": "Epic"},
                "customfield_10011": epic_name  # Epic Name field, may need to adjust field id
            }
        }
        return self.super().post(url, json=data)

    def __postStory(self, summary, description, epic_key):
        url = f"{self.base_url}/issue"
        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Story"},
                "customfield_10014": epic_key  # Epic Link field, may need to adjust field id
            }
        }
        return self.post(url, json=data)

    def postGroupsToJira(self, affinity_groups: list[dict]):
        created_epics = []
        for group in affinity_groups:
            epic_resp = self.create_epic(group["name"], group["summary"])
            epic_key = epic_resp["key"]
            created_epics.append(epic_key)
            for story in group["stories"]:
                self.create_story(story["summary"], story.get("description", ""), epic_key)
        return created_epics
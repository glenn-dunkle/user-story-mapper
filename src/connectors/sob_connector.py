import uuid
import json
from src.util.http_helper import HTTPHelper
from src.util.config_helper import CONFIG

class SobConnector(HTTPHelper):
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        super().__init__(f"sob_{self.uuid}")
        self.api_key = CONFIG["sob"]["SOB_API_KEY"]
        self.base_url = CONFIG["sob"]["SOB_BASE_URL"]
        self.board_id = CONFIG["sob"]["SOB_BOARD_ID"]

    def getBoard(self, api_key=None, base_url=None, board_id=None):
        api_key = api_key if api_key else self.api_key
        base_url = base_url if base_url else self.base_url
        board_id = board_id if board_id else self.board_id

        getURL = f"{base_url}{board_id}/items"
        headers = {"Authorization": f"Bearer {api_key}"}

        api_details = {
            "api_key": api_key,
            "base_url": base_url,
            "board_id": board_id,
            "get_url": getURL,
            "headers": headers
        }

        response = super().get(getURL, headers=headers)
        if response.status_code == 200:
            return self.__parse_sob_response(response.json()["data"])

        super().getHttpError(response, api_details)

    def putBoard(self, data, api_key=None, base_url=None, board_id=None):
        api_key = api_key if api_key else self.api_key
        base_url = base_url if base_url else self.base_url
        board_id = board_id if board_id else self.board_id

        putURL = f"{base_url}{board_id}/items"
        headers = {"Authorization": f"Bearer {api_key}"}

        api_details = {
            "api_key": api_key,
            "base_url": base_url,
            "board_id": board_id,
            "put_url": putURL,
            "headers": headers
        }

        response = super().put(putURL, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()

        super().getHttpError(response, api_details)

    def postBoard(self, data, api_key=None, base_url=None, board_id=None, note_clusters=None):
        api_key = api_key if api_key else self.api_key
        base_url = base_url if base_url else self.base_url
        board_id = board_id if board_id else self.board_id 
        postURL = f"{base_url}{board_id}/items"
        headers = {"Authorization": f"Bearer {api_key}"}

        api_details = {
            "api_key": api_key,
            "board_id": board_id,
            "url": postURL,
            "headers": headers
        }
        if note_clusters:
            json_data = {}
            for cluster_id, stories in note_clusters.items():
                cluster_title = f"Cluster {cluster_id}"

                # Create an Epic (blue card)
                epic_payload = {
                    "title": cluster_title,
                    "cardType": "epic",  # or "step" for yellow, "story" for white
                }
                epic_response = super().post(postURL, headers=headers, json=epic_payload)
                epic_response.raise_for_status()
                epic_id = epic_response.json()['id']
                json_data += json_data + json.dumps(epic_response.json())
                super().getHttpError(epic_response, api_details)

                # Create Stories (white cards) under the Epic
                for story in stories:
                    story_payload = {
                        "title": story,
                        "cardType": "story",
                        "parentId": epic_id
                    }
                    story_response = super().post(postURL, headers=headers, json=story_payload)
                    story_response.raise_for_status()
                json_data += json_data + json.dumps(epic_response.json())

                super().getHttpError(epic_response, api_details)

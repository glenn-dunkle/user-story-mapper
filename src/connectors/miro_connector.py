# import requests
import uuid
import urllib.parse
from src.util.http_helper import HTTPHelper
from src.util.config_helper import CONFIG

class MiroConnector(HTTPHelper):
    def __init__(self):
        # Load configuration values from the config file
        self.uuid = str(uuid.uuid4())
        super().__init__(f"miro_{self.uuid}")
        self.api_key = CONFIG["miro"]["MIRO_API_KEY"]
        self.base_url = CONFIG["miro"]["MIRO_BASE_URL"]
        self.board_id = CONFIG["miro"]["MIRO_BOARD_ID"]
        self.http_accept = CONFIG["miro"]["MIRO_HTTP_ACCEPT"]
        self.http_content_type = CONFIG["miro"]["MIRO_HTTP_CONTENT_TYPE"]

    def getBoard(self,
                  api_key=None,
                  base_url=None,
                  board_id=None):
        # Use provided parameters or fall back to class attributes from config file
        api_key = api_key if api_key else self.api_key
        base_url = base_url if base_url else self.base_url
        board_id = board_id if board_id  else self.board_id

        # Construct the URL for fetching board items
        board_id = urllib.parse.quote(board_id, safe="")
        getURL = f"{base_url}{board_id}/items"
        headers = { "Authorization": f"Bearer {api_key}" }

        # Create a dictionary of API details
        api_details = {
            "api_key": api_key,
            "board_id": board_id,
            "url": getURL,
            "headers": headers
        }
        # Make the GET request to Miro API
        response = super().get(self, url=getURL, headers=headers)
        if response.status_code == 200:
            return self.__parse_miro_response(response.json()["data"])
        
        # Hanlde the response, and any errors if is not successful
        super().getHttpError(response, api_details)
        
    def __parse_miro_response(self, response):
        sitcky_notes = [item for item in response if item["type"] == "sticky_note"]
        return [note["data"]["content"] for note in sitcky_notes]
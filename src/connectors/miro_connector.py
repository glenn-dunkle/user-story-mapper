# import requests
import re
import uuid
import urllib.parse
from src.util.http_helper import HTTPHelper
from src.util.config_helper import CONFIG

class MiroConnector(HTTPHelper):
    def __init__(self):
        # Load configuration values from the config file
        self.uuid = str(uuid.uuid4())
        super().__init__(f"miro_conn_{self.uuid}")
        self.api_key = CONFIG["miro"]["MIRO_API_KEY"]
        self.base_url = CONFIG["miro"]["MIRO_BASE_URL"]
        self.board_id = CONFIG["miro"]["MIRO_BOARD_ID"]
        self.page_item_limit = CONFIG["miro"]["MIRO_PAGE_ITEMS"]
        self.http_accept = CONFIG["miro"]["MIRO_HTTP_ACCEPT"]
        self.http_content_type = CONFIG["miro"]["MIRO_HTTP_CONTENT_TYPE"]

    def __remove_html_tags(self, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

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
        url = f"{base_url}{board_id}/items"
        headers = { "Authorization": f"Bearer {api_key}" }
        params = { "limit": self.page_item_limit }

        # Create a dictionary of API details
        api_details = {
            "api_key": api_key,
            "board_id": board_id,
            "url": url,
            "headers": headers,
            "params" : params
        }
        # Make the GET request to Miro API
        response = super().get(self, url=url, headers=headers, params=params)

        # TODO: Miro returns cursor based pagination. Add handling for tha
#        response = super().get_paginated_with_cursor(url, headers, params)
        if response.status_code == 200:
            return self.__parse_miro_response(response.json()["data"])
        
        # Hanlde the response, and any errors if is not successful
        super().getHttpError(response, api_details)
        
    def __parse_miro_response(self, response):
        sitcky_notes = [item for item in response if item["type"] == "sticky_note"]
        return [self.__remove_html_tags(note["data"]["content"]) for note in sitcky_notes]
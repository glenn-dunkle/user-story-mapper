import uuid
import re
import urllib.parse
from src.util.http_helper import HTTPHelper
from src.util.config_helper import CONFIG

class MiroConnector(HTTPHelper):
    def __init__(self):
        # Load configuration values from the config file
        self.uuid = str(uuid.uuid4())
        super().__init__(f"miro_{self.uuid}")
        self.api_key = CONFIG["credentials"]["MIRO_API_KEY"]
        self.base_url = CONFIG["miro"]["MIRO_BASE_URL"]
        self.board_id = CONFIG["miro"]["MIRO_BOARD_ID"]
        self.http_accept = CONFIG["miro"]["MIRO_HTTP_ACCEPT"]
        self.http_content_type = CONFIG["miro"]["MIRO_HTTP_CONTENT_TYPE"]
        self.result_limit = CONFIG["miro"]["MIRO_RESULT_LIMIT"]
    
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
        params = { "limit": self.result_limit }

        # Create a dictionary of API details
 #       api_details = {
 #           "api_key": api_key,
 #           "board_id": board_id,
 #           "url": url,
 #           "headers": headers
##            "params": params
 #       }
        # Make the GET request to Miro API which uses first/prior/next/last full URL
        try:
            response = super().get_paginated(self,
                            url=url,
                            headers=headers,
                            params=params)
         
            if response:
              return self.__parse_miro_response(response)
        except Exception as e:
            self.logger.error(f"Error fetching Miro board: {str(e)}")
            return None
     
    def __parse_miro_response(self, response):
        try:
            if not response:
                raise ValueError("Empty response from Miro API")
            
            sticky_notes = [item for item in response if item["type"] == "sticky_note"]
            if not sticky_notes:
                raise ValueError("No sticky notes found in Miro board")
            
            return [self.__remove_html_tags(note["data"]["content"]) for note in sticky_notes]
        except Exception as e:
            self.logger.error(f"Error parsing Miro response: {str(e)}")
            raise e
    
    def __remove_html_tags(self, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
   
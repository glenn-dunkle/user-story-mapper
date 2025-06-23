import requests
import time
import urllib.parse
from .config_helper import CONFIG
from typing import Optional, Dict, Any, List, Union

# TODO: abstract hardcoded values
# TODO: add retry logic based on https://tinyurl.com/yck3tn2f
class HTTPHelper: 
    def __init__(self, name):
        self.name = name
        self.timeout = CONFIG['http']['HTTP_TIMEOUT']
        
    @staticmethod
    def get(self,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            timeout: Optional[int] = None) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        if params:
                params = urllib.parse.quote(params, safe='/')

        response = requests.get(url, headers=headers, params=params, timeout=effective_timeout)
        response.raise_for_status()
        return response
    
    @staticmethod
    def post(self,
             url: str,
             data: Optional[Any] = None,
             json: Optional[Any] = None,
             headers: Optional[Dict[str, str]] = None,
             timeout: Optional[int] = None) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout

        response = requests.post(url, data=data, json=json, headers=headers, timeout=effective_timeout)
        response.raise_for_status()
        return response

    @staticmethod
    def put(self,
            url: str,
            data: Optional[Any] = None,
            json: Optional[Any] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout

        response = requests.put(url, data=data, json=json, headers=headers, timeout=effective_timeout)
        response.raise_for_status()
        return response

    @staticmethod
    def delete(self,
               url: str,
               headers: Optional[Dict[str, str]] = None,
               timeout: Optional[int] = None) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout

        response = requests.delete(url, headers=headers, timeout=effective_timeout)
        response.raise_for_status()
        return response
    
    @staticmethod
    def patch(self,
              url: str,
              data: Optional[Any] = None,
              json: Optional[Any] = None,
              headers: Optional[Dict[str, str]] = None,
              timeout: Optional[int] = None) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        response = requests.patch(url, data=data, json=json, headers=headers, timeout=effective_timeout)
        response.raise_for_status()
        return response
    
    @staticmethod
    def get_paginated(self,
                      url: str,
                      headers: Optional[Dict[str, str]] = None,
                      params: Optional[Dict[str, Any]] = None,
                      timeout: Optional[int] = None,
                      next_key: str = "next",
                      results_key: str = "data") -> List[Any]:
        effective_timeout = timeout if timeout is not None else self.timeout
        results = []
        while True:
            response = requests.get(url, headers=headers, params=params, timeout=effective_timeout)
            response.raise_for_status()
            data = response.json()
            results.extend(data.get(results_key, []))
            next_url = data.get(next_key)
            if not next_url:
                break
            url = next_url
            params = None  # Assume next_url is a full URL
        return results 
    
    @staticmethod
    def get_paginated_with_cursor(self,
                                   url: str,
                                   headers: Optional[Dict[str, str]] = None,
                                   params: Optional[Dict[str, Any]] = None,
                                   timeout: Optional[int] = None,
                                   cursor_key: str = "cursor",
                                   results_key: str = "data") -> List[Any]:
        effective_timeout = timeout if timeout is not None else self.timeout
        results = []
        cursor = None
        while True:
            if cursor:
                params[cursor_key] = cursor
            response = requests.get(url, headers=headers, params=params, timeout=effective_timeout)
            response.raise_for_status()
            data = response.json()
            results.extend(data.get(results_key, []))
            cursor = data.get(cursor_key)
            if not cursor:
                break
            # Reset params to avoid sending the cursor in the next request
            params = {k: v for k, v in params.items() if k != cursor_key}    

    @staticmethod
    def get_with_retry(self,
                       url: str,
                       headers: Optional[Dict[str, str]] = None,
                       params: Optional[Dict[str, Any]] = None,
                       timeout: Optional[int] = None,
                       retries: int = 3,
                       backoff_factor: float = 0.3) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=effective_timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise e
    
    @staticmethod
    def post_with_retry(self,
                        url: str,
                        data: Optional[Any] = None,
                        json: Optional[Any] = None,
                        headers: Optional[Dict[str, str]] = None,
                        timeout: Optional[int] = None,
                        retries: int = 3,
                        backoff_factor: float = 0.3) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        for attempt in range(retries):
            try:
                response = requests.post(url, data=data, json=json, headers=headers, timeout=effective_timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise e
    
    @staticmethod
    def put_with_retry(self,
                       url: str,
                       data: Optional[Any] = None,
                       json: Optional[Any] = None,
                       headers: Optional[Dict[str, str]] = None,
                       timeout: Optional[int] = None,
                       retries: int = 3,
                       backoff_factor: float = 0.3) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        for attempt in range(retries):
            try:
                response = requests.put(url, data=data, json=json, headers=headers, timeout=effective_timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise e
                
    @staticmethod
    def delete_with_retry(self,
                          url: str,
                          headers: Optional[Dict[str, str]] = None,
                          timeout: Optional[int] = None,
                          retries: int = 3,
                          backoff_factor: float = 0.3) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        for attempt in range(retries):
            try:
                response = requests.delete(url, headers=headers, timeout=effective_timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise e
                
    @staticmethod
    def patch_with_retry(self,
                         url: str,
                         data: Optional[Any] = None,
                         json: Optional[Any] = None,
                         headers: Optional[Dict[str, str]] = None,
                         timeout: Optional[int] = None,
                         retries: int = 3,
                         backoff_factor: float = 0.3) -> requests.Response:
        effective_timeout = timeout if timeout is not None else self.timeout
        for attempt in range(retries):
            try:
                response = requests.patch(url, data=data, json=json, headers=headers, timeout=effective_timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise e
    
    @staticmethod
    def getHTTPErrorMessage(self,
                            response: requests.Response,
                            params: Optional[Dict[str, Any]] = None) -> str:
        if response.status_code == 400:
            return f"Bad Request: {response.text} with params {param_items}"
        elif response.status_code == 401:
            header_info = ""
            if params and "headers" in params and isinstance(params["headers"], dict):
                header_info = f" (header: {params['headers']})"
            return f"Unauthorized: Invalid API key or token.{header_info}"
        elif response.status_code == 403:
            url_info = ""
            if params and "url" in params and isinstance[params["url"], dict]:
                url_info = f" (url: {params['url']})"
            return f"Forbidden: You do not have permission to access this resource. {url_info}"
        elif response.status_code == 404:
            url_info = ""
            if params and "url" in params and isinstance[params["url"], dict]:
                url_info = f" (url: {params['url']})"
            return f"Not Found: The requested resource could not be found at {url_info}."
        elif response.status_code == 429:
            url_info = ""
            if params and "url" in params and isinstance[params["url"], dict]:
                url_info = f" (url: {params['url']})"
            return f"Too Many Requests: Rate limit exceeded. Please try again later. {url_info}"
        else:
            param_items = ", ".join([f"{k}={v}" for k, v in (params or {}).items()])
            return f"{response.status_code} {response.reason} {param_items}"
                       
    @staticmethod
    def test_connection(self,
                        url: str,
                        headers: Optional[Dict[str, str]] = None,
                        timeout: Optional[int] = None) -> bool:
        effective_timeout = timeout if timeout is not None else self.timeout

        try:
            response = requests.get(url, headers=headers, timeout=effective_timeout)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False
        

""" Classes OMDBApi ver.1 and ver.2"""
import requests
import ast
from typing import Optional, List


class OMDBApi:
    """ Class OMDBApi ver.1"""

    def __init__(self, api_key):
        """ Class initialization function """
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"

    def _images_path(self, title: str) -> Optional[str]:
        """ Get titles. Return path to poster for film"""
        response = requests.get(f"{self.url}/?apikey={self.api_key}&t={title}")
        if (ast.literal_eval(response.text)['Response'] == 'True'):
            imdbID = ast.literal_eval(response.text)['imdbID']
            url = f"{self.url.replace('www', 'img')}/?apikey={self.api_key}&i={imdbID}"
            if requests.get(url).status_code == 200:
                return url

    def get_posters(self, titles: List[str]) -> List[str]:
        """ Get list of titles. Return posters path's for films"""
        posters = []
        for title in titles:
            path = self._images_path(title)
            if path:  # If image isn`t exist
                posters.append(path)
            else:
                posters.append('assets/none.jpeg')  # Add plug

        return posters

""" Classes OMDBApi ver.1 and ver.2"""
import requests
import ast
from typing import Optional, List


class OMDBApi2:

    def __init__(self, api_key):
        """ Class initialization function"""
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"

    def _images_path(self, title: str, year: str) -> Optional[str]:
        """ Get title and year of film. Return path to poster of film."""
        # print(title, year)
        response = requests.get(self.url, {'apikey': self.api_key,
                                           't': title, 'y': year})
        # print(response.url)
        # print(response.text, response.json()['Response'])
        if response.json()['Response'] == 'False':
            response = requests.get(self.url, {'apikey': self.api_key,
                                               't': title, 'y': ''})
            # print(response.url)
            # print(response.text, response.json()['Response'])
        resp = ast.literal_eval(response.text)
        if response.status_code == 200 and resp['Response'] == 'True':
            imdbID = ast.literal_eval(response.text)['imdbID']
            # print(imdbID)
            url = f"{self.url.replace('www', 'img')}/?apikey={self.api_key}&i={imdbID}"
            if requests.get(url).status_code == 200:
                return url
            elif len(resp['Poster']) > 0:
                return resp['Poster']

    def get_posters(self, titles: str) -> List[str]:
        """ Get list of tuple: (title, year) of films.
            Return list of path to films posters"""
        # print(titles)
        posters = []
        for title in titles:
            path = self._images_path(title[:-7], title[-5:-1])
            if path:  # If image isn`t exist
                # print(path)
                posters.append(path)
            else:
                posters.append('assets/none.jpeg')  # Add plug

        return posters

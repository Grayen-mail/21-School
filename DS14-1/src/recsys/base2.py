""" Module to work with data ver.2.0"""
from typing import List, Set, AnyStr
import streamlit as st
import pandas as pd
from .utils import parse
from dataclasses import dataclass
from dataclasses import field
import ast


@dataclass
class Film_info:
    id:         int = 0
    title:      str = "Unknown"
    keywords:   str = "Unknown"
    year:       int = 0
    genre:      str = "Unknown"
    director:   str = "Unknown"
    sim:        float = 0.0
    ratio:      float = 0.0


@st.cache_data
def _load_distance(path: str, index_col: str = 'id') -> pd.DataFrame:
    """Load distance CSV file to pandas.DataFrame"""
    db = pd.read_csv(path, index_col=index_col)
    db.index = db.index.astype(int)
    db.columns = db.columns.astype(int)
    return db


@st.cache_data
def _load_movies(path: str, index_col: str = 'id') -> pd.DataFrame:
    """Load movie CSV file to pandas.DataFrame"""
    db = pd.read_csv(path, index_col=index_col)
    db.index = db.index.astype(int)
    db['genres'] = db['genres'].apply(parse)
    db['years'] = pd.DatetimeIndex(
        db.release_date).year.fillna(0).astype(int)
    db['title_year'] = db['title'] + ' ('+db['years'].astype(str)+')'
    db['director'] = db['crew'].apply(lambda x: "".join(
        [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director']))
    db['actors'] = db['cast'].apply(parse)
    return db


class ContentBaseRecSys2:
    """Work with data class ver.2.0"""

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        """ Class init function. Load similarity matrix."""
        self.distance_all = _load_distance(distance_filepath, index_col='id')
        self.distance = self.distance_all
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        """ Load movies db"""
        self.movies_all = _load_movies(movies_dataset_filepath, index_col='id')
        self.movies = self.movies_all

    def get_titles(self) -> List[str]:
        """ Return titles of all films as list"""
        # title = self.movies_all['title'].values
        return self.movies_all['title_year'].values

    def get_genres(self) -> Set[str]:
        """ Return set of films genres"""
        genres = [item for sublist in self.movies_all['genres'].values.tolist()
                  for item in sublist]
        return set(genres)

    def get_years(self) -> Set[str]:
        """ Return set of films year of production"""
        return set(self.movies_all.years)

    def get_film_id(self, title_year: str) -> int:
        """ Return film id"""
        # print('\n---Get film ID')
        # print(
        # title, self.movies_all.loc[self.movies_all.title == title].index[0])
        return self.movies_all.loc[self.movies_all.title_year == title_year].index[0]

    def get_film_year(self, id: int) -> int:
        """ Return film year"""
        return self.movies_all.loc[id].years

    def get_film_director(self, id: int) -> int:
        return self.movies_all.loc[id].director

    def get_film_actors(self, id: int) -> List[str]:
        return self.movies_all.loc[id].actors

    def get_film_genres(self, id: int) -> List[str]:
        return self.movies_all.loc[id].genres

    def get_similarity(self, id1: int, id2: int) -> AnyStr:
        return str(round(self.distance[id1][id2]*100))

    def get_film_title(self, id: int) -> AnyStr:
        return self.movies_all.loc[id].title

    def get_film_original_title(self, id: int) -> AnyStr:
        return self.movies_all.loc[id].original_title

    def get_film_overview(self, id: int) -> AnyStr:
        return self.movies_all.loc[id].overview

    def set_filter(self, year: int, genre: str) -> None:
        self.movies = self.movies_all
        if year:
            # movies rows filtered
            self.movies = self.movies.loc[self.movies.years == year]
        if genre:
            self.movies = self.movies.loc[self.movies.genres.apply(     # movies rows filtered
                lambda x: genre in x)]
        # distance rows filtered
        self.distance = self.distance.loc[self.movies.index]
        # distance columns filtered
        # self.distance = self.distance[[i for i in self.movies.index]]
        # print('\n---Filter is set---\n')
        # print('distance.shape', self.distance.shape)
        # print('movies.shape', self.movies.shape)

    def remove_filter(self) -> None:
        self.movies = self.movies_all
        self.distance = self.distance_all
        # print('\n---Filter removed---\n')
        # print('distance.shape', self.distance.shape)
        # print('movies.shape', self.movies.shape)

    def recommendation(self, title_year: str, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """
        # filtered = self.movies.genres
        indices = pd.Series(
            self.movies_all.index, index=self.movies_all['title_year'])
        # print('\n---indices :', indices)
        idx = indices[title_year]
        # print('\n---idx :', idx)
        sim_scores = list(enumerate(self.distance[idx]))
        # print('\n---self.distance[idx]', self.distance[idx])
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_k+1]
        movie_ind = [i[0] for i in sim_scores]
        # print('movie_ind :', movie_ind)
        return list(self.movies['title_year'].iloc[movie_ind])

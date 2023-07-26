""" ver.2 recomendayion system"""
import os

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.echo_expander import echo_expander
from dotenv import load_dotenv

from api import OMDBApi2
from recsys import ContentBaseRecSys2


TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi2(API_KEY)

recsys2 = ContentBaseRecSys2(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)
with st.sidebar:
    add_vertical_space(10)
    st.sidebar.write(
        """spinachg@student.21-school  
        Intensive Parallel  
        21 TGU_DS_0423  
        Tribe: Mercury  
        26.04.2023 - 08.08.2023""")

st.markdown(
    "<h1 style='text-align: center;'>Movie Recommender Service</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: left;'>The search is performed by the movie that you liked</h1>",
    unsafe_allow_html=True
)

selected_movie = None

selected_movie = selectbox(
    "Type or select a movie you like :",
    recsys2.get_titles(),
    no_selection_label='---'
)

if selected_movie:
    # print(selected_movie[-5:-1])
    col1, col2 = st.columns([1, 4])
    film_id = recsys2.get_film_id(selected_movie)
    with col2:
        st.markdown("**Original name** : " +
                    recsys2.get_film_original_title(
                        recsys2.get_film_id(selected_movie)) + "<br>" +
                    # "**Year of prodaction** : " +
                    # str(recsys.get_film_year(film_id)) + "<br>" +
                    "**Director** : " +
                    recsys2.get_film_director(film_id) + "<br>" +
                    "**Genres** : " + ", ".join(recsys2.get_film_genres(film_id)) + "<br>" +
                    "**Overview** : " + recsys2.get_film_overview(film_id),
                    unsafe_allow_html=True)
        with st.expander('Show actors'):
            st.markdown(
                "**Actors** : " +
                ", ".join(recsys2.get_film_actors(film_id)) + "<br>",
                unsafe_allow_html=True, help='Show actors')

    with col1:
        st.image(omdbapi.get_posters([selected_movie]),
                 use_column_width=True)

st.markdown("""---""")

st.markdown("""By default, the search is performed in all records.
            To limit the search, you can choose the <strong>year</strong> or 
            <strong>genre</strong> of the desired movie. 
            For example: if you choose the genre "fantasy", the search will be 
            performed only on films with the tag "fantasy", even if the movie you 
            like is not.""", unsafe_allow_html=True)

#    filter_col = st.columns([2,3,2])
filter_col = st.columns([3, 3])
with filter_col[0]:
    selected_genre = selectbox(
        "Type or select a genre :",
        recsys2.get_genres(),
        no_selection_label='All genres'
    )

with filter_col[1]:
    selected_year = selectbox(
        "Type or select a year of prodaction :",
        recsys2.get_years(),
        no_selection_label='All years'
    )

#    with filter_col[2]:
#        min_rating = st.slider(
#            "Select minimal film ratio", 0.0, 10.0, 5.0
#        )

if selected_year or selected_genre:
    recsys2.set_filter(selected_year, selected_genre)
else:
    recsys2.remove_filter()

st.markdown("""If you have chosen everything you wanted, click the button
            and let's see which films we recommend for your viewing""",
            unsafe_allow_html=True)

st.divider()

btn_col = st.columns(2)

with btn_col[0]:
    btn_pressed = st.button('Show Recommendation')
with btn_col[1]:
    mode = st.radio("Select the display mode", ('Vertical', 'Horizontal'))
    # btn = btn

# print(btn)

if btn_pressed:  # If button pressed
    if selected_movie:  # If moview selected
        recommended_movie_names = recsys2.recommendation(
            selected_movie, top_k=TOP_K)
        if len(recommended_movie_names) == 0:
            st.write("""There are no recommendations for your choice. 
                    Please unselect genre or year.""")
        else:
            if mode == 'Vertical':
                st.subheader("Recommended Movies:")
                # print('\n---Recomended films---', recommended_movie_names)
                # titles = [recsys2.get_film_original_title(
                #        recsys2.get_film_id(name)
                #        ) for name in recommended_movie_names]
                recommended_movie_posters = omdbapi.get_posters(
                    recommended_movie_names)
                # movies_col = st.columns(len(recommended_movie_names))
                movies_col = st.columns(TOP_K)
                for index, col in enumerate(movies_col):
                    if index == len(recommended_movie_names):
                        break
                    with col:
                        st.image(
                            recommended_movie_posters[index],
                            use_column_width=True,
                        )
                        # st.subheader(recommended_movie_names[index])
                movies_col = st.columns(TOP_K)
                for index, col in enumerate(movies_col):
                    if index == len(recommended_movie_names):
                        break
                    with col:
                        st.markdown("<h3 style='text-align: center;'>" +
                                    recommended_movie_names[index]+"</h3>",
                                    unsafe_allow_html=True)
                        # print('\n---Movie name :', recommended_movie_names[index])
                        rec_id = recsys2.get_film_id(
                            recommended_movie_names[index])
                        # print('Film id : ', id)
                        # print(id)
                        st.markdown(
                            "<p style='text-align: center;'><strong>" +
                            # "Year of prodaction:</strong><br>" +
                            # str(recsys2.get_film_year(rec_id))+"<br>" +
                            "<strong>Director</strong> : <br>" +
                            recsys2.get_film_director(rec_id) + "<br>" +
                            "<strong>Genre:</strong><br>" +
                            ", ".join(
                                recsys2.get_film_genres(rec_id))+"</p>",
                            unsafe_allow_html=True)
                        st.markdown(
                            "<p style='text-align: center;'><strong>Similarity:<br>" +
                            recsys2.get_similarity(
                                film_id, rec_id) + "%</strong></p>",
                            unsafe_allow_html=True
                        )
            else:
                st.subheader("Recommended Movies:")
                recommended_movie_posters = omdbapi.get_posters(
                    recommended_movie_names)
                for index, title in enumerate(recommended_movie_names):
                    cont = st.container()
                    col1, col2 = cont.columns([1, 4])
                    with col1:
                        st.image(
                            recommended_movie_posters[index],
                            use_column_width=True,
                        )
                    with col2:
                        st.markdown("<h3 style='text-align: left;'>" +
                                    title+"</h3>",
                                    unsafe_allow_html=True)
                        # print('\n---Movie name :', title)
                        rec_id = recsys2.get_film_id(title)
                        # print('Film id : ', id)
                        # print(id)
                        st.markdown(
                            "<strong>Original title : </strong>" +
                            recsys2.get_film_original_title(rec_id) + "<br>" +
                            "**Director** : " +
                            recsys2.get_film_director(rec_id) + "<br>" +
                            "**Genres** : " +
                            ", ".join(recsys2.get_film_genres(rec_id)) + "<br>" +
                            "**Overview** : " +
                            recsys2.get_film_overview(rec_id) + "<br>" +
                            "<strong>Similarity:" +
                            recsys2.get_similarity(
                                film_id, rec_id) + "%</strong></p>",
                            unsafe_allow_html=True
                        )
                        with st.expander('Show actors'):
                            st.markdown(
                                "**Actors** : " +
                                ", ".join(recsys2.get_film_actors(
                                    rec_id)) + "<br>",
                                unsafe_allow_html=True, help='Show actors')
    else:
        st.write('Sorry. Please select movie first.')

# st.write('''Not implemented yet. May be later...
#        In the plans:
#        It was in version 1:
#        - Implemented a recommendation algorithm based on the description
#        of the movie (`overview`) and keywords for the movie (`keywords`).
#        - The Tf-Idf matrix for the description of the film is calculated.
#        - Calculated "cosine similarity" between films.''')
# st.write('''Planned in version 2:
#        - Implementation of an additional SVG algorithm.
#        - Choice: Algorithm 1, Algorithm 2, both with a slider of importance
#        in between.
#        Hmm... Sliders... Movie sliders... Ratio sliders... Year slider...
#        May be...''')

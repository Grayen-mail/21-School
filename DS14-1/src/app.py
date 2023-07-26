""" Main module """
import os

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.echo_expander import echo_expander
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys


TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)

recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)

# ver = st.sidebar.radio("Select version", ('ver. 1', 'ver. 2'))
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
    recsys.get_titles()
)

if selected_movie:
    col1, col2 = st.columns([1, 4])
    film_id = recsys.get_film_id(selected_movie)
    with col2:
        st.markdown("**Selected film** : " +
                    selected_movie + "<br>" +
                    "**Director** : " +
                    recsys.get_film_director(film_id) + "<br>" +
                    "**Genres** : " + ", ".join(recsys.get_film_genres(film_id)) + "<br>" +
                    "**Overview** : " + recsys.get_film_overview(film_id),
                    unsafe_allow_html=True)

    with col1:
        st.image(omdbapi.get_posters([recsys.get_film_original_title(film_id)]),
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
        recsys.get_genres(),
        no_selection_label='All genres'
    )

with filter_col[1]:
    selected_year = selectbox(
        "Type or select a year of prodaction :",
        recsys.get_years(),
        no_selection_label='All years'
    )

if selected_year or selected_genre:
    recsys.set_filter(selected_year, selected_genre)
else:
    recsys.remove_filter()

st.markdown("""If you have choosen everything you wanted, click the button
            and let's see which films we recommend for your viewing""",
            unsafe_allow_html=True)

st.divider()

btn_pressed = st.button('Show Recommendation')

# print(btn)

if btn_pressed:  # If button pressed
    if selected_movie:  # If moview selected
        recommended_movie_names = recsys.recommendation(
            selected_movie, top_k=TOP_K)
        if len(recommended_movie_names) == 0:
            st.write("""There are no recommendations for your choice. 
                    Please unselect genre or year.""")
        else:
            st.subheader("Recommended Movies:")
            # print('\n---Recomended films---', recommended_movie_names)
            titles = [recsys.get_film_original_title(
                recsys.get_film_id(name)
            ) for name in recommended_movie_names]
            recommended_movie_posters = omdbapi.get_posters(titles)
            movies_col = st.columns(len(recommended_movie_names))
            for index, col in enumerate(movies_col):
                with col:
                    st.image(
                        recommended_movie_posters[index],
                        use_column_width=True,
                    )
            movies_col = st.columns(len(recommended_movie_names))
            for index, col in enumerate(movies_col):
                with col:
                    st.markdown("<h3 style='text-align: center;'>" +
                                recommended_movie_names[index]+"</h3>",
                                unsafe_allow_html=True)
                    # print('\n---Movie name :', recommended_movie_names[index])
                    rec_id = recsys.get_film_id(
                        recommended_movie_names[index])
                    # print('Film id : ', id)
                    # print(id)
                    st.markdown(
                        "<p style='text-align: center;'><strong>" +
                        "Year of prodaction:</strong><br>" +
                        str(recsys.get_film_year(rec_id))+"<br>" +
                        "<strong>Director</strong> : <br>" +
                        recsys.get_film_director(film_id) + "<br>" +
                        "<strong>Genre:</strong><br>" +
                        ", ".join(
                            recsys.get_film_genres(rec_id))+"</p>",
                        unsafe_allow_html=True)
                    st.markdown(
                        "<p style='text-align: center;'><strong>Similarity:<br>" +
                        recsys.get_similarity(recsys.get_film_id(
                            selected_movie), rec_id) + "%</strong></p>",
                        unsafe_allow_html=True
                    )

    else:
        st.write('Sorry. Please select movie first.')

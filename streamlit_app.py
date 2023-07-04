import pickle
import streamlit as st
import requests
import pandas as pd

# Function to fetch movie poster URL
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page title and sidebar heading
st.set_page_config(page_title='Movie Recommendation', layout='wide')
st.markdown(
    """
    <style>
    .title-text {
        margin-top:0px;
        color: #FF5733; /* Coral */
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .sidebar-text {
        color: #EFA18A;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .recommend-button {
        background-color: #00FF00;
        color: #EFA18A;
        padding: 10px 20px;
        font-size: 18px;
        border: none;
        border-radius: 5px;
        margin-top: 10px;
    }
    .recommend-button:hover {
        background-color: #00CC00;
    }
    .movie-name {
        color: #EFA18A;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title and sidebar heading
st.markdown('<p class="title-text">🍿 Movie Recommendation</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-text">🎥 Select a Movie</p>', unsafe_allow_html=True)

# Movie selection dropdown
selected_movie_name = st.sidebar.selectbox('Choose a movie', movies['title'].values)

# Recommendation button
if st.sidebar.button('🔍Recommend', key='recommend-button', help='Click to get movie recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display recommended movies and posters in columns
    with col1:
        st.markdown('<p class="movie-name">{}</p>'.format(recommended_movie_names[0]), unsafe_allow_html=True)
        st.image(recommended_movie_posters[0], use_column_width=True)

    with col2:
        st.markdown('<p class="movie-name">{}</p>'.format(recommended_movie_names[1]), unsafe_allow_html=True)
        st.image(recommended_movie_posters[1], use_column_width=True)

    with col3:
        st.markdown('<p class="movie-name">{}</p>'.format(recommended_movie_names[2]), unsafe_allow_html=True)
        st.image(recommended_movie_posters[2], use_column_width=True)

    with col4:
        st.markdown('<p class="movie-name">{}</p>'.format(recommended_movie_names[3]), unsafe_allow_html=True)
        st.image(recommended_movie_posters[3], use_column_width=True)

    with col5:
        st.markdown('<p class="movie-name">{}</p>'.format(recommended_movie_names[4]), unsafe_allow_html=True)
        st.image(recommended_movie_posters[4], use_column_width=True)

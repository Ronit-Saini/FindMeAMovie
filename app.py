import pickle 
import streamlit as st
import requests
import random

# CSS for background image and content area styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSZiSszIyi0XvkdWUf31oJ0nobjeSn3BYolw&s");
    background-size: 50%;
}

[data-testid="stToolbar"] {
    right: 2rem;
}

body {
    color: white;  /* Set text color to white */
}

.scrollable {
    max-width: 100px;  /* Set a maximum width */
    overflow-x: auto;  /* Enable horizontal scrolling */
    white-space: nowrap;  /* Prevent text from wrapping */
    padding: 0.5rem;  /* Add padding */
    color: white;  /* Set text color to white */
    border-radius: 5px;  /* Optional: add rounded corners */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7eefcd74ca3e3e497ad1b2327738464".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

# Define CSS to import Google Font (Oswald) and apply dark yellow color
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald&display=swap');

    h1 {
        font-family: 'Oswald', sans-serif;  /* Apply Oswald font */
        font-weight: 400;  /* Regular weight */
        color: #b8860b;  /* Dark yellow color */
        text-align: center;  /* Center align text */
        margin-bottom: 20px;  /* Add margin bottom */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main heading with Oswald font and dark yellow color, centered
st.markdown('<h1>Find Your Movie Match !!</h1>', unsafe_allow_html=True)
st.write("")  # Adds a space after the heading

# Loading the dumped pickle files into variables
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Store names of movies in movie_list variable and then showcase it
movie_list = movies['title'].values

# Generate random movies to display at the top
st.subheader('Hey there, care to try these?')  # Change text color as requested
st.write("")  # Adds space after the subheader

random_movies = random.sample(list(movie_list), 5)

# Display the random movies with black background for names
cols = st.columns(5)
for idx, col in enumerate(cols):
    with col:
        movie_name = random_movies[idx]
        movie_id = movies[movies['title'] == movie_name].iloc[0].movie_id
        st.markdown(f'<div class="scrollable">{movie_name}</div>', unsafe_allow_html=True)
        st.image(fetch_poster(movie_id))

st.write("")  # Adds space after the subheader
st.write("")  # Adds space after the heading
st.write("")  # Adds space after the heading
st.write("")  # Adds space after the heading

st.subheader('No? Well I have got you covered!')  # Change text color as requested
st.write("")  # Adds space after the subheader
st.write("")  # Adds space after the subheader

# Select movie dropdown
selected_movie = st.selectbox(
    'Select or type in a movie name',
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with eval(f"col{i+1}"):
            st.markdown(f'<div class="scrollable">{recommended_movies_name[i]}</div>', unsafe_allow_html=True)
            st.image(recommended_movies_poster[i])

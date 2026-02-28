import streamlit as st
import pickle
import requests
import os
from dotenv import load_dotenv

# ---------- Load ENV ----------
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# ---------- Load data ----------
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# ---------- Poster Fetch ----------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        pass

    # fallback image
    return "https://via.placeholder.com/500x750?text=No+Image"

# ---------- Recommendation ----------
def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    recommended_movies=[]
    recommended_posters=[]

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_posters

# ---------- UI ----------
st.set_page_config(page_title="Movie Recommender",layout="wide")

st.title("🎬 Movie Recommendation System")
st.write("Select a movie and get similar recommendations!")

selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

if st.button("Recommend 🎥"):

    names, posters = recommend(selected_movie)

    col1,col2,col3,col4,col5 = st.columns(5)

    cols=[col1,col2,col3,col4,col5]

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
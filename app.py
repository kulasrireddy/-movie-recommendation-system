import streamlit as st
import pickle
import pandas as pd
import requests

# ---------- Streamlit Setup ----------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# ---------- Google Drive File IDs ----------
MOVIES_FILE_ID = "1GOmXJxXTpLxmyBCr4f7PLRUjCRl7lagT"
SIMILARITY_FILE_ID = "1XmEKbwAh6fkF2PKZ8zhvIdaHtXpGxhPx"

# ---------- Function to download pickle files from Google Drive ----------
def load_pickle_from_gdrive(file_id, filename):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    with open(filename, "rb") as f:
        return pickle.load(f)

# ---------- Load Data ----------
movies = load_pickle_from_gdrive(MOVIES_FILE_ID, "movies.pkl")
similarity = load_pickle_from_gdrive(SIMILARITY_FILE_ID, "similarity.pkl")

# ---------- Recommendation Function ----------
def recommend(movie_name, n=5):
    if movie_name not in movies['title'].values:
        st.error("Movie not found!")
        return []
    
    idx = movies[movies['title'] == movie_name].index[0]
    distances = list(enumerate(similarity[idx]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)
    recommended_movies = [movies.iloc[i[0]]['title'] for i in distances[1:n+1]]
    return recommended_movies

# ---------- Streamlit Interface ----------
selected_movie = st.selectbox("Select a movie", movies['title'].values)
if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("You might also like:")
    for i, movie in enumerate(recommendations, 1):
        st.write(f"{i}. {movie}")

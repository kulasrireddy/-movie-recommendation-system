# app.py
import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Streamlit Setup ----------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# ---------- Load movies.pkl ----------
try:
    with open('movies.pkl','rb') as f:
        movies = pickle.load(f)
except FileNotFoundError:
    st.error("Please run model.py first to create movies.pkl")
    st.stop()

# ---------- Function to fetch poster ----------
def fetch_poster(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return None

# ---------- Recommendation Function ----------
def recommend(movie_name, n=5):
    if movie_name not in movies['title'].values:
        st.error("Movie not found!")
        return [], []

    # Compute similarity dynamically
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)

    idx = movies[movies['title'] == movie_name].index[0]
    distances = list(enumerate(similarity[idx]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommended_movies = [movies.iloc[i[0]]['title'] for i in distances[1:n+1]]
    recommended_posters = []
    if 'poster_path' in movies.columns:
        recommended_posters = [movies.iloc[i[0]]['poster_path'] for i in distances[1:n+1]]
    else:
        recommended_posters = [None]*n

    return recommended_movies, recommended_posters

# ---------- Streamlit Interface ----------
selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie)

    st.subheader("You might also like:")

    # Display recommendations horizontally
    cols = st.columns(len(recommendations))
    for col, title, poster in zip(cols, recommendations, posters):
        poster_url = fetch_poster(poster)
        if poster_url:
            col.image(poster_url, width=200, caption=title)
        else:
            col.write(title)

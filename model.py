# model.py
import pandas as pd
import ast
import pickle

# ---------- Load CSVs ----------
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

# Merge on title
movies = movies.merge(credits, on='title')

# Keep only required columns
columns_needed = ['id','title','overview','genres','keywords','cast','crew']
if 'poster_path' in movies.columns:
    columns_needed.append('poster_path')

movies = movies[columns_needed]
movies.dropna(inplace=True)

# ---------- Helper functions ----------
def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def fetch_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:3]]

def fetch_director(text):
    return [i['name'] for i in ast.literal_eval(text) if i['job']=='Director']

# Apply functions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(fetch_cast)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# ---------- Combine tags ----------
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# ---------- Convert list to string (CRUCIAL) ----------
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# ---------- Save pickle ----------
pickle.dump(movies, open('movies.pkl','wb'))
print("✅ movies.pkl created successfully!")

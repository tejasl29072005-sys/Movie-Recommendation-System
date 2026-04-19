import streamlit as st
import pandas as pd
import ast
import requests
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ================= DATA =================
@st.cache_data
def load_data():
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')

    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

    def convert(x):
        return [i['name'] for i in ast.literal_eval(x)]

    def convert_cast(x):
        return [i['name'] for i in ast.literal_eval(x)[:3]]

    def fetch_director(x):
        for i in ast.literal_eval(x):
            if i['job'] == 'Director':
                return [i['name']]
        return []

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)

    for col in ['genres','keywords','cast','crew']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ","") for i in x])

    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    new_df = movies[['movie_id','title','tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

    return new_df

new_df = load_data()

# ================= MODEL =================
@st.cache_resource
def create_similarity(data):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(data['tags']).toarray()
    return cosine_similarity(vectors)

similarity = create_similarity(new_df)

# ================= TMDB =================
API_KEY = "abc7fc65db6b31ef33a5398702552afb"  # 🔥 replace

def fetch_poster(movie_id, movie_name):
    try:
        # 🔹 Try ID first
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url, timeout=5).json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        # 🔹 Fallback search
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": API_KEY, "query": movie_name}
        data = requests.get(search_url, params=params, timeout=5).json()

        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

# ================= RECOMMEND =================
def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    rec_movies, rec_posters, reasons = [], [], []

    for i in distances:
        movie_id = new_df.iloc[i[0]].movie_id
        title = new_df.iloc[i[0]].title

        rec_movies.append(title)
        rec_posters.append(fetch_poster(movie_id, title))

        # better explanation
        reasons.append(f"🧠 Similar themes, genres & cast (score: {round(i[1],2)})")

        time.sleep(0.2)

    return rec_movies, rec_posters, reasons

# ================= UI =================
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommendation System")
st.markdown("### 🎯 Find movies similar to your favorites")

selected_movie = st.selectbox("Search Movie", new_df['title'].values)

if st.button("Recommend"):
    names, posters, reasons = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.subheader(names[i])
            st.caption(reasons[i])

            col1, col2 = st.columns(2)

            with col1:
                if st.button("👍", key=f"like{i}"):
                    st.success("Liked!")

            with col2:
                if st.button("👎", key=f"dislike{i}"):
                    st.warning("Noted!")
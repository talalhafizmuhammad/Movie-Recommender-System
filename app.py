import pickle
import joblib # type: ignore
import streamlit as st  # type: ignore
import requests  # type: ignore

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    
    title = data.get('title', 'Unknown Title')
    rating = data.get('vote_average', 'N/A')
    year = data.get('release_date', 'N/A')[:4] if data.get('release_date') else "N/A"
    
    return {
        "title": title,
        "poster": poster_url,
        "rating": rating,
        "year": year
    }

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)
        recommended_movies.append(movie_details)
    return recommended_movies

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .movie-card {
        transition: transform 0.3s, box-shadow 0.3s;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        text-align: center;
        background-color: #111;
        color: white;
        padding: 8px;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .movie-title {
        margin-top: 8px;
        font-size: 16px;
        font-weight: 600;
    }
    .movie-info {
        font-size: 14px;
        color: #bbb;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommender System 🍿</h1>", unsafe_allow_html=True)
st.write("")

movies = pickle.load(open('movies.pkl','rb'))
similarity = joblib.load("similarity_compressed.pkl")

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie:", movie_list)

if st.button('😎 Get Recommendations'):
    recommendations = recommend(selected_movie)
    
    cols = st.columns(5, gap="large")
    for idx, col in enumerate(cols):
        with col:
            movie = recommendations[idx]
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{movie['poster']}" width="100%" style="border-radius:10px;" />
                    <div class="movie-title">{movie['title']}</div>
                    <div class="movie-info">⭐ {movie['rating']} | 🎞️ {movie['year']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    cols = st.columns(5, gap="large")
    for idx, col in enumerate(cols):
        with col:
            movie = recommendations[idx+5]
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{movie['poster']}" width="100%" style="border-radius:10px;" />
                    <div class="movie-title">{movie['title']}</div>
                    <div class="movie-info">⭐ {movie['rating']} | 🎞️ {movie['year']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

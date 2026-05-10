'''
Author: Akash Navani
Email: akashnavani25@gmail.com
'''
import os
import pickle
import streamlit as st
import requests
import pandas as pd

# --- UI Customization ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main background and text */
        .stApp {
            background-color: #f7f9fc;
            color: #2b3035;
            font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Headers and titles */
        h1, h2, h3 {
            color: #1a1d20;
            font-weight: 700;
        }
        
        /* Center the main title */
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            color: #1a1d20;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
            padding-top: 2rem;
        }
        
        /* Subtitle/Tagline */
        .sub-title {
            text-align: center;
            font-size: 1.1rem;
            color: #6c757d;
            margin-bottom: 3rem;
            font-weight: 400;
        }
        
        /* Selectbox styling */
        .stSelectbox label {
            font-weight: 600;
            color: #495057;
        }
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 8px;
            border: 1px solid #ced4da;
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
        }
        .stSelectbox div[data-baseweb="select"]:hover {
            border-color: #aeb4ba;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            background-color: #2b3035;
            color: #ffffff;
            font-weight: 600;
            padding: 0.6rem 1rem;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            margin-top: 1.8rem;
        }
        .stButton > button:hover {
            background-color: #1a1d20;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
            color: #ffffff;
        }
        .stButton > button:active {
            transform: translateY(0);
            color: #ffffff;
        }
        
        /* Movie Card Container */
        .movie-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid #eef0f2;
            margin-bottom: 1rem;
        }
        .movie-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.1);
            border-color: #dde0e3;
        }
        
        /* Movie Image inside Card */
        .movie-card img {
            border-radius: 8px;
            width: 100%;
            object-fit: cover;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            aspect-ratio: 2/3;
        }
        
        /* Movie Title */
        .movie-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #2b3035;
            margin-bottom: 0.8rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 1.3;
            min-height: 2.6em;
        }
        
        /* Movie Meta (Year, Rating) */
        .movie-meta {
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: auto;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 0.8rem;
            border-top: 1px solid #f0f2f5;
        }
        
        .movie-rating {
            font-weight: 600;
            color: #f5c518; /* subtle yellow for rating */
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Spinner color */
        .stSpinner > div > div {
            border-top-color: #2b3035 !important;
        }
        
        /* Container padding adjustment */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
        }
        
        /* Success/Warning messages */
        .stAlert {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)


# --- API Keys ---
# Using environment variables for security, with fallback to default keys for local testing
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "trilogy")
PLACEHOLDER_POSTER = "https://placehold.co/500x750/eef0f2/6c757d?text=No+Poster+Available"


def _fetch_poster_tmdb(movie_id):
    """Attempt to fetch poster from TMDB (primary source)."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url, timeout=3)
    response.raise_for_status()
    poster_path = response.json().get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None


def _fetch_poster_omdb(movie_title, movie_year=None):
    """Attempt to fetch poster from OMDb (fallback source)."""
    params = {"t": movie_title, "apikey": OMDB_API_KEY}
    if movie_year and pd.notna(movie_year):
        params["y"] = int(movie_year)
    response = requests.get("http://www.omdbapi.com/", params=params, timeout=5)
    response.raise_for_status()
    poster_url = response.json().get("Poster")
    if poster_url and poster_url != "N/A":
        return poster_url
    return None


def fetch_poster(movie_id, movie_title="", movie_year=None):
    """Fetches poster via TMDB -> OMDb -> placeholder fallback."""
    try:
        poster = _fetch_poster_tmdb(movie_id)
        if poster:
            return poster
    except requests.exceptions.RequestException:
        pass

    try:
        poster = _fetch_poster_omdb(movie_title, movie_year)
        if poster:
            return poster
    except requests.exceptions.RequestException:
        pass

    return PLACEHOLDER_POSTER


def recommend(movie):
    """Recommends 5 similar movies based on the selected movie."""
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the dataset. Please select another one.")
        return [], [], [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_years = []
    recommended_movie_ratings = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        year = movies.iloc[i[0]].year
        recommended_movie_names.append(title)
        recommended_movie_years.append(year)
        recommended_movie_ratings.append(movies.iloc[i[0]].vote_average)
        recommended_movie_posters.append(fetch_poster(movie_id, title, year))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_years, recommended_movie_ratings

# --- Main App ---
st.set_page_config(
    page_title="Cinematch | Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styles()

# Hero Section
st.markdown("<div class='main-title'>Find Your Next Favorite Movie</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Discover personalized movie recommendations powered by machine learning.</div>", unsafe_allow_html=True)

# Load the data files
try:
    movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please run the data processing notebook first.")
    st.stop()

movie_list = movies['title'].values

# Search Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie = st.selectbox(
        "Search for a movie you like:",
        movie_list,
        index=0
    )
    
    analyze_button = st.button('Discover Similar Movies ✨', use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

if analyze_button:
    with st.spinner('Analyzing movie properties and finding the best matches...'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_years, recommended_movie_ratings = recommend(selected_movie)
    
    if recommended_movie_names:
        st.markdown(f"<h3 style='text-align: center; color: #495057; margin-bottom: 2rem;'>Top Picks inspired by <b>{selected_movie}</b></h3>", unsafe_allow_html=True)
        
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                year = recommended_movie_years[i]
                year_str = int(year) if pd.notna(year) else "N/A"
                rating = recommended_movie_ratings[i]
                card_html = f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[i]}" alt="{recommended_movie_names[i]} poster" />
                    <div class="movie-title">{recommended_movie_names[i]}</div>
                    <div class="movie-meta">
                        <span>📅 {year_str}</span>
                        <span class="movie-rating">★ {rating:.1f}</span>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

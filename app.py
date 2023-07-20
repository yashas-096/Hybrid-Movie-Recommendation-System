from interface_hybrid_recommendation_system_final import get_weighted_scores, get_Tmdb_id
import json
import requests
import csv
import os
tmdb_ids1 = [] 
error_ids1 = []


def _image_is_gif(pil_image):
    if pil_image is None:
        return False
    return bool(pil_image.format == "GIF")

def get_movie_poster(movie_name):
    Movie_ID = get_Tmdb_id(movie_name)
    query = 'https://api.themoviedb.org/3/movie/' + str(Movie_ID) + '?api_key=27b15482be4911927bf423c0350415c2'
    img = "https://image.tmdb.org/t/p/w185/"
    response = requests.get(query)
    if response.status_code == 200:
        # status code ==200 indicates the API query was successful
        array = response.json()
        text = json.dumps(array)
        dataset = json.loads(text)
        # print(dataset)
        try:
          poster = img + dataset['poster_path']
          return poster
        except:
          print("error")
    else:
        print("error getting response")

import streamlit as st
st.title('Movie Recommender')
movie_name = st.text_input("Enter a movie name:")
try:
    hybrid_recommendations = get_weighted_scores(movie_name,0.5,10)
    print(hybrid_recommendations)
    
except:
    print("error in get_weighted_scores")
if movie_name:
    # Display the movie posters for the top recommended movies
    st.header("Hybrid Recommendations:")
    show_top5 = st.button("Show Top 5 recommendations")
    show_top10 = st.button("Show Top 10 recommendations")
    if show_top5:
        st.header("Top 5 Hybrid Recommendations:")
        top_n = 5
        cols = st.columns(3)
        for i, movie in enumerate(hybrid_recommendations[:top_n]):
            poster_url = get_movie_poster(movie)
            with cols[i % 3]:
                st.write(f"{movie}")
                st.image(poster_url, width=200)
    
    if show_top10:
        st.header("Top 10 Hybrid Recommendations:")
        top_n = 10
        cols = st.columns(3)
        for i, movie in enumerate(hybrid_recommendations[:top_n]):
            poster_url = get_movie_poster(movie)
            with cols[i % 3]:
                st.write(f"{movie}")
                st.image(poster_url, width=200)

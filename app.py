import streamlit as st
import pickle
import pandas as pd
import requests




def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original/'+ data["poster_path"]


def recommend(movie):
    movie_index = Movies[Movies['title'] == movie].index[0]    #fetching the index of movie from data
    distances = Similarity[movie_index]   
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]  #fetching 5 movies of similarity
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = Movies.iloc[i[0]].movie_id

        
        recommended_movies.append(Movies.iloc[i[0]].title)

        #fetch the poster from api

        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters



Movies_dict = pickle.load(open("Movies_dict.pkl","rb"))
Movies = pd.DataFrame(Movies_dict)

Similarity = pickle.load(open("Similarity.pkl","rb"))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select Movie",
    Movies["title"].values
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
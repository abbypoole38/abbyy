import streamlit as st
import json
import pandas as pd

# NEW
def load_movie_data():
    with open("data.json", "r") as file:
        movies = json.load(file)
    return movies

# NEW
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = 'All'
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None


st.title("My Favorite Movies!")

# NEW
selected_genre = st.selectbox("Select a Movie Genre:", ['All', 'Rom-Com', 'Sci-Fi', 'Crime', 'Drama'])
st.session_state.selected_genre = selected_genre

movie_data = load_movie_data()

filtered_movies = []
for movie in movie_data:
    if selected_genre == 'All' or movie['Genre'] == selected_genre:
        filtered_movies.append(movie)

st.write("Filtered Movie Data:")

# Show details of filtered movies
for movie in filtered_movies:
    st.write("**Movie:**", movie['Movie'])
    st.write("**Genre:**", movie['Genre'])
    st.write("**Rating:**", movie['Rating'])
    st.write("**Description:**", movie['Description'])

# NEW
st.write("### Search for a Movie")

search_movie = st.text_input("Enter movie title to search:")
filtered_by_search = [movie for movie in movie_data if search_movie.lower() in movie['Movie'].lower()]

st.write("### Search Results")
for movie in filtered_by_search:
    st.write(f"**{movie['Movie']}** - Genre: {movie['Genre']}, Rating: {movie['Rating']}")

#NEW
st.write("### Dynamic Bar Chart")

x_axis_bar = st.selectbox("Select X-axis for Bar Chart (Movie):", ['Movie', 'Genre'])
y_axis_bar = st.selectbox("Select Y-axis for Bar Chart (Movie):", ['Rating'])

if x_axis_bar == 'Movie':
    x_data_bar = [movie['Movie'] for movie in movie_data]
else:
    x_data_bar = [movie['Genre'] for movie in movie_data]

if y_axis_bar == 'Rating':
    y_data_bar = [movie['Rating'] for movie in movie_data]

bar_data = pd.DataFrame({x_axis_bar: x_data_bar, y_axis_bar: y_data_bar})

st.write(f"### Bar Chart: {x_axis_bar} vs Rating")
st.bar_chart(bar_data.set_index(x_axis_bar))

#NEW
st.write("### Dynamic Bar Chart: Movie vs Budget/Duration")

x_axis_second = st.selectbox("Select X-axis for New Bar Chart:", ['Budget', 'Duration (hrs)'])
y_axis_second = 'Movie'

if x_axis_second == 'Budget (Millions)':
    x_data_second = [movie['Budget (Millions)'] for movie in movie_data]
else:
    x_data_second = [movie['Duration (hrs)'] for movie in movie_data]

y_data_second = [movie['Movie'] for movie in movie_data]

second_bar_data = pd.DataFrame({y_axis_second: y_data_second, x_axis_second: x_data_second})

st.write(f"### Bar Chart: {y_axis_second} vs {x_axis_second}")
st.bar_chart(second_bar_data.set_index(y_axis_second))

# NEW
st.write("### Static Bar Chart of All Movie Ratings")
all_movies = [movie['Movie'] for movie in movie_data]
all_ratings = [movie['Rating'] for movie in movie_data]
ratings_df = pd.DataFrame({'Rating': all_ratings}, index=all_movies)
st.bar_chart(ratings_df)

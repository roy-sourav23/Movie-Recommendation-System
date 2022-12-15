import pandas as pd
import audio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# loading datasets
movies_data = pd.read_parquet("parquet/movies.parquet", engine="fastparquet")

ratings_data = pd.read_parquet("parquet/ratings.parquet", engine="fastparquet")
    
links_data = pd.read_parquet("parquet/links.parquet", engine="fastparquet")

tags_data = pd.read_parquet("parquet/tags.parquet", engine="fastparquet")
 
# merge datasets
movie_ratings = pd.merge(movies_data, ratings_data, on="movieId")
movie_links = pd.merge(movies_data, links_data, on="movieId")
# merged_dataset = pd.merge(movie_links, movie_ratings)
movies_tags = pd.merge(movie_links, tags_data)

# get specific user data
def get_user_data(user_id):
    user_data = movie_ratings[movie_ratings["userId"] == user_id]
    return user_data

# most rated movies
def num_of_ratings():
    ratings = movie_ratings.groupby('title')['rating'].count().reset_index(name='no of ratings')   
    movie_ratings["no of ratings"] = pd.DataFrame(ratings["no of ratings"])  

    # fill up Nan Values
    movie_ratings["no of ratings"].fillna(0, inplace=True)
    # convert data types
    movie_ratings["no of ratings"] = movie_ratings["no of ratings"].astype(int)
    top_m = movie_ratings.sort_values('no of ratings', ascending=False)

    top_m = top_m[top_m["rating"] == 5.0]
    return  top_m[top_m["no of ratings"] > 20]

# get user top movie on specific genre from user 
def get_top_movie(user_id, genre):
    user_data = get_user_data(user_id)
    movie_ids = []
    for index, rows in user_data.iterrows():
        if rows["genres"] != '(no genres listed)':
            genres = rows["genres"].split('|')        
            if genre in genres:
                movie_ids.append(rows["movieId"])

    movie_list = user_data[user_data["movieId"].isin(movie_ids)].sort_values("rating", ascending=False)  
    return movie_list["title"].iloc[0]

# top rated movies from a specific genre
def top_rated_movies(genre) -> list:
    most_rated_movies = num_of_ratings()
    x= 0
    top_movie_ids = []
    for i, r in most_rated_movies.iterrows():
        s_genre = genre
        if x == 5:
            break
        elif r["genres"] != '(no genres listed)':
            genres = r["genres"].split('|')        
            if s_genre in genres:
                if r["movieId"] not in top_movie_ids:
                    top_movie_ids.append(r["movieId"])
                    x += 1
    return top_movie_ids

def main():
    print("Enter user id: ", end="")
    # user_id = int(input())
    # genre = audio.main()           
    user_id = 5
    genre = "Adventure"

    top_movie = get_top_movie(user_id, genre)

    selected_features = ["genres", "tag"] # title
    # replacing the null valuess with null string
    for feature in selected_features:
        movies_tags[feature] = movies_tags[feature].fillna("")

    # creating genre specific popularity list
    genre_list = []
    for index, row in movies_tags.iterrows():
        if genre in row["genres"]:
            genre_list.append(row["movieId"])
    
    combined_features = (
        movies_tags["genres"]
        + " "
        + movies_tags["tag"] 
        + " "
        + movies_tags["title"]

    )

    # converting text data to feature vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)

    id_of_the_movie = movie_ratings[(movie_ratings["title"] == top_movie)]["movieId"].iloc[0]
    # getting the similarity scores using cosine similarity
    similarity = cosine_similarity(feature_vectors)

    # getting a list of similar movies
    similarity_score = list(enumerate(similarity[id_of_the_movie]))

    # sorting the movies based on their similarity score
    sorted_similar_movies = sorted(
        similarity_score, key=lambda x: x[1], reverse=True)

    print("\nMovies suggested for you : ")
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        if index in genre_list:
            title_from_index = movies_data[movies_data.index == index]["title"].values[0]
            if i <= 5:
                print(i, ".", title_from_index)
                i += 1
    
    print(f"\nPopular {genre} Movies:")
    top_movie_ids = top_rated_movies(genre)
    z=1
    for i, r in movie_links.iterrows():
        if r["movieId"] in top_movie_ids:
            if z <= 5:
                print(f"{z}. ", r["title"])
                z += 1


main()






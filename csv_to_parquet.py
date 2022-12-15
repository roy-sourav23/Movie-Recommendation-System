import datetime
import pandas as pd

def convert_to_perquet():   
    t1 = datetime.datetime.now()

    with open('movie_dataset/movies.csv') as f1:
        movies_data = pd.read_csv(f1, engine="pyarrow")
    movies_data.to_parquet("parquet/movies.parquet", compression=None)

    with open('movie_dataset/ratings.csv') as f2:
        ratings_data = pd.read_csv(f2, engine="pyarrow")
    ratings_data.to_parquet("parquet/ratings.parquet", compression=None)

    with open('movie_dataset/links.csv') as f3:
        links_data = pd.read_csv(f3, engine="pyarrow")
    links_data.to_parquet("parquet/links.parquet", compression=None)

    with open('movie_dataset/tags.csv') as f4:
        tags_data = pd.read_csv(f4, engine="pyarrow")
    tags_data.to_parquet("parquet/tags.parquet", compression=None)

    t2 = datetime.datetime.now()
    print(f"load run time: {(t2-t1).total_seconds()} seconds", )

def main():
    if __name__ == "__main__":
        convert_to_perquet()
    
main()
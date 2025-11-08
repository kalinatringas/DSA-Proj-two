import re
import pandas as pd
from cosineSim import CosineSimAlgo as algo
import numpy as np
print("Reading dataset...")
movies = pd.read_csv("TMDB_movie_dataset_v11.csv")
movies = movies.drop_duplicates().reset_index(drop=True)
keep_cols = ['id','title','tagline','overview','genres','keywords','cast','crew',
             'release_date','runtime','vote_average','vote_count','popularity']
print("Dropping low rated movies...")
movies = movies.loc[movies['popularity'] >= 3.0, [c for c in keep_cols if c in movies.columns]].reset_index(drop=True)
for c in ['title','overview','genres','keywords','cast','crew']:
    if c in movies.columns:
        movies[c] = movies[c].fillna('')
movies = movies.head(100000)
algorithm = algo(movies)

movies = movies.reset_index()

if __name__ == "__main__":
    movie = input("What movie did you like? :")
    print(f"Here is what the cosine simulary function reccomended: \n{algorithm.recommend(movie)}")

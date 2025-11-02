import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

movies = pd.read_csv("TMDB_movie_dataset_v11.csv")
movies['genres'] = movies['genres'].fillna('')
movies['keywords'] = movies['keywords'].fillna('')  
movies['tagline'] = movies['tagline'].fillna('')

movies = movies.drop_duplicates().reset_index(drop=True)
# figure out how to filter rows with low ratings
# Keep relevant columns if exist
keep_cols = ['id','title','tagline','overview','genres','keywords','cast','crew',
             'release_date','runtime','vote_average','vote_count','popularity']
movies = movies[[c for c in keep_cols if c in movies.columns]]
for c in ['title','overview','genres','keywords','cast','crew']:
    if c in movies.columns:
        movies[c] = movies[c].fillna('')

def clean_title(title):
    # we need to clean titles to make search easier
    title = str(title)
    title = re.sub("[^a-zA-Z0-9 ]","", title)   
    return title

movies["clean_title"] = movies["title"].apply(clean_title) 

movies["combined"] = (movies['genres'] + ' ' + 
                     movies['overview'] + ' ' + 
                     movies['vote_average'].astype(str) + ' ' + 
                     movies['keywords'])
movies = movies.head(100000)
vectorizerKeywords = TfidfVectorizer(ngram_range=(1,2)) # see what this has that I don
tfdif_matrix = vectorizerKeywords.fit_transform(movies['combined'])


movies = movies.reset_index()


def reccomend(movie_title: str, n=5):
    matches = movies[movies["clean_title"].str.lower() == movie_title.lower()]
    if len(matches) == 0:
        print(f"Movie '{movie_title}' not found")
        return pd.Series(dtype=str)
    idx = matches.index[0]
    movie_vector = tfdif_matrix[idx]

    sim_scores = cosine_similarity(movie_vector, tfdif_matrix).flatten()

    top_indicies = np.argpartition(sim_scores, -n-1)
    top_indicies = top_indicies[np.argsort(-sim_scores[top_indicies])]
    top_indicies = top_indicies[top_indicies != idx][:n]
    return movies['clean_title'].iloc[top_indicies]

# def reccomend(title_index, top_n = 2):
#     sim_scores = sim

if __name__ == "__main__":
    print(reccomend("Inception"))

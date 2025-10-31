import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

movies = pd.read_csv("./.ignoreme/TMDB_movie_dataset_v11.csv")
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
movies = movies.head(10000)
#vectorizerSearch = TfidfVectorizer(ngram_range=(1,2))

# will be replaced by own function
#tfidf = vectorizerSearch.fit_transform(movies["clean_title"])

vectorizerKeywords = TfidfVectorizer(ngram_range=(1,2)) # see what this has that I don
tfdif_matrix = vectorizerKeywords.fit_transform(movies['combined'])

#cosine_sim = cosine_similarity(tfdif_matrix, tfdif_matrix)

# def search(title):
# #title = "Inception"
#     title = clean_title(title)
#     query_vec = vectorizerSearch.transform([title])
#     simularity = cosine_similarity(query_vec, tfidf).flatten()
#     indicies = np.argpartition(simularity, -5)[-5:] # finds the five most simular
#     return movies.iloc[indicies][::-1]


movies = movies.reset_index()


def reccomend(movie_title: str, n=5):
    matches = movies[movies["clean_title"].str.lower() == movie_title.lower()]
    if len(matches) == 0:
        print(f"Movie '{movie_title}' not found")
        return pd.Series(dtype=str)
    idx = matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x : x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    movie_indicies = [i[0] for i in sim_scores]
    return movies['clean_title'].iloc[movie_indicies]

# def reccomend(title_index, top_n = 2):
#     sim_scores = sim

if __name__ == "__main__":
    print(reccomend("Inception"))

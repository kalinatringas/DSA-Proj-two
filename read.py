import re
import pandas as pd
from cosineSim import CosineSimAlgo as algo
from heaps import Heap
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

def clean_text(text) -> str:
    text = text.lower()  # lowercase everything
    text = re.sub(r"[^a-z0-9 ]", "", text)  # remove punctuation
    return text


def build_similarity_heap(input_title, movies, tfidf_matrix):
    print("Building similarity heap...")
    clean_input = clean_text(input_title)
    matches = movies[movies["clean_title"] == clean_input]
    if matches.empty:
        matches = movies[movies["clean_title"].str.contains(clean_input, case=False, regex=False)]
        if matches.empty:
            print(f"Movie {input_title} not found in dataset.")
            return None
    input_idx = matches.index[0]
    input_vector = tfidf_matrix[input_idx]
    heap = Heap(is_min=False)
    for i, title in enumerate(movies['title']):
        if i == input_idx:
            continue  # skip comparing to itself
        similarity = algo.cosine_sim_man(input_vector, tfidf_matrix[i])
        heap.insert((similarity, title))
    return heap

def heap_recommend(heap, k=5):
    for _ in range(min(k, len(heap))):
        sim, title = heap.pop()
        print(f"{title} — Similarity: {sim:.3f}")

if __name__ == "__main__":
    movie = input("What movie did you like?: ")
    print(f"Here is what the KNN algorithm recommended: \n{algorithm.recommend(movie)}")
    heap = build_similarity_heap(movie, movies, algorithm.tfidf_matrix)
    print("Here is what the heap recommended:")
    heap_recommend(movie, heap)

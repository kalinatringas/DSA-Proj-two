## Movie Recommendation System
### Overview

This project implements a movie recommendation system using TF-IDF and cosine similarity.
Our system takes a movie title as input and suggests similar movies based on metadata such as genres, keywords, overview, cast, crew, and ratings.

Two recommendation methods are included:

Cosine Similarity Algorithm – Uses a TF-IDF matrix of movie features to recommend the top-N most similar movies.

Heap-Based Recommendation – Builds a heap of similarity scores to efficiently retrieve the most similar movies.

## Dataset

Source: [TMDB_movie_dataset_v11.csv](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)
> due to the datasets large size, you will have to download the dataset yourself in order to run the program

Columns used:
['id','title','tagline','overview','genres','keywords','cast','crew','release_date','runtime','vote_average','vote_count','popularity']

Preprocessing:
Drop duplicate movies.
Keep only popular movies (popularity >= 3.0).
Fill missing values in text columns with empty strings.
Limit dataset to first 100,000 movies for performance.

## Installation

Clone the repository
Install dependancies
>pip install pandas numpy

## Usage

Run the main script:
> python read.py

## Notes

Large datasets can consume significant memory, so we have limited dataset size for testing.

Currently, the system relies on exact or substring matches of movie titles.

TF-IDF vocabulary is limited to the top 15,000 words to reduce memory usage.


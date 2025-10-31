# cosine sim
import numpy as np
import re
from collections import Counter

class CosimeSimAlgo:
    def __init__(self, movies):
        self.movies = [self.clean_text(movie) for movie in movies]
        self.build_vocab()
        self.compute_tfdif()
        self.compute_sim()

    def clean_text(text):
        text = text.lower()  # lowercase everything
        text = re.sub(r"[^a-z0-9 ]", "", text)  # remove punctuation
        return text

    def build_vocab(self):
        self.vocab = sorted(set(word for movie in self.movies for word in movie.split())) # sorts alphabetically everything in the col
        self.vocab_index = {word : i for i, word in enumerate(self.vocab)}


    def compute_tfdif(self):
        
        self.tf_matrix = np.zeros((len(self.movies), len(self.vocab)))

        for i, movie in enumerate(self.movies):
            counts = Counter(movie.split()) #  
            for word, count in counts.items():
                self.tf_matrix[i, self.vocab_index[word]] = count /len(self.movies.split())
        
        n = len(self.movies)
        self.idf = np.log(n / np.array([sum(1 for movie in self.movies if word in movie.split()) for word in self.vocab]))

        self.tf_matrix = self.tf_matrix*self.idf

    # first we have to build the vocabulary


    def cosime_sim_man(vec1, vec2):
        # A dot B div by norm A  norm B, from linear alg!

        dot_product = np.dot(vec1,vec2) #thank you numpy
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2) #thank you numpy, we are just normalizing the vector
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product/(norm1 * norm2)
    
    def compute_sim(self):
        n_movies = len(self.movies)
        self.simularity


# cosine sim
import numpy as np
import re
from collections import Counter

def clean_text(text) -> str:
    text = text.lower()  # lowercase everything
    text = re.sub(r"[^a-z0-9 ]", "", text)  # remove punctuation
    return text

class CosineSimAlgo:
    def __init__(self, movies):
        self.movies = movies
        self.movies["clean_title"] = movies["title"].apply(clean_text)
        self.movies["combined"] = (movies['genres'] + ' ' +
                                   movies['overview'] + ' ' +
                                   movies['vote_average'].astype(str) + ' ' +
                                   movies['keywords'])
        self.build_vocab()
        self.compute_tfidf()

    def build_vocab(self): # building vocabulary of entire corpus
        corpus = " ".join(self.movies["combined"])
        words = corpus.split()
        word_counter = Counter(words)
        # limited to top 10k most common words for memory sake
        self.vocab = [word for word, count in word_counter.most_common(15000)]
        self.word_to_idx = {word: idx for idx, word in enumerate(self.vocab)}
        self.vocab_size = len(self.vocab)

    def tf(self, document_text): # helper to compute term frequency within one movie's data
        print("Building term frequency..")
        tf_dict = {}
        words = document_text.split()
        word_count = Counter(words)
        total_words = len(words)
        # runs in O(len(self.vocab))
        for word in self.vocab:
            count = word_count.get(word, 0)
            tf_dict[word] = count / float(total_words) if total_words > 0 else 0

        return tf_dict

    def compute_tfidf(self):
        # TF: how frequently a word appears in a movie
        # IDF: given N movies, # of movies in which term appears for each term
        # TF-IDF = TF * IDF
        N = len(self.movies)
        # building document-term matrix (DTM)
        # runs in O(len(self.movies[combined])* len(word_count.items()))
        print("Building document-term-matrix...")
        dtm = np.zeros((N, self.vocab_size))
        doc_lengths = np.zeros(N)
        for i, text in enumerate(self.movies["combined"]):
            words = text.split()
            doc_lengths[i] = len(words)
            word_count = Counter(words)
            for word, count in word_count.items():
                if word in self.word_to_idx:
                    j = self.word_to_idx[word]
                    dtm[i, j] = count

        print("Computing document frequencies...")
        doc_freq = np.sum(dtm > 0, axis=0)  # count docs where word appears

        print("Computing inverse document frequency..")
        idf = np.log10((N + 1.0) / (doc_freq + 1.0))

        print("Computing term frequency...")
        tf = dtm / doc_lengths[:, np.newaxis] # broadcasted division

        self.tfidf_matrix = tf * idf  # element-wise multiplication
        print("TF-IDF Matrix computed!")


    @staticmethod
    def cosine_sim_man(vec1, vec2):
        #print("Computing Cosine Similarity...")
        # A dot B div by norm A  norm B, from linear alg!
        dot_product = np.dot(vec1,vec2) #thank you numpy
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2) #thank you numpy, we are just normalizing the vector
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product/(norm1 * norm2)

    def recommend(self, movie_title: str, n=5):
        print("Recommending...")
        # Find matching movies to given title
        clean_input = clean_text(movie_title)
        matches = self.movies[self.movies["clean_title"] == clean_input]

        if len(matches) == 0:
            print(f"Movie '{movie_title}' not found")
            return -1

        idx = matches.index[0]
        movie_vector = self.tfidf_matrix[idx]

        # compute similarity scores using cosine similarity
        sim_scores = []
        print("Computing Cosine Similarity...")
        for i in range(len(self.movies)):
            sim = self.cosine_sim_man(movie_vector, self.tfidf_matrix[i])
            sim_scores.append(sim)
        sim_scores = np.array(sim_scores)

        top_indices = np.argpartition(sim_scores, -n - 1)
        top_indices = top_indices[np.argsort(-sim_scores[top_indices])]
        top_indices = top_indices[top_indices != idx][:n]

        return self.movies['title'].iloc[top_indices]
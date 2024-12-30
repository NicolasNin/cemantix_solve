import numpy as np
import random
from api_score import *
from  models import get_model
from sklearn.metrics.pairwise import cosine_similarity
import time

MAX_ATTEMPT = 10

def cosine_one_vs_all(model, word):
    if word in model.key_to_index:
        return np.round(cosine_similarity([model[word]],model.vectors),4)

def get_possible_words_from_score(model,word,score,epsilon=0):
    if word in model.key_to_index:
        c = cosine_one_vs_all(model, word)
        return [model.index_to_key[x] for x in np.where(np.abs(c-score)<=epsilon)[1]]

def random_word(model):
    N = len(model.key_to_index)
    return model.index_to_key[random.randint(0,N)]

class Solver:
    def __init__(self,language="fr"):
        self.model = get_model(language)
        self.word_scores = {}
        self.possible = list(self.model.key_to_index)
        self.first_word_method = "random"

    def get_starting_word(self):
        if self.first_word_method == "random":
            return random_word(self.model)
        return 'spécifique'
    
    def get_possible_words_from_score(self,word,score,epsilon=0):
        return get_possible_words_from_score(self.model,word,score,epsilon=epsilon)
    
    def auto_solve(self):
        word = self.get_starting_word()
        notFound = True
        possible = list(self.model.key_to_index)
        i=0
        while notFound:
            print(f"Step {i+1}")
            print("-----------------------------")
            print(f"checking score for {word}")
            score = self.send_word(word)
            print(word,score)
            new_possible = self.get_possible_words_from_score(word,score["score"])
            sim = score["score"]
            print(f"Possible found: {len(new_possible)} with similarity {sim}")
            print(new_possible)
            possible = np.intersect1d(possible,new_possible)
            if len(possible)<len(new_possible):
                print("Intersection:")
                print(possible)
            if len(possible)==1:
                notFound = False
            word = possible[0]
            i+=1
            if i>MAX_ATTEMPT:
                print("Max attempt Reached")
                break
            time.sleep(0.5)


    def check_word(self,word):
        return word in self.model.key_to_index
    
    def send_word(self,word,force=False):
        if word not in self.word_scores:
            if self.check_word(word) or force:
                score = get_score(word)
                if score != "error":
                    self.word_scores[word] = score
                    return score
            else:
                print(f"{word} not in model")

    def find_close_words(self, word,target_sim, epsilon=0.0001):
        results = []
        for w in self.model.key_to_index:
            if w == word:
                continue
            sim = self.model.similarity(word, w)
            if abs(sim - target_sim) <= epsilon:
                results.append((w, sim))
        
        # Sort by how close they are to target similarity
        return sorted(results, key=lambda x: abs(x[1] - target_sim))

if __name__ == "__main__":
    solver = Solver()
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

def random_word(model,max_N=-1):
    if max_N==-1:
        N = len(model.key_to_index)
    else:
        N=max_N
    return model.index_to_key[random.randint(0,N)]



class Game:
    def __init__(self,model,difficulty="medium"):
        self.model = model
        self.current_word = None
        self.top_similar = {}
        self.difficulty = difficulty
        self.N_max = None
        self.set_difficulty(difficulty)
        self.init_random_word()

    def set_difficulty(self,difficulty):
        difficulty_dict = {"easy":1000,"medium":5000,"hard":10000,"very_hard":-1}
        if difficulty in difficulty_dict:
            self.difficulty = difficulty
            self.N_max = difficulty_dict[difficulty]
            self.init_random_word()  

    def init_random_word(self):
        self.current_word = random_word(self.model,max_N=self.N_max)
        print(f"NEW RANDOM WORD {self.current_word}")
        top_similar = self.model.most_similar(self.current_word,topn=999)
        self.top_similar = {}
        for i,(word,score) in enumerate(top_similar):
            self.top_similar[word]=(1000-i-1,round(score,4))
        return  self.current_word
    
    def get_score(self,word):
        print("IN game",self.current_word,word)
        if word == self.current_word:
            return {"score":1,"percentile":1000}
        if word in self.model.key_to_index:
            if word in self.top_similar:
                percentile,score = self.top_similar[word]
                return {"score":round(score,4),"percentile":percentile}
            return {"score":round(self.model.similarity(word,self.current_word),4)}
        else:
            return {'error': 'Je ne connais pas le mot <i>'+word+'</i>.'}
class Solver:
    def __init__(self,language="fr",score_strategy=None):
        self.model = get_model(language)
        self.word_scores = {}
        self.possible = list(self.model.key_to_index)
        self.first_word_method = "random"
        self.api = "fr"
        self.score_strategy = score_strategy or ExternalAPIStrategy()
    
    def reset(self):
        self.word_scores = {}
        self.possible = list(self.model.key_to_index)
    def get_score(self,word):
        return self.score_strategy.get_score(word)
    def set_score_strategy(self, strategy: ScoreStrategy):
        """Allow switching strategies at runtime"""
        print("switching strategy",strategy)
        self.score_strategy = strategy
        self.reset()
    def get_starting_word(self):
        if self.first_word_method == "random":
            return random_word(self.model)
        return 'spécifique'
    def get_random_word(self):
        return random_word(self.model,max_N=2000)

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
    
    def send_word(self,word):
        print(self.word_scores)
        if word in self.word_scores:
            return self.word_scores[word]
        if self.check_word(word) :
            score = self.get_score(word)
            print("get score",word,score)
            if score != "error":
                self.word_scores[word] = score
                return score
        else:
            print(f"{word} not in model")
            return {"error":"word not in model"}

if __name__ == "__main__":
    solver = Solver()
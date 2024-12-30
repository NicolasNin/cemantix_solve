import gensim
import numpy as np
model = gensim.models.KeyedVectors.load_word2vec_format('model/frWac_no_postag_phrase_500_cbow_cut10_stripped.bin', binary=True)

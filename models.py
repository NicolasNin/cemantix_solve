import gensim
model_path={
    "fr":'models/frWac_no_postag_phrase_500_cbow_cut10_stripped.bin',
    "en":'models/GoogleNews-vectors-negative300_stripped.bin'
}

def get_model(language="fr"):
    if language in model_path:
        path = model_path[language]
        return gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    return "language not found"
from gensim.models import word2vec
from gensim.models import KeyedVectors

W2V_SG_GOLD_MODEL_PATH = "./self-made-word2vec/gold/sg/default_2022-06-08 01:23:23.927263.model"
W2V_CBOW_GOLD_MODEL_PATH = "./self-made-word2vec/gold/cbow/default_2022-06-08 01:23:39.405964.model"

W2V_CBOW_GITHUB_MODEL_PATH = "./self-made-word2vec/github/cbow/default_2022-06-08 02:39:57.235883.model"
W2V_SG_GITHUB_MODEL_PATH = "./self-made-word2vec/github/sg/default_2022-06-08 02:49:07.957679.model"

from collections import defaultdict
from gensim.models.keyedvectors import KeyedVectors
from sklearn.cluster import KMeans

class W2V(object):
    @staticmethod
    def load():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        results = model.wv.most_similar(positive=["SC-APT-GET-INSTALL"])
        print(model.wv["SC-APT-GET-INSTALL"])


def main():
    pass
    W2V.load()
    

if __name__ == "__main__":
    main()
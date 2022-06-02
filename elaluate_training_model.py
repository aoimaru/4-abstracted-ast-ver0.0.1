from gensim.models.doc2vec import Doc2Vec

GOLD_DBOW_PATH = "./self-made-model/gold/dbow/default_2022-06-02 21:33:08.518763.model"

class D2V():
    @staticmethod
    def load():
        model = Doc2Vec.load(GOLD_DBOW_PATH)
        



def main():
    pass


if __name__ == "__main__":
    main()
from gensim.models import word2vec
from gensim.models import KeyedVectors

import numpy as np

from numpy import dot
from numpy.linalg import norm

W2V_SG_GOLD_MODEL_PATH = "./self-made-word2vec/gold/sg/default_2022-06-08 01:23:23.927263.model"
W2V_CBOW_GOLD_MODEL_PATH = "./self-made-word2vec/gold/cbow/default_2022-06-08 01:23:39.405964.model"

W2V_CBOW_GITHUB_MODEL_PATH = "./self-made-word2vec/github/cbow/default_2022-06-08 02:39:57.235883.model"
W2V_SG_GITHUB_MODEL_PATH = "./self-made-word2vec/github/sg/default_2022-06-08 02:49:07.957679.model"

from collections import defaultdict
from gensim.models.keyedvectors import KeyedVectors
from sklearn.cluster import KMeans

class W2V(object):
    @staticmethod
    def sample():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        results = model.wv.most_similar(positive=["SC-APT-GET-INSTALL"])
        apt_install = model.wv["SC-APT-GET-INSTALL"]
        apt_pkg = model.wv["SC-APT-GET-PACKAGES"]
        apt_add = apt_install+apt_pkg
        print(apt_add)

    @staticmethod
    def load():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR']
        sample_2 = ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL']

        sample_3 = ['SC-EXPORT', 'SC-EXPORT-TARGET', 'BASH-ASSIGN', 'BASH-ASSIGN-RHS', 'BASH-DOUBLE-QUOTED', 'BASH-DOLLAR-PARENS', 'SC-MKTEMP', 'SC-MKTEMP-F-DIRECTORY']

        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            ss_1 += model.wv[sam_1]
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            ss_2 += model.wv[sam_2]
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            ss_3 += model.wv[sam_3]

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()
    
    @staticmethod
    def load2():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['SC-APK-ADD', 'SC-APK-F-NO-CACHE']
        sample_2 = ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:GNUPG']

        sample_3 = ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-ADD-USER', 'SC-ADD-USER-F-DEFAULTS']

        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            ss_1 += model.wv[sam_1]
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            ss_2 += model.wv[sam_2]
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            ss_3 += model.wv[sam_3]

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()

    @staticmethod
    def load3():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL']
        sample_2 = ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL']

        sample_3 = ['SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL']

        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            ss_1 += model.wv[sam_1]
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            ss_2 += model.wv[sam_2]
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            ss_3 += model.wv[sam_3]

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()

    @staticmethod
    def load4():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['SC-APT-GET-UPDATE', 'SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:JQ']
        sample_2 = ['SC-APT-GET-UPDATE', 'SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS']
        
        sample_3 = ['SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL']

        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            ss_1 += model.wv[sam_1]
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            ss_2 += model.wv[sam_2]
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            ss_3 += model.wv[sam_3]

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()
    
    @staticmethod
    def load5():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['SC-APT-GET-UPDATE', 'SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:JQ']
        sample_2 = ['SC-APT-GET-UPDATE', 'SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS']
        
        sample_3 = ['SC-APT-GET-UPDATE', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL']

        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            ss_1 += model.wv[sam_1]
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            ss_2 += model.wv[sam_2]
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            ss_3 += model.wv[sam_3]

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()

    
    @staticmethod
    def test():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        results = model.wv.most_similar(
            positive=["SC-APT-GET-UPDATE", "SC-APT-GET-INSTALL", "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:JQ'],
            negative=["SC-APT-GET-INSTALL", 'SC-APT-GET-PACKAGES',"SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 'SC-APT-GET-PACKAGE:JQ']
        )

        for result in results:
            print(result)

    @staticmethod
    def test2():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ["SC-APT-GET-UPDATE", "SC-APT-GET-INSTALL", "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:JQ']
        sample_2 = ["SC-APT-GET-UPDATE", "SC-APT-GET-INSTALL", 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:JQ']
        
        sample_3 = ['SC-APT-GET-UPDATE', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL']

        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            ss_1 += model.wv[sam_1]
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            ss_2 += model.wv[sam_2]
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            ss_3 += model.wv[sam_3]

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()


def main():
    pass
    W2V.test()
    

if __name__ == "__main__":
    main()
from gensim.models import word2vec
from gensim.models import KeyedVectors

import numpy as np

from numpy import dot
from numpy.linalg import norm

W2V_SG_GOLD_MODEL_PATH = "./self-made-word2vec/gold/sg/default_2022-06-08 01:23:23.927263.model"
W2V_CBOW_GOLD_MODEL_PATH = "./self-made-word2vec/gold/cbow/default_2022-06-08 01:23:39.405964.model"

W2V_CBOW_GITHUB_MODEL_PATH = "./self-made-word2vec/github/cbow/default_2022-06-08 02:39:57.235883.model"
W2V_SG_GITHUB_MODEL_PATH = "./self-made-word2vec/github/sg/default_2022-06-08 02:49:07.957679.model"

LOAD8 = "./self-made-word2vec/github/sg/default_2022-06-08 02:49:07.957679.model"

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
            try:
                com = model.wv[sam_1]
            except Exception as e:
                pass
            else:
                ss_1 += com
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            try:
                com = model.wv[sam_2]
            except Exception as e:
                pass
            else:
                ss_2 += com
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            try:
                com = model.wv[sam_3]
            except Exception as e:
                pass
            else:
                ss_3 += com

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

    @staticmethod
    def load6():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:GNUPG']
        sample_2 = ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:DIRMNGR']
        
        sample_3 = ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:CA-CERTIFICATES']

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
    def load7():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)
        sample_1 = ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-ASC']
        sample_2 = ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR']
        
        sample_3 = ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:CA-CERTIFICATES']

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
    def load8():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)

        sp_1 = [
            ['BASH-FOR-IN', 'BASH-FOR-IN-VARIABLE', 'BASH-VARIABLE:url'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-ITEMS', 'BASH-VARIABLE:TOMCAT_TGZ_URLS'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-THEN', 'BASH-ASSIGN', 'BASH-ASSIGN-LHS', 'BASH-VARIABLE:success'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-THEN', 'BASH-ASSIGN', 'BASH-ASSIGN-RHS', 'BASH-LITERAL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-THEN', 'UNKNOWN'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-ELSE']
        ]

        sp_2 = [
            ['BASH-FOR-IN', 'BASH-FOR-IN-VARIABLE', 'BASH-VARIABLE:url'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-ITEMS', 'BASH-VARIABLE:TOMCAT_ASC_URLS'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-ASC'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-CONDITION', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-THEN', 'BASH-ASSIGN', 'BASH-ASSIGN-LHS', 'BASH-VARIABLE:success'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-THEN', 'BASH-ASSIGN', 'BASH-ASSIGN-RHS', 'BASH-LITERAL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-THEN', 'UNKNOWN'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'BASH-IF-EXPRESSION', 'BASH-IF-ELSE']
        ]

        sp_3 = [
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:WGET'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:CA-CERTIFICATES']
        ]


        sample_1 = list()
        sample_2 = list()
        sample_3 = list()

        for s_1 in sp_1:
            sample_1.extend(s_1)

        for s_2 in sp_2:
            sample_2.extend(s_2)

        for s_3 in sp_3:
            sample_3.extend(s_3)
        


        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            try:
                com = model.wv[sam_1]
            except Exception as e:
                pass
            else:
                ss_1 += com
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            try:
                com = model.wv[sam_2]
            except Exception as e:
                pass
            else:
                ss_2 += com
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            try:
                com = model.wv[sam_3]
            except Exception as e:
                pass
            else:
                ss_3 += com

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()
    
    @staticmethod
    def load9():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)

        sp_1 = [
            ['SC-SET', 'SC-SET-F-E'],
            ['SC-SET', 'SC-SET-F-X'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-VARIABLE', 'BASH-VARIABLE:key'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-ITEMS', 'BASH-VARIABLE:GPG_KEYS'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-GPG', 'SC-GPG-F-BATCH'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-GPG', 'SC-GPG-KEYSERVER', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-GPG', 'SC-GPG-KEYSERVER', 'BASH-LITERAL', 'ABS-URL-HA-POOL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-GPG', 'SC-GPG-KEYSERVER', 'BASH-LITERAL', 'ABS-URL-POOL'],
            ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-GPG', 'SC-GPG-RECV-KEYS', 'SC-GPG-RECV-KEY', 'BASH-LITERAL']
        ]

        sp_2 = [
            ['SC-SET', 'SC-SET-F-E'],
            ['SC-SET', 'SC-SET-F-X'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
            ['SC-LDCONFIG', 'SC-LDCONFIG-F-VERBOSE']
        ]

        sp_3 = [
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:WGET'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:CA-CERTIFICATES']
        ]


        sample_1 = list()
        sample_2 = list()
        sample_3 = list()

        for s_1 in sp_1:
            sample_1.extend(s_1)

        for s_2 in sp_2:
            sample_2.extend(s_2)

        for s_3 in sp_3:
            sample_3.extend(s_3)
        


        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            try:
                com = model.wv[sam_1]
            except Exception as e:
                pass
            else:
                ss_1 += com
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            try:
                com = model.wv[sam_2]
            except Exception as e:
                pass
            else:
                ss_2 += com
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            try:
                com = model.wv[sam_3]
            except Exception as e:
                pass
            else:
                ss_3 += com

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()

    @staticmethod
    def load10():
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH)

        sp_1 = [
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE']
        ]

        sp_2 = [
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-COMMAND', 'BASH-BRACE-GROUP', 'SC-ECHO', 'SC-ECHO-ITEMS', 'SC-ECHO-ITEM', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
            ['BASH-REDIRECT', 'BASH-REDIRECT-REDIRECTS', 'BASH-REDIRECT-OVERWRITE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE']
        ]

        sp_3 = [
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:WGET'],
            ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:CA-CERTIFICATES']
        ]


        sample_1 = list()
        sample_2 = list()
        sample_3 = list()

        for s_1 in sp_1:
            sample_1.extend(s_1)

        for s_2 in sp_2:
            sample_2.extend(s_2)

        for s_3 in sp_3:
            sample_3.extend(s_3)
        


        ss_1 = np.zeros(100)
        for sam_1 in sample_1:
            try:
                com = model.wv[sam_1]
            except Exception as e:
                pass
            else:
                ss_1 += com
        # print(ss_1)

        ss_2 = np.zeros(100)
        for sam_2 in sample_2:
            try:
                com = model.wv[sam_2]
            except Exception as e:
                pass
            else:
                ss_2 += com
        # print(ss_2)
        
        result = dot(ss_1, ss_2)/(norm(ss_1)*norm(ss_2))
        print("s1~s2: ", result)
        print()

        ss_3 = np.zeros(100)
        for sam_3 in sample_3:
            try:
                com = model.wv[sam_3]
            except Exception as e:
                pass
            else:
                ss_3 += com

        result = dot(ss_1, ss_3)/(norm(ss_1)*norm(ss_3))
        print("s1~s3: ",result)
        print()

        result = dot(ss_2, ss_3)/(norm(ss_2)*norm(ss_3))
        print("s2~s3: ", result)
        print()

def main():
    pass
    W2V.load10()
    

if __name__ == "__main__":
    main()
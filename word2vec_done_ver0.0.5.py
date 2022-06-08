from gensim.models import word2vec
from gensim.models import KeyedVectors

import json
import copy
import pathlib
import os
from datetime import datetime
import sys
import glob
import pprint

import numpy as np

from numpy import dot
from numpy.linalg import norm

W2V_SG_GOLD_MODEL_PATH = "./self-made-word2vec/gold/sg/default_2022-06-08 01:23:23.927263.model"
W2V_CBOW_GOLD_MODEL_PATH = "./self-made-word2vec/gold/cbow/default_2022-06-08 01:23:39.405964.model"

W2V_CBOW_GITHUB_MODEL_PATH = "./self-made-word2vec/github/cbow/default_2022-06-08 02:39:57.235883.model"
W2V_SG_GITHUB_MODEL_PATH = "./self-made-word2vec/github/sg/default_2022-06-08 02:49:07.957679.model"

W2V_SG_GITHUB_MODEL_PATH_2 = "./self-made-word2vec/github/sg/06082252_2022-06-08 22:59:55.372483.model"

LOAD8 = "./self-made-word2vec/github/sg/default_2022-06-08 02:49:07.957679.model"

VECTOR_SIZE = 100

"""
    - goldルールのみのファイルパスを取得するためのパス
"""
PATCH_GLOB_SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/**"


from collections import defaultdict
from gensim.models.keyedvectors import KeyedVectors
from sklearn.cluster import KMeans

SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/"

SELF_MADE_DATASETS_GITHUB_PATH = "./self-made-datasets/github/"
SAMPLE_WORD2VEC_PATH = "./sample/word2vec/gold/"

class Recursive(object):
    @staticmethod
    def do(obj):
        """
            - シンプルな再帰
            - 深さ優先探索を行う
            - ASTをDoc2Vecで受け入れられる最低限の形に持っていく
        """
        tokens = list()
        def rec(now, tp=list()):
            # print(now["children"])
            if now["children"]:
                for nxt in now["children"]:
                    ntp = copy.copy(tp)
                    ntp.append(now["type"])
                    rec(nxt, ntp)
            else:
                tp.append(now["type"])
                tokens.append(tp)
        rec(obj, tp=list())
        
        return tokens

class BaseAST(object):
    def __init__(self, file_sha):
        def exists() -> bool:
            return os.path.exists(file_path)
        file_path = "{}{}.json".format(SELF_MADE_DATASETS_GITHUB_PATH, file_sha); file_path = str(pathlib.Path(file_path).resolve())
        if exists():
            with open(file_path, mode="r") as f:
                obj = json.load(f)
        else:
            obj = dict()
        self._children = obj
        self._file_sha = file_sha
    @property
    def children(self):
        pass
    
    @children.getter
    def children(self):
        return self._children
    
    @property
    def file_sha(self):
        pass

    @file_sha.getter
    def file_sha(self):
        return self._file_sha

class MetaData(object):
    @staticmethod
    def get_sha():
        with open(METADATA_SHA_PATH, mode="r") as f:
            data = json.load(f)
        return data["file_sha"]
    
    @staticmethod
    def patch():
        file_shas = list()
        origins = [origin for origin in glob.glob(PATCH_GLOB_SELF_MADE_DATASETS_GOLD_PATH, recursive=True)]
        for origin in origins:
            base_name = os.path.basename(origin)
            file_sha = base_name.replace(".json", "")
            file_shas.append(file_sha)
        return file_shas

class W2V(object):
    @staticmethod
    def load(test_case):
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH_2)
        
        subject = list()
        for tc in test_case:
            subject.extend(tc)

        subject_vector = np.zeros(VECTOR_SIZE)
        for sub in subject:
            try:
                sub_vec = model.wv[sub]
            except Exception as e:
                pass
            else:
                subject_vector += sub_vec

        snaps = list()
        file_sha = MetaData.patch()
        for sha in file_sha:
            ast_obj = BaseAST(sha)
            children = ast_obj.children
            for child in children:
                if child["type"] == "DOCKER-RUN":
                    tokens = Recursive.do(child)
                    test_vector = np.zeros(VECTOR_SIZE)
                    for token in tokens:
                        tars = token[2:]
                        for tar in tars:
                            try:
                                tar_vec = model.wv[tar]
                            except Exception as e:
                                pass
                            else:
                                test_vector += tar_vec
                    try:
                        result = dot(subject_vector, test_vector)/(norm(subject_vector)*norm(test_vector))
                    except Exception as e:
                        print(e)
                    else:
                        if result > 0.75:
                            words = list()
                            for token in tokens:
                                words.append(token[2:])
                            snap = {
                                "result": result,
                                "file_sha": ast_obj.file_sha,
                                "tokens": words
                            }
                            snaps.append(snap)
                                
        return snaps
    
    @staticmethod
    def test(test_case, predict, limit):
        model = word2vec.Word2Vec.load(W2V_SG_GITHUB_MODEL_PATH_2)
        
        subject = list()
        for tc in test_case:
            subject.extend(tc)

        subject_vector = np.zeros(VECTOR_SIZE)
        for sub in subject:
            try:
                sub_vec = model.wv[sub]
            except Exception as e:
                pass
            else:
                subject_vector += sub_vec

        snaps = list()
        file_sha = MetaData.patch()
        for sha in file_sha:
            ast_obj = BaseAST(sha)
            children = ast_obj.children
            for child in children:
                if child["type"] == "DOCKER-RUN":
                    tokens = Recursive.do(child)
                    test_vector = np.zeros(VECTOR_SIZE)
                    for token in tokens:
                        tars = token[2:]
                        for tar in tars:
                            try:
                                tar_vec = model.wv[tar]
                            except Exception as e:
                                pass
                            else:
                                test_vector += tar_vec
                    try:
                        result = dot(subject_vector, test_vector)/(norm(subject_vector)*norm(test_vector))
                    except Exception as e:
                        pass
                    else:
                        if result > 0.75:
                            words = list()
                            for token in tokens:
                                words.append(token[2:])
                            snap = {
                                "result": result,
                                "file_sha": ast_obj.file_sha,
                                "tokens": words
                            }
                            snaps.append(snap)
                                
        count = 0
        for snap in snaps:
            tokens = snap["tokens"]
            for token in tokens:
                if predict in token:
                    count += 1
                    break
            else:
                # print(tokens)
                continue

        print("count: {}/{}".format(count, len(snaps)))
        print("{}%".format(count/len(snaps)*100))


def test1():
    test_case = [
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-APT-GET-UPDATE", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-APT-GET-UPDATE", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-APT-GET-UPDATE", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-APT-GET-UPDATE", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-APT-GET-UPDATE", 0.95)

def test2():
    test_case = [
        ['SC-APT-GET-UPDATE'],
        # ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.95)

def test2():
    test_case = [
        ['SC-APT-GET-UPDATE'],
        # ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-APT-GET-F-YES", 0.95)

def test3():
    test_case = [
        ['SC-APT-GET-UPDATE'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-RM", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-RM", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-RM", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-RM", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-RM", 0.95)

def test4():
    test_case = [
        ['SC-APT-GET-UPDATE'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "ABS-APT-LISTS", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "ABS-APT-LISTS", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "ABS-APT-LISTS", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "ABS-APT-LISTS", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "ABS-APT-LISTS", 0.95)


def test5():
    test_case = [
        ['SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL'],
        ['SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.95)

def test6():
    test_case = [
        # ['SC-CONFIGURE', 'SC-CONFIGURE-BUILD', 'BASH-LITERAL']
        ['SC-CONFIGURE', 'SC-CONFIGURE-WITH-CONFIG-FILE-PATH', 'BASH-LITERAL'],
        ['SC-CONFIGURE', 'SC-CONFIGURE-WITH-CONFIG-FILE-SCAN-DIR', 'BASH-LITERAL']
    ]

    print("閾値:{}".format(0.65))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.65)
    print("閾値:{}".format(0.70))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.70)
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-CONFIGURE-BUILD", 0.95)

def test7():
    test_case = [
        ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
        # ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-URL-PROTOCOL-HTTPS'],
        ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
        ['SC-CURL', 'SC-CURL-F-FAIL'],
        ['SC-CURL', 'SC-CURL-F-LOCATION']
    ]

    print("閾値:{}".format(0.65))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.65)
    print("閾値:{}".format(0.70))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.70)
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "ABS-URL-PROTOCOL-HTTPS", 0.95)

def test8():
    test_case = [
        ['SC-APT-GET-UPDATE'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        # ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-APT-GET-F-NO-INSTALL-RECOMMENDS", 0.95)


def test9():
    test_case = [
        # ['SC-APK-ADD', 'SC-APK-F-NO-CACHE'],
        # ['SC-APK-ADD', 'SC-APK-F-NO-CACHE'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:BASH'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:LESS'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:MYSQL-CLIENT']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-APK-F-NO-CACHE", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-APK-F-NO-CACHE", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-APK-F-NO-CACHE", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-APK-F-NO-CACHE", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-APK-F-NO-CACHE", 0.95)

def test10():
    test_case = [
        ['SC-TAR', 'SC-TAR-X'],
        ['SC-TAR', 'SC-TAR-J'],
        ['SC-TAR', 'SC-TAR-FILE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
        ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
        ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-SRC-DIR'],
        ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-USR-SRC-DIR']
    ]

    
    print("閾値:{}".format(0.75))
    W2V.test(test_case, "SC-RM", 0.75)
    print("閾値:{}".format(0.80))
    W2V.test(test_case, "SC-RM", 0.80)
    print("閾値:{}".format(0.85))
    W2V.test(test_case, "SC-RM", 0.85)
    print("閾値:{}".format(0.90))
    W2V.test(test_case, "SC-RM", 0.90)
    print("閾値:{}".format(0.95))
    W2V.test(test_case, "SC-RM", 0.95)
    

def main():
    test10()

if __name__ == "__main__":
    main()

# ['SC-CONFIGURE', 'SC-CONFIGURE-BUILD', 'BASH-LITERAL']
# ['SC-CONFIGURE', 'SC-CONFIGURE-WITH-CONFIG-FILE-PATH', 'BASH-LITERAL']
# ['SC-CONFIGURE', 'SC-CONFIGURE-WITH-CONFIG-FILE-SCAN-DIR', 'BASH-LITERAL']


# ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL']
# ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-URL-PROTOCOL-HTTPS']
# ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-EXTENSION-TAR']
# ['SC-CURL', 'SC-CURL-F-FAIL']
# ['SC-CURL', 'SC-CURL-F-LOCATION']


# ['SC-TAR', 'SC-TAR-X']
# ['SC-TAR', 'SC-TAR-J']
# ['SC-TAR', 'SC-TAR-FILE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR']
# ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH']
# ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE']
# ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-SRC-DIR']
# ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-USR-SRC-DIR']
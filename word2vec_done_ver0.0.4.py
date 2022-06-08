from gensim.models import word2vec
from gensim.models import KeyedVectors

import json
import copy
import pathlib
import os
from datetime import datetime
import sys
import glob

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
                print(e)
            else:
                subject_vector += sub_vec

        count = 0
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
                                # print(e)
                            else:
                                test_vector += tar_vec
                    try:
                        result = dot(subject_vector, test_vector)/(norm(subject_vector)*norm(test_vector))
                    except Exception as e:
                        print(e)
                    else:
                        if result > 0.75:
                            count += 1
                            print("result: ", result, ast_obj.file_sha)
                            for token in tokens:
                                print(token[2:])
                            print()
        print("count:{}".format(count))        



def main():
    test_case = [
        ['SC-RM', 'SC-RM-F-RECURSIVE'],
        ['SC-RM', 'SC-RM-F-FORCE'],
        ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-APT-LISTS'],
        ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-PATH-VAR'],
        ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
        ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-GLOB', 'ABS-GLOB-STAR']
    ]


    test_case_2 = [
        ['SC-APK-ADD', 'SC-APK-F-NO-CACHE'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:BASH'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:LESS'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:MYSQL-CLIENT']
    ]

    test_case_3 = [
        ['SC-SET', 'SC-SET-F-E'],
        ['SC-SET', 'SC-SET-F-X'],
        ['SC-MKDIR', 'SC-MKDIR-F-PARENTS'],
        ['SC-MKDIR', 'SC-MKDIR-PATHS', 'SC-MKDIR-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        ['SC-MKDIR', 'SC-MKDIR-PATHS', 'SC-MKDIR-PATH', 'BASH-LITERAL', 'ABS-PATH-VAR'],
        ['SC-MKDIR', 'SC-MKDIR-PATHS', 'SC-MKDIR-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
        ['SC-CHOWN', 'SC-CHOWN-F-RECURSIVE'],
        ['SC-CHOWN', 'SC-CHOWN-OWNER', 'BASH-LITERAL'],
        ['SC-CHOWN', 'SC-CHOWN-PATHS', 'SC-CHOWN-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        ['SC-CHOWN', 'SC-CHOWN-PATHS', 'SC-CHOWN-PATH', 'BASH-LITERAL', 'ABS-PATH-VAR'],
        ['SC-CHOWN', 'SC-CHOWN-PATHS', 'SC-CHOWN-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE']
    ]

    test_case_4 = [
        ['SC-LN', 'SC-LN-F-SYMBOLIC'],
        ['SC-LN', 'SC-LN-F-FORCE'],
        ['SC-LN', 'SC-LN-TARGET', 'BASH-LITERAL'],
        ['SC-LN', 'SC-LN-LINK', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        ['SC-LN', 'SC-LN-LINK', 'BASH-LITERAL', 'ABS-PATH-ROOT-DIR'],
        ['SC-LN', 'SC-LN-LINK', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE']
    ]

    test_case_5 = [
        ['SC-APT-GET-UPDATE'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    test_case_6 = [
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
        ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:LIBNSS-WRAPPER']
    ]

    test_case_7 = [
        ['SC-TAR', 'SC-TAR-X'],
        ['SC-TAR', 'SC-TAR-V'],
        ['SC-TAR', 'SC-TAR-FILE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
        ['SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL'],
        ['SC-TAR', 'SC-TAR-STRIP-COMPONENTS', 'BASH-LITERAL']
    ]

    test_case_8 = [
        ['SC-CURL', 'SC-CURL-OUTPUT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        ['SC-CURL', 'SC-CURL-OUTPUT', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
        # ['SC-CURL', 'SC-CURL-F-FAIL'],
        # ['SC-CURL', 'SC-CURL-F-SHOW-ERROR'],
        # ['SC-CURL', 'SC-CURL-F-LOCATION'],
        ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
        ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-URL-PROTOCOL-HTTPS']
    ]

    test_case_9 = [
        ['SC-GPG', 'SC-GPG-F-BATCH'],
        ['SC-GPG', 'SC-GPG-VERIFYS', 'SC-GPG-VERIFY', 'BASH-LITERAL', 'ABS-EXTENSION-ASC'],
        ['SC-GPG', 'SC-GPG-VERIFYS', 'SC-GPG-VERIFY', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
        ['SC-GPG', 'SC-GPG-VERIFYS', 'SC-GPG-VERIFY', 'BASH-LITERAL', 'ABS-EXTENSION-TAR']
    ]

    test_case_10 = [
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:GIT'],
        ['SC-APK-ADD', 'SC-APK-PACKAGES', 'SC-APK-PACKAGE:OPENSSH-CLIENT']
    ]

    test_case_11 = [
        ['SC-CONFIGURE', 'SC-CONFIGURE-BUILD', 'BASH-LITERAL']
        # ['BASH-SUBSHELL', 'SC-CONFIGURE', 'SC-CONFIGURE-LIBDIR', 'BASH-LITERAL'],
        # ['BASH-SUBSHELL', 'SC-CONFIGURE', 'SC-CONFIGURE-PREFIX', 'BASH-PATH', 'BASH-LITERAL']
        # ['BASH-SUBSHELL', 'SC-CONFIGURE', 'SC-CONFIGURE-WITH-APR', 'BASH-LITERAL']
        # ['BASH-SUBSHELL', 'SC-CONFIGURE', 'SC-CONFIGURE-WITH-JAVA-HOME', 'BASH-LITERAL'],
        # ['BASH-SUBSHELL', 'SC-CONFIGURE', 'SC-CONFIGURE-F-WITH-SSL']
    ]

    test_case_12 = [
        ['BASH-SUBSHELL', 'SC-MAKE', 'SC-MAKE-JOBS', 'BASH-LITERAL', 'ABS-SINGLE-SPACE'],
        ['BASH-SUBSHELL', 'SC-MAKE', 'SC-MAKE-TARGET', 'BASH-LITERAL']
    ]

    test_case_13 = [
        ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-X'],
        ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-Z']
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-FILE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-STRIP-COMPONENTS', 'BASH-LITERAL']
    ]

    test_case_13 = [
        ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL'],
        ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
        ['BASH-FOR-IN', 'BASH-FOR-IN-BODY', 'SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL', 'ABS-URL-PROTOCOL-HTTPS']
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-FILE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-MAYBE-PATH'],
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-DIRECTORY', 'BASH-PATH', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
        # ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-TAR', 'SC-TAR-STRIP-COMPONENTS', 'BASH-LITERAL']
    ]

    W2V.load(test_case)
    

if __name__ == "__main__":
    main()
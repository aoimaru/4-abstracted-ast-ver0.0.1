import json
import copy
import pathlib
import os
from datetime import datetime
import sys

import glob

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

GOLD_DBOW_PATH = "./self-made-model/gold/dbow/default_2022-06-02 21:33:08.518763.model"
GOLD_DMPV_PATH = "./self-made-model/gold/dmpv/default_2022-06-03 01:54:52.150092.model"
GOLD_DMPV_RUN_PATH_DUMY = "./self-made-model/gold/dmpv/run_2022-06-03 02:53:25.816957.model"
GOLD_DMPV_EPOCH_20_RUN_PATH = "./self-made-model/gold/dmpv/epoch-20_run_2022-06-04 00:05:10.647523.model"
GOLD_DBOW_RUN_PATH_DUMY = "./self-made-model/gold/dbow/run_2022-06-07 02:03:39.770506.model"
GOLD_DMPV_RUN_PATH = "./self-made-model/gold/dmpv/dmpv_run_2022-06-07 02:15:22.389849.model"
GOLD_DBOW_RUN_PATH = "./self-made-model/gold/dbow/dbow_run_2022-06-07 02:17:35.553002.model"


METADATA_SHA_PATH = "./self-made-metadata/created/2022:05:21:22:32:53:0b-deduplicated-dockerfile-sources-sha"
SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/"
SELF_MADE_DATASETS_GITHUB_PATH = "./self-made-datasets/github/"
SELF_MADE_DATASETS_ORIGIN_PATH = "./self-made-datasets/origin/"

TEST_CASES = [
    ['SC-APK-ADD', 'SC-APK-F-NO-CACHE'],
    ['SC-APK-ADD', 'SC-APK-PACKAGES'],
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES'],
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS'],
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES'],
    ['SC-APT-GET-PURGE', 'SC-APT-GET-F-YES'],
    ['SC-APT-GET-PURGE', 'SC-APT-GET-F-AUTO-REMOVE'],
    ['SC-CHMOD', 'SC-CHMOD-MODE'],
    ['SC-CHMOD', 'SC-CHMOD-PATHS', 'SC-CHMOD-PATH', 'BASH-LITERAL'],
    ['SC-CHOWN', 'SC-CHOWN-OWNER', 'BASH-LITERAL'],
    ['SC-CHOWN', 'SC-CHOWN-PATHS', 'SC-CHOWN-PATH', 'BASH-LITERAL'],
    ['SC-CP-PATHS', 'SC-CP-PATH'],
    ['SC-CP-PATHS', 'SC-CP-PATH', 'BASH-LITERAL'],
    ['SC-CP-PATHS', 'SC-CP-PATH'],
    ['SC-CP-PATHS', 'SC-CP-PATH', 'BASH-LITERAL'],
    ['SC-CURL', 'SC-CURL-OUTPUT', 'BASH-PATH', 'BASH-LITERAL'],
    ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
    ['SC-CURL', 'SC-CURL-F-LOCATION'],
    ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL', 'ABS-PROBABLY-URL'],
    ['SC-CURL', 'SC-CURL-F-FAIL'],
    ['SC-CURL', 'SC-CURL-F-LOCATION'],
    ['SC-CURL', 'SC-CURL-URL', 'BASH-LITERAL'],
    ['BASH-LITERAL', 'ABS-PROBABLY-URL'],
    ['BASH-LITERAL', 'ABS-URL-PROTOCOL-HTTPS'],
    ['BASH-ASSIGN', 'BASH-ASSIGN-LHS'],
    ['BASH-ASSIGN', 'BASH-ASSIGN-RHS', 'BASH-DOUBLE-QUOTED'],
    ['BASH-ASSIGN', 'BASH-ASSIGN-LHS'],
    ['BASH-ASSIGN', 'BASH-ASSIGN-RHS', 'BASH-DOUBLE-QUOTED'],
    ['SC-FIND', 'SC-FIND-F-EXEC'],
    ['SC-FIND', 'SC-FIND-TARGET', 'BASH-LITERAL'],
    ['SC-FIND', 'SC-FIND-ARGS', 'SC-FIND-ARG', 'BASH-LITERAL'],
    ['SC-FIND', 'SC-FIND-ARGS', 'SC-FIND-ARG', 'BASH-SINGLE-QUOTED'],
    ['SC-FIND', 'SC-FIND-ARGS', 'SC-FIND-ARG'],
    ['SC-FIND-ARGS', 'SC-FIND-ARG', 'BASH-LITERAL'],
    ['SC-FIND-ARGS', 'SC-FIND-ARG', 'BASH-SINGLE-QUOTED'],
    ['SC-FIND-ARGS', 'SC-FIND-ARG'],
    ['SC-FIND-ES', 'SC-FIND-E', 'BASH-LITERAL', 'ABS-TRUE'],
    ['SC-FIND-ES', 'SC-FIND-E', 'BASH-LITERAL', 'ABS-TRUE'],
    ['SC-FIND-ES', 'SC-FIND-E', 'BASH-LITERAL', 'ABS-TRUE'],
    ['BASH-LITERAL', 'ABS-PROBABLY-URL'],
    ['BASH-LITERAL', 'ABS-URL-HA-POOL'],
    ['BASH-LITERAL', 'ABS-URL-POOL'],
    ['SC-GPG-VERIFYS', 'SC-GPG-VERIFY', 'BASH-LITERAL', 'ABS-EXTENSION-ASC'],
    ['SC-GPG-VERIFYS', 'SC-GPG-VERIFY', 'BASH-LITERAL'],
    ['SC-LN', 'SC-LN-F-SYMBOLIC'],
    ['SC-LN', 'SC-LN-TARGET', 'BASH-LITERAL'],
    ['SC-LN', 'SC-LN-LINK', 'BASH-LITERAL'],
    ['BASH-LITERAL', 'ABS-MAYBE-PATH'],
    ['BASH-LITERAL', 'ABS-PATH-ABSOLUTE'],
    ['BASH-LITERAL', 'ABS-MAYBE-SRC-DIR'],
    ['BASH-LITERAL', 'ABS-USR-SRC-DIR'],
    ['SC-MKDIR', 'SC-MKDIR-F-PARENTS'],
    ['SC-MKDIR', 'SC-MKDIR-PATHS', 'SC-MKDIR-PATH', 'BASH-LITERAL'],
    ['SC-SED', 'SC-SED-F-IN-PLACE'],
    ['SC-SED', 'SC-SED-EXPRESSIONS', 'SC-SED-EXPRESSION', 'BASH-LITERAL'],
    ['SC-SED', 'SC-SED-PATHS'],
    ['SC-SED', 'SC-SED-EXPRESSIONS', 'SC-SED-EXPRESSION', 'BASH-LITERAL'],
    ['SC-SED', 'SC-SED-PATHS', 'SC-SED-PATH', 'BASH-LITERAL'],
    ['SC-SET', 'SC-SET-F-E'],
    ['SC-SET', 'SC-SET-F-X'],
    ['SC-TAR', 'SC-TAR-X'],
    ['SC-TAR', 'SC-TAR-FILE', 'BASH-PATH', 'BASH-LITERAL', 'ABS-EXTENSION-TAR'],
    ['SC-WGET', 'SC-WGET-OUTPUT-DOCUMENT', 'BASH-PATH', 'BASH-LITERAL'],
    ['SC-WGET', 'SC-WGET-URL', 'BASH-LITERAL']
]

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

class D2V_VER2():
    @staticmethod
    def load(words):
        def op(flg):
            sha, hgs, wds = flg.split(":")
            file_path = "{}{}.json".format(SELF_MADE_DATASETS_GOLD_PATH, sha)
            with open(file_path, mode="r") as f:
                children = json.load(f)
            trs = dict()
            for hg, child in enumerate(children):
                tokens = Recursive.do(child)
                for wd, token in enumerate(tokens):
                    tr = {
                        "{}:{}:{}".format(sha, hg, wd) : token
                    }
                    trs.update(tr)

            for key, value in trs.items():
                if key == "{}:{}:{}".format(sha, hgs, wds):
                    print(value[2:])

        model = Doc2Vec.load(GOLD_DBOW_RUN_PATH)
        x = model.infer_vector(words)
        most_similar_texts = model.docvecs.most_similar([x])
        for similar_text in most_similar_texts:
            print(similar_text[1], " : ", similar_text[0])
            op(similar_text[0])

class D2V(object):
    def __init__(self, model_name):
        self._model_name = model_name
        self._model = Doc2Vec.load(model_name)

    def sim(self, words):
        x = self._model.infer_vector(words)
        most_similar_texts =  self._model.docvecs.most_similar([x])
        def res(val):
            sha, hw, ww = val.split(":")
            file_path = "{}{}.json".format(SELF_MADE_DATASETS_GOLD_PATH, sha)
            with open(file_path, mode="r") as f:
                children = json.load(f)
            tr_data = dict()
            for hg, child in enumerate(children):
                tokens = Recursive.do(child)
                for wd, token in enumerate(tokens):
                    tr = {
                        "{}:{}:{}".format(sha, hg, wd): token
                    }
                    tr_data.update(tr)
            
            res = [document[2:] for tag, document in tr_data.items() if tag == val]
            return res[0]
        results = list()
        for most_similar_text in most_similar_texts:
            result = res(most_similar_text[0])
            results.append(result)
        return results

class Test(object):
    @staticmethod
    def do():
        d2v = D2V(GOLD_DBOW_RUN_PATH)
        for test_case in TEST_CASES:
            print()
            print(test_case)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            results = d2v.sim(test_case)
            for result in results:
                print(result)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print()
    




def main():
    Test.do()



if __name__ == "__main__":
    main()
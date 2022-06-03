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
GOLD_DMPV_RUN_PATH = "./self-made-model/gold/dmpv/run_2022-06-03 02:53:25.816957.model"
GOLD_DMPV_EPOCH_20_RUN_PATH = "./self-made-model/gold/dmpv/epoch-20_run_2022-06-04 00:05:10.647523.model"


METADATA_SHA_PATH = "./self-made-metadata/created/2022:05:21:22:32:53:0b-deduplicated-dockerfile-sources-sha"
SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/"
SELF_MADE_DATASETS_GITHUB_PATH = "./self-made-datasets/github/"
SELF_MADE_DATASETS_ORIGIN_PATH = "./self-made-datasets/origin/"
"""
    - goldルールのみのファイルパスを取得するためのパス
"""
PATCH_GLOB_SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/**"

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

class D2V():
    @staticmethod
    def load():
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


        model = Doc2Vec.load(GOLD_DMPV_RUN_PATH)
        # words = ['BASH-SUBSHELL', 'SC-CONFIGURE', 'SC-CONFIGURE-WITH-JAVA-HOME', 'BASH-LITERAL']
        words = ['BASH-AND-IF', 'BASH-AND-MEM', 'SC-RM', 'SC-RM-F-FORCE']
        x = model.infer_vector(words)
        most_similar_texts = model.docvecs.most_similar([x])
        for similar_text in most_similar_texts:
            print(similar_text[1], " : ", similar_text[0])
            op(similar_text[0])



def main():
    D2V.load()


if __name__ == "__main__":
    main()
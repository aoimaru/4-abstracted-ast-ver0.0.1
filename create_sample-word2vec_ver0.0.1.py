import json
import copy
import pathlib
import os
from datetime import datetime
import sys
import glob
from gensim.models import word2vec
from gensim.models import KeyedVectors


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
    
def main():
    FILE_SHA_1 = "0aa1cd6a00cfe247f17e680d5e2c394b5f0d3edc"
    FILE_SHA_2 = "0b15d39cebd7afc18eded9d4f41d932b00770eed"
    FILE_SHA_3 = "0b687ec4b2f490051a53d114bf64242580c32f28"
    FILE_SHA_4 = "0b1975d451426f9858f59b812411970f4e2ac49c"

    ast_obj = BaseAST(FILE_SHA_3)
    children = ast_obj.children
    for child in children:
        if child["type"] == "DOCKER-RUN":
            tokens = Recursive.do(child)
            print()
            for token in tokens:
                print(token[2:])
    
    print()
    ast_obj = BaseAST(FILE_SHA_4)
    children = ast_obj.children
    for child in children:
        if child["type"] == "DOCKER-RUN":
            tokens = Recursive.do(child)
            print()
            for token in tokens:
                print(token[2:])





if __name__ == "__main__":
    main()
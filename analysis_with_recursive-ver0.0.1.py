import json
import pprint
import pathlib

import copy

"""
    - 定数周り
"""
METADATA_SHA_PATH = "./self-made-metadata/created/2022:05:21:22:32:53:0b-deduplicated-dockerfile-sources-sha"

SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/github/"


class MetaData(object):
    @staticmethod
    def get_sha():
        with open(METADATA_SHA_PATH, mode="r") as f:
            data = json.load(f)
        return data["file_sha"]

class BaseAST(object):
    def __init__(self, file_sha):
        file_path = "{}{}.json".format(SELF_MADE_DATASETS_GOLD_PATH, file_sha); file_path = str(pathlib.Path(file_path).resolve())
        with open(file_path, mode="r") as f:
            obj = json.load(f)
        self._children = obj
        
    @property
    def children(self):
        pass
    
    @children.getter
    def children(self):
        return self._children
    

class Recursive(object):
    @staticmethod
    def do(obj):
        """
            - シンプルな再帰
            - 深さ優先探索を行う
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
        
        for token in tokens:
            print(token)


def test():
    TEST_INDEX = 0
    file_sha = MetaData.get_sha()
    ast_obj = BaseAST(file_sha[TEST_INDEX])
    # パッチ
    # ast_obj = BaseAST("0b15d39cebd7afc18eded9d4f41d932b00770eed")
    children = ast_obj.children
    for child in children:
        print()
        if child["type"] == "DOCKER-RUN":
            Recursive.do(child)




def main():
    test()


if __name__ == "__main__":
    main()
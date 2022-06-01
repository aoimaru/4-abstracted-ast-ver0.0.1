import json
import copy
import pathlib


"""
    - 定数周り
"""
METADATA_SHA_PATH = "./self-made-metadata/created/2022:05:21:22:32:53:0b-deduplicated-dockerfile-sources-sha"
SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/"
SELF_MADE_DATASETS_GITHUB_PATH = "./self-made-datasets/github/"
SELF_MADE_DATASETS_ORIGIN_PATH = "./self-made-datasets/origin/"

class TR(object):
    pass
    @staticmethod
    def do(ast_obj, tr_data=dict()):
        children = ast_obj.children
        if not children:
            return
        for hg, child in enumerate(children):
            tokens = Recursive.do(child)
            for wd, token in enumerate(tokens):
                print(hg, wd, token)
                tr = {
                    "{}:{}:{}".format(ast_obj.file_sha, hg, wd) : token
                }
                tr_data.update(tr)
        return tr_data


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

class MetaData(object):
    @staticmethod
    def get_sha():
        with open(METADATA_SHA_PATH, mode="r") as f:
            data = json.load(f)
        return data["file_sha"]

class BaseAST(object):
    def __init__(self, file_sha):
        file_path = "{}{}.json".format(SELF_MADE_DATASETS_GITHUB_PATH, file_sha); file_path = str(pathlib.Path(file_path).resolve())
        with open(file_path, mode="r") as f:
            obj = json.load(f)
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
    TEST_INDEX = 18
    file_sha = MetaData.get_sha()
    tr_data = dict()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        tr_data = TR.do(ast_obj, tr_data)
    
    for key, value in tr_data.items():
        print(key, value)
    



if __name__ == "__main__":
    main()
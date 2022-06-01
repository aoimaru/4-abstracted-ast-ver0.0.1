
"""
    - これいらないかも
    - 使ってない
"""

import json
import pprint
import pathlib

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
    


class GoldAST(BaseAST):
    pass
    

class GitHubAST(BaseAST):
    pass



def main():
    file_sha = MetaData.get_sha()
    ast_obj = BaseAST(file_sha[0])
    children = ast_obj.children
    for child in children:
        print(child)




if __name__ == "__main__":
    main()
import json
import copy
import pathlib
import os
from datetime import datetime
import sys

import glob

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

"""
    - 定数周り
"""
METADATA_SHA_PATH = "./self-made-metadata/created/2022:05:21:22:32:53:0b-deduplicated-dockerfile-sources-sha"
SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/"
SELF_MADE_DATASETS_GITHUB_PATH = "./self-made-datasets/github/"
SELF_MADE_DATASETS_ORIGIN_PATH = "./self-made-datasets/origin/"

"""
    - goldルールのみのファイルパスを取得するためのパス
"""
PATCH_GLOB_SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/**"


class D2V(object):
    @staticmethod
    def do(training_data, min_count=100, dm=1, window=5, name="default", types="github"):
        """
            - モデルの作成
        """
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
        documents = [TaggedDocument(words=token, tags=[tag_name]) for tag_name, token in training_data.items()]
        pass
        model = Doc2Vec(
            documents=documents,
            min_count=min_count,
            dm=dm,
            window=window
        )
        if dm==1:
            model_name = "./self-made-model/{}/dmpv/{}_{}.model".format(types, name, current_time)
        else:
            model_name = "./self-made-model/{}/dbow/{}_{}.model".format(types, name, current_time)
        
        model.save(model_name)
    
    @staticmethod
    def epoch(training_data, min_count=100, dm=1, window=5, epochs=20, name="default", types="github"):
        """
            - epochでの実装, モデルの作成
        """
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
        documents = [TaggedDocument(words=token, tags=[tag_name]) for tag_name, token in training_data.items()]
        pass
        model = Doc2Vec(
            documents=documents,
            min_count=min_count,
            dm=dm,
            window=window
        )
        if dm==1:
            model_name = "./self-made-model/{}/dmpv/epoch-{}_{}_{}.model".format(types, epochs, name, current_time)
        else:
            model_name = "./self-made-model/{}/dbow/epoch-{}_{}_{}.model".format(types, epochs, name, current_time)
        
        alpha = 0.025
        alpha_delta = 0.001

        # los_vals = []
        for epoch in range(epochs):
            print("Epoch: {}".format(epoch + 1))
            model.alpha, model.min_alpha = alpha, alpha
            model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
            alpha -= alpha_delta
            # los_vals.append(model.get_latest_training_loss())
        
        model.save(model_name)
            

class TR(object):
    pass
    @staticmethod
    def do(ast_obj):
        children = ast_obj.children
        if not children:
            return None
        trs = dict()
        for hg, child in enumerate(children):
            tokens = Recursive.do(child)
            for wd, token in enumerate(tokens):
                tr = {
                    "{}:{}:{}".format(ast_obj.file_sha, hg, wd) : token
                }
                trs.update(tr)
        return trs
    
    @staticmethod
    def do_with_run(ast_obj):
        children = ast_obj.children
        if not children:
            return None
        trs = dict()
        for hg, child in enumerate(children):
            tokens = Recursive.do_with_run(child)
            for wd, token in enumerate(tokens):
                tr = {
                    "{}:{}:{}".format(ast_obj.file_sha, hg, wd) : token
                }
                trs.update(tr)
        return trs
                 
    @staticmethod
    def does():
        pass


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

    @staticmethod
    def do_with_run(obj):
        """
            - シンプルな再帰
            - 深さ優先探索を行う
            - ASTをDoc2Vecで受け入れられる最低限の形に持っていく
            - runのみを取得
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
        
        ZERO = 0
        res = list()
        for token in tokens:
            if token[ZERO] == "DOCKER-RUN":
                res.append(token[2:])
        
        return res
            


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
    

def test():
    tr_data = dict()
    file_sha = MetaData.patch()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        trs = TR.do_with_run(ast_obj)
        if trs:
            tr_data.update(trs)
    
    return tr_data



def main():
    tr_data = test()
    D2V.epoch(tr_data, min_count=100, dm=1, window=5, name="run", types="gold", epochs=20)
    
    
    



if __name__ == "__main__":
    main()
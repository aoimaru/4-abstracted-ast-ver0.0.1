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

        los_vals = []
        for epoch in range(epochs):
            print("Epoch: {}".format(epoch + 1))
            model.alpha, model.min_alpha = alpha, alpha
            model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
            alpha -= alpha_delta
            los_vals.append(model.get_latest_training_loss())
        
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
                print(token)
        #         tr = {
        #             "{}:{}:{}".format(ast_obj.file_sha, hg, wd) : token
        #         }
        #         trs.update(tr)
        # return trs
                 
    @staticmethod
    def patch(ast_obj):
        children = ast_obj.children
        if not children:
            return None
        tr_data = list()
        for child in children:
            if child["type"] == "DOCKER-RUN":
                tokens = Recursive.do(child)
                words = list()
                for token in tokens:
                    words.extend(token[2:])
                tr_data.append(words)
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


from gensim.models import word2vec


class W2V(object):
    @staticmethod
    def do(corpus, sg=1, size=100, min_count=100, window=5, name="default", types="github"):
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
        model = word2vec.Word2Vec(
            corpus,
            sg=sg,
            size=size, 
            min_count=min_count, 
            window=window
        )
        if sg==1:
            model_name = "./self-made-word2vec/{}/sg/{}_{}.model".format(types, name, current_time)
        elif sg==0:
            model_name = "./self-made-word2vec/{}/cbow/{}_{}.model".format(types, name, current_time)

        model.save(model_name)
    


def create_github_training_data() -> dict:
    file_sha = MetaData.get_sha()
    tr_data = dict()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        trs = TR.do(ast_obj)
        if trs:
            tr_data.update(trs)
    return tr_data

def check_num_of_gold_word():
    tr_data = dict()
    file_sha = MetaData.patch()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        trs = TR.do(ast_obj)
        if trs:
            tr_data.update(trs)
    
    cnt = 0
    for tr in tr_data.values():
        cnt += len(tr)

    print(cnt)

def create_gold_training_data() -> dict:
    tr_data = dict()
    file_sha = MetaData.patch()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        trs = TR.do(ast_obj)
        if trs:
            tr_data.update(trs)

    return tr_data

def create_gold_run_training_data() -> dict:
    tr_data = dict()
    file_sha = MetaData.patch()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        trs = TR.patch(ast_obj)
        if trs:
            tr_data.update(trs)

    return tr_data

def get_w2v_data(tr_data):
    training_data = list()
    for value in tr_data.values():
        if value[0] == "DOCKER-RUN":
            training_data.append(value[2:])
    return training_data

def patch():
    file_sha = MetaData.patch()
    training_data = list()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        tr_data = TR.patch(ast_obj)
        if tr_data:
            for tr in tr_data:
                if tr:
                    if not tr[0] == "UNKNOWN":
                        training_data.append(tr)
    return training_data

def patches():
    file_sha = MetaData.get_sha()
    training_data = list()
    for sha in file_sha:
        ast_obj = BaseAST(sha)
        tr_data = TR.patch(ast_obj)
        if tr_data:
            for tr in tr_data:
                if tr:
                    if not tr[0] == "UNKNOWN":
                        training_data.append(tr)
    return training_data

def main():
    training_data = patches()
    # print(len(training_data))
    W2V.do(corpus=training_data, sg=1, size=100, min_count=20, window=5, name="06001332_min_count_20", types="github")
    # file_sha = MetaData.get_sha()
    # print(len(file_sha))

    

if __name__ == "__main__":
    main()
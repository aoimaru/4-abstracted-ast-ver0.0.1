import pandas as pd
import pathlib
import datetime
import json

import pprint

"""
    - 定数周り
"""
GITHUB_JSONL_PATH = "./original-datasets/github.jsonl"
GOLD_JSONL_PATH = "./original-datasets/gold.jsonl"
SELF_MADE_DATASETS_PATH = "./self-made-datasets/"
SELF_MADE_PICKLE_PATH = "./self-made-pickle/"

"""
    - pickleの定数周り
"""
PICKLE_OBJECT_GITHUB_VER001 = "./self-made-pickle/github/2022:05:26:14:57:50.pkl"
PICKLE_OBJECT_GOLD_VER001 = "./self-made-pickle/gold/2022:05:26:15:39:54.pkl"

"""
    - self-made系
"""
SELF_MADE_DATASETS_GOLD_PATH = "./self-made-datasets/gold/"
SELF_MADE_DATASETS_GITHUB_PATH = "./self-made-datasets/github/"

class ReadJSONL(object):
    """
        - 初期パッチ
    """
    @staticmethod
    def do(file_path):
        file_path = pathlib.Path(file_path).resolve()
        return pd.read_json(file_path, orient='records', lines=True)
    """
        - pandasの動作確認のパッチ
    """
    @staticmethod
    def patch(file_path):
        file_path = pathlib.Path(file_path).resolve()
        return pd.read_json(file_path, orient='records', lines=True)[:10]

class PickleJSONL(object):
    """
        - 初期パッチ
    """
    @staticmethod
    def to_github(df):
        dt_now = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
        file_path = str(pathlib.Path(SELF_MADE_PICKLE_PATH).resolve())
        file_name = "/github/{}.pkl".format(dt_now)
        df.to_pickle(file_path+file_name)
    @staticmethod
    def to_gold(df):
        dt_now = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
        file_path = str(pathlib.Path(SELF_MADE_PICKLE_PATH).resolve())
        file_name = "/gold/{}.pkl".format(dt_now)
        df.to_pickle(file_path+file_name)

class ReadPickle(object):
    @staticmethod
    def read(pickle_path):
        return pd.read_pickle(pickle_path)


class SelfMadeGitHub(object):
    pass
    @staticmethod
    def do(row):
        file_sha = row["file_sha"]; children = row["children"]
        file_path = SELF_MADE_DATASETS_GITHUB_PATH+"{}.json".format(file_sha)
        with open(file_path, mode="w") as f:
            json.dump(children, f, ensure_ascii=False, indent=4)
            

class SelfMadeGold(object):
    @staticmethod
    def do(row):
        file_sha = row["file_sha"]; children = row["children"]
        file_path = SELF_MADE_DATASETS_GOLD_PATH+"{}.json".format(file_sha)
        with open(file_path, mode="w") as f:
            json.dump(children, f, ensure_ascii=False, indent=4)

def exec_gold():
    jsonl_obj = ReadPickle.read(PICKLE_OBJECT_GOLD_VER001)
    for _, row in jsonl_obj.iterrows():
        SelfMadeGold.do(row)

def exec_github():
    jsonl_obj = ReadPickle.read(PICKLE_OBJECT_GITHUB_VER001)
    for _, row in jsonl_obj.iterrows():
        SelfMadeGitHub.do(row)


def main():
    """
        この部分"ReadJSONL.do(); PickleJSONL.do(jsonl_obj)"はできれば実行したくない 初期パッチ
        - jsonl_obj = ReadJSONL.do(GITHUB_JSONL_PATH)
        - PickleJSONL.do(jsonl_obj)
    """
    """
        - jsonl_obj = ReadJSONL.do(GOLD_JSONL_PATH)
        - PickleJSONL.to_gold(jsonl_obj)
    """
    exec_github()

    

if __name__ == "__main__":
    main()
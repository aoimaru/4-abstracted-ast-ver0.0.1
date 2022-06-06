import json
import copy
import pprint

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


def main():
    PROGRESS_REPORT_0609 = "./self-made-datasets/gold/ff952dd922c364107cfccba49c45c0ce2a379c12.json"
    with open(PROGRESS_REPORT_0609, mode="r") as f:
        objs = json.load(f)
    for obj in objs:
        print()
        tokens = Recursive.do(obj)
        for token in tokens:
            print(token[2:])





if __name__ == "__main__":
    main()
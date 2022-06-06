import json
import copy

MINED_RULES_EXAMPLE_PATH = "./self-made-datasets/mined-rules-example-ver0.0.1.json"



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
    with open(MINED_RULES_EXAMPLE_PATH, mode="r") as f:
        objs = json.load(f)
    for idx, obj in enumerate(objs):
        print("number: {}".format(idx+1))
        tokens = Recursive.do(obj)
        for token in tokens:
            print(token)




if __name__ == "__main__":
    main()
#CommandCompilerデバッグ用スクリプト

import sys

import CommandReverseCompiler
import CommandCompiler


def diff(rc, org, compiled):
    #行番号以外無視してコンパイル内容が同一かどうかの比較テストを行う
    #print(compiled)
    if len(org) != len(compiled):
        print("script length not match: org(%d), recompiled(%d)" % (len(org), len(compiled)))
        return False
    for org_p, compiled_p in zip(org, compiled):
        #print(org_p)
        #print(compiled_p)
        if org_p["commandId"] != compiled_p["commandId"]:
            print("commandId not match(line:%d)" % org_p["lineNumber"])
            print(org_p, "\n", compiled_p)
            print(rc.eval_command(org_p))
            return False
        elif len(org_p["parameters"]) != len(compiled_p["parameters"]):
            print("parameters length not match(line:%d)" % org_p["lineNumber"])
            print(org_p, "\n", compiled_p)
            print(rc.eval_command(org_p))
            return False
        for org_pp, compiled_pp in zip(org_p["parameters"], compiled_p["parameters"]):
            if org_pp["ParameterType"] != compiled_pp["ParameterType"]:
                print("ParameterType not match(line:%d)" % org_p["lineNumber"])
                print(org_pp, "\n", compiled_pp)
                print(rc.eval_command(org_p))
                return False
            elif org_pp["rawData"] != compiled_pp["rawData"]:
                print("rawData not match(line:%d)" % org_p["lineNumber"])
                print(org_pp, "\n", compiled_pp)
                print(rc.eval_command(org_p))
                return False
            elif org_pp["rawType"] != compiled_pp["rawType"]:
                print("rawType not match(line:%d)" % org_p["lineNumber"])
                print(org_pp, "\n", compiled_pp)
                print(rc.eval_command(org_p))
                return False
    return True

def main(key=None):
    rc = CommandReverseCompiler.ReverseCompiler()
    c = CommandCompiler.Compiler()
    rc.load_script("ScriptDataContainer.bytes")
    if key is None:
        keys = rc.keys()
    else:
        keys = [key]
    for key in keys:
        print("[%s]" % key)
        rc.eval_by_key(key=key)
        scr = rc.print(no_print=True)
        org = rc.select_by_key(key=key)["value"]["commands"]
        compiled = c.compile_script(scr[scr.index("\n"):])
        if not diff(rc, org, compiled):
            return
        #exit()
    print("compare test passed.")


if __name__ == "__main__":
    try:
        key = sys.argv[1]
    except IndexError:
        key = None
    main(key)
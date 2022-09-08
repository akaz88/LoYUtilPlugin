"""
scriptdata_assets_all.bundle内のScriptDataContainer.bytes逆コンパイラ
スクリプトがデカすぎてWindowsのPythonだとjsonの読み込みでコケるかも


ScriptDataContainer.bytesの中身

先頭4バイト分謎データの詰まったJSONファイル。
{"container":
    {"pairs":
        [{"key": "<ラベル名>"
          "value":
            {"commands":
                [{"commandId": <コマンドID>
                  "lineNumber": <元のスクリプトの行番号？(デバッグ用？)>
                  "parameters":
                    [{"ParameterType": <スクリプトエンジン上でのパラメータの型>
                      "rawData": <データ>
                      "rawType": <rawDataのTypeCode>
                     }, ...
                    ]
                 }, ...
                ]
            },
         },
        ], ...
    }
}

lineNumberはdnSpyで参照を探してもデバッグ用と思しき箇所でしか使用されていなかった
おそらく元のスクリプトでの行番号であると思われる
"""
import json
import os.path
import pprint
import sys

import commandlist


class ReverseCompiler:

    def __init__(self):
        self.pdict = {}
        self.compiled = {}
        self.decoded = {}
        self.printable = ""

    def eval_expression_value(self, parameters, i, rng):
        #["container"]["pairs"][n]["value"]["commands"][m]["parameters"]
        #このうち特にExpressionValueTypeの逆コンパイルを行う
        l = [commandlist.expval_t[int(parameters[i]["rawData"])]]
        cnv = {
            "Int": lambda x: int(x),
            "Float": lambda x: float(x),
            "Bool": lambda x: bool(x),
            "String": lambda x: str(x)
        }
        tps = commandlist.expval_args[int(parameters[i]["rawData"])]
        if tps:
            for tp in tps:
                """
                p = parameters[rng.__next__()]["rawData"]
                if not isinstance(tp, str) or tp == str:
                    s = cnv[tp](p)
                else:
                    if tp == "flag":
                        s = "flag(%s)" % commandlist.flags[int(p)]
                    else:
                        s = "%s(%s)" % (tp, str(p))
                l.append(str(s))
                """
                l.append(self.eval_parameter(parameters[rng.__next__()]))
        #print(l)
        s = ":".join(l)
        self.decoded = s
        return s

    def eval_parameter(self, parameter=None):
        #["container"]["pairs"][n]["value"]["commands"][m]["parameters"]
        if parameter is None:
            parameter = self.compiled

        if parameter["ParameterType"] == 0:
            #string
            s = '"%s"' % parameter["rawData"]
            self.decoded = s
            return s
        elif parameter["ParameterType"] in (1, 2, 3, 51, 52):
            #bool, int, float, ExpressionInt
            s = parameter["rawData"]
            self.decoded = s
            return s
        elif parameter["ParameterType"] == 8:
            #ScriptFlagId
            try:
                s = "flag(%s)" % commandlist.flags[int(parameter["rawData"])]
            except KeyError:
                #ゲーム内で定義されていないフラグIDはそのまま数字で出す
                s = "flag(%d)" % int(parameter["rawData"])
            self.decoded = s
            return s
        elif parameter["ParameterType"] == 49:
            #Operator
            s = commandlist.operator[int(parameter["rawData"])]
            self.decoded = s
            return s
        elif parameter["ParameterType"] == 50:
            #ExpressionValueType
            #ここには到達しないはず
            raise KeyError
            #s = commandlist.expval_t[int(parameter["rawData"])]
            #self.decoded = s
            #return s
        else:
            s = "%s(%s)" % (commandlist.parameter_t[parameter["ParameterType"]], parameter["rawData"])
            self.decoded = s
            return s

    def eval_parameters(self, parameters=None):
        if parameters is None:
            parameters = self.compiled
        l = []
        prev_parameter = None
        rng = iter(range(len(parameters)))
        try:
            while True:
                i = rng.__next__()
                p = parameters[i]
                if p["ParameterType"] == 50:
                    r = self.eval_expression_value(parameters, i, rng)
                else:
                    r = self.eval_parameter(p)
                l.append(r)
        except StopIteration:
            pass
        self.decoded = l
        return l

    def eval_command(self, command=None):
        if command is None:
            command = self.compiled
        #["container"]["pairs"][n]["value"]["commands"][{}, ...]
        d = {}
        cmdid = ""
        for k, v in command.items():
            #print(k, v)
            if k == "commandId":
                d[k] = commandlist.command[v]
                cmdid = v
            if k == "lineNumber":
                d[k] = v
            if k == "parameters" and v:
                d[k] = self.eval_parameters(v)
        if "parameters" in d:
            result = "%s:%s" % (d["commandId"], ":".join(d["parameters"]))
        else:
            result = "%s" % d["commandId"]
        #if self.with_lineno:
        result = result + ";%s" % d["lineNumber"]

        #print(result)
        self.decoded = result
        return result

    def eval_commands(self, commands=None):
        #["container"]["pairs"][n]["value"]["commands"]
        if commands is None:
            commands = self.compiled
        l = []
        for cmd in commands:
            l.append(self.eval_command(cmd))
        self.decoded = l
        return l

    def eval_value(self, value=None):
        #["container"]["pairs"][n]["value"]
        if value is None:
            value = self.compiled
        d = {}
        for k, v in value.items():
            if k == "commands":
                d[k] = self.eval_commands(v)
            else:
                print("[eval_value]unknown keyword: %s: %s" % (k, v))
        self.decoded = d
        return d

    def eval_pair(self, pair=None):
        #["container"]["pairs"][n]
        if pair is None:
            pair = self.compiled
        d = {}
        for k, v in pair.items():
            if k == "key":
                d[k] = v
            elif k == "value":
                #pprint.pp(v)
                d[k] = self.eval_value(v)
        self.decoded = d
        return d

    def eval_pairs(self, pairs=None):
        #["container"]["pairs"]
        if pairs is None:
            pairs = self.compiled
        l = []
        for pair in pairs:
            l.append(self.eval_pair(pair))
        self.decoded = l
        return l

    def eval_container(self, container=None):
        #["container"]
        if container is None:
            container = self.compiled
        d = {}
        for k, v in container.items():
            if k == "pairs":
                d[k] = self.eval_pairs(v)
            else:
                print("[eval_container]unknown keyword: %s" % k)
        self.decoded = d
        return d

    def eval_script(self, script=None):
        #scriptをそのままぶち込んで解釈
        if script is None:
            script = self.compiled
        d = {}
        for k, v in script.items():
            if(k == "container"):
                d[k] = self.eval_container(v)
            else:
                print("[eval_script]unknown keyword: %s" % k)
        self.decoded = d
        return d

    def eval(self, script=None):
        #どのレベルのスクリプトも一発で逆コンパイル
        if script is None:
            script = self.compiled
        if "container" in script:
            self.eval_script(script)
        elif "pairs" in script:
            self.eval_container(script)
        elif "key" in script:
            self.eval_pair(script)
        elif "commands" in script:
            self.eval_value(script)
        elif "commandId" in script:
            self.eval_command(script)
        elif "ParameterType" in script:
            self.eval_parameter(script)
        elif isinstance(script, list):
            if "key" in script[0]:
                self.eval_pairs(script)
            elif "commandId" in script[0]:
                self.eval_commands(script)
            elif "ParameterType" in script[0]:
                self.eval_parameters(script)
        return self.decoded

    def keys(self):
        #ScriptDataContainer.bytesからkey一覧を返す
        l = []
        for d in self.compiled["container"]["pairs"]:
            l.append(d["key"])
        return l

    def select_by_key(self, script="", key=0):
        #keyに指定したpairを返す
        if not script:
            script = self.compiled
        #print(key)
        if isinstance(key, int):
            try:
                return script["container"]["pairs"][key]
            except IndexError:
                print("not found.")
                #self.decoded = {}
                return {}
        for d in script["container"]["pairs"]:
            if d["key"] == key:
                break
        else:
            print("%s is not valid key." % key)
            raise IndexError(key)
        #self.decoded = d
        return d

    def eval_by_key(self, script="", key=0):
        #keyに指定したpairを逆コンパイル
        if not script:
            script = self.compiled
        self.decoded = self.eval_pair(self.select_by_key(script, key))
        return self.decoded

    def load_script(self, scfile="ScriptDataContainer.bytes"):
        #コンパイル済みスクリプトをロードする
        if not os.path.exists(scfile):
            print("%s not found." % scfile)
            exit(-1)
        with open(scfile, "rb") as f:
            buf = f.read()
        i = 0
        while(buf[i] != ord("{")):
            i += 1
            if i > 10:
                print("%s is not valid script??" % scfile)
                exit()
        self.compiled = json.loads(buf[i:])
        return self.compiled
        #return json.loads(open(scfile, "rb").read()[4:])

    def dump_script(self, printable="", outpath="o.txt", force=False):
        #ファイルに出力
        if not printable:
            if self.printable:
                printable = self.printable
            else:
                printable = self.print(no_print=True)
        if os.path.exists(outpath) and not force:
            print("%s already exist." % outpath)
            return
        with open(outpath, "wt") as f:
            f.write(printable)
            f.truncate()

    def print(self, script="", no_print=False):
        #逆コンパイルされたスクリプトをprintする
        if not script:
            script = self.decoded
        s = ""
        depth = 0
        indent = lambda x: " " * 4 * x
        if isinstance(script, list):
            cp = script[0:]
        else:
            cp = script.copy()

        def print_pair(pair, depth):
            #flg = False
            s = ""
            s += "%skey: %s\n" % (indent(depth), pair["key"])
            for i in range(len(pair["value"]["commands"])):
                cmd = pair["value"]["commands"][i]
                #ncmd = pair["value"]["commands"][(i + 1) if i + 1 < len(pair["value"]["commands"]) else i]
                if cmd.startswith("_endif") or cmd.startswith("_else") or cmd.startswith("_show_selection"):
                    depth -= 1
                cmd, lineno = cmd.split(";")
                s += "%s[%s]%s\n" % (indent(depth), lineno, cmd)
                if cmd.startswith("_if") or cmd.startswith("_else") or cmd.startswith("_start_selection"):
                    depth += 1
                #きったねえ解決法
                #if cmd.startswith("_decided_selection") or cmd.startswith("_canceled_selection"):
                    #depth += 1
                #elif ncmd.startswith("_decided_selection") or ncmd.startswith("_canceled_selection") or ncmd.startswith("_end_selection"):
                    #if not flg:
                        #depth += 1
                    #flg = True
                    #depth -= 1
            depth -= 1
            return s

        if "container" in cp:
            s += "container\n"
            depth += 1
            cp = cp["container"]
        if "pairs" in cp:
            s += "%spairs\n" % indent(depth)
            depth += 1
            cp = cp["pairs"]
        if isinstance(cp, list):
            for d in cp:
                s += print_pair(d, depth)
        elif "key" in cp:
            s += print_pair(cp, depth)
        if not no_print:
            print(s)
        self.printable = s
        return s


def rcompile(compiled, raw_scr, key=None, force=False, no_print=False):
    if not os.path.exists(compiled):
        print("%s is not exist." % compiled)
        return
    if raw_scr != "stdout" and not force and os.path.exists(raw_scr):
        print("%s is already exist." % raw_scr)
        return
    if raw_scr == "stdout":
        no_print = False
    rc = ReverseCompiler()
    rc.load_script(compiled)

    if key is not None:
        rc.eval_by_key(key=key)
    else:
        rc.eval()

    rc.print(no_print=no_print)
    if raw_scr != "stdout":
        rc.dump_script(rc.printable, raw_scr, force=force)


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help", "/?"):
        print("CommandReverseCompiler.py <in> <out> [-f/--force] [--key=SCRIPT_NAME] [--no-print]")
        exit()
    compiled = sys.argv[1]
    raw_scr = sys.argv[2]
    if raw_scr == compiled:
        print("input and output are same path.")
        exit()
    force = False
    key = None
    no_print = False
    if len(sys.argv) > 3:
        for a in sys.argv[3:]:
            if a in ("-f", "--force"):
                force = True
            elif a.startswith("--key="):
                key = a[6:]
            elif a == "--no-print":
                no_print = True
            else:
                print("invalid argument : %s" % a)
                exit()
    rcompile(compiled, raw_scr, key=key, force=force, no_print=no_print)

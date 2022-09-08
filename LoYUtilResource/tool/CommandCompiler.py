import json
import os.path
import pprint
import re
import sys

import ply.lex

import commandlist


#このコンパイラでコンパイルしたスクリプトは開始行をLINE_BASE行目とする
#こうしないと一つのスクリプトに対し複数の行指定でのスクリプトの挿入がなされた場合に衝突の危険がある
#LINE_BASEは衝突を回避するために任意の数に置き換えて良い
LINE_BASE=10000

#このコンパイラでコンパイルしたスクリプトが特別な制限のない際に指定する最初のScriptFlagId
#--ex-flagpthオプションが指定されない場合などにもこのScriptFlagIdが使用される
#すると当然、フラグIDが被ってしまい、スクリプトの実行に影響が出ることが考えられる
exflag_base = 2000

dict_reverse = lambda x, y=True: {v: str(k) if y else k for k, v in x.items()}

r_command = dict_reverse(commandlist.command, False)
r_operator = dict_reverse(commandlist.operator)
r_parameter_t = dict_reverse(commandlist.parameter_t, False)
r_raw_t = dict_reverse(commandlist.raw_t, False)
r_expval_t = dict_reverse(commandlist.expval_t)
r_flags = dict_reverse(commandlist.flags)
parameter_cnv = dict([(k, r_raw_t[v]) for k, v in commandlist.parameter_type.items()])


class Lexer:
    tokens = (
        "COMMAND",
        "SEP",
        "PARAM",
        "COMMENT"
    )

    t_COMMAND = "_[_a-z]+"
    t_SEP = ":"
    t_PARAM = "[^_\: \[\t\n\r\f\v][^\: \t\n\r\f\v]*"
    t_ignore = " \t"
    t_ignore_LineNo = r"\[[0-9]+\]"

    def t_newline(self, t):
        r"\r?\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("error: %s" % t.value[0])
        t.lexer.skip(1)

    def t_COMMENT(self, t):
        r';.*'
        t.lexer.lineno += t.value.count('\n')

    def __init__(self):
        self.lexer = ply.lex.lex(module=self)

    def input(self, script):
        self.lexer.input(script)
        return self

    def do(self):
        for tok in self.lexer:
            yield tok


class Compiler:

    def __init__(self, ex_flag_path=""):
        self.exflag_path = ex_flag_path
        self.exflags = self.load_exflag()
        self.exflags_changed = False

    def __del__(self):
        self.save_exflag()

    def load_exflag(self):
        if not os.path.exists(self.exflag_path):
            return {}
        with open(self.exflag_path, "rt") as f:
            l = f.read().split(",")
        d = {}
        for p in l:
            if ":" not in p:
                continue
            k, v = p.split(":")
            d[k] = int(v)
        return d

    def save_exflag(self):
        if self.exflag_path == "" or not self.exflags_changed:
            return
        s = ""
        for k, v in self.exflags.items():
            s += "%s:%s," % (k, v)
        if s == "":
            return
        s = s[:-1]
        with open(self.exflag_path, "wt") as f:
            f.write(s)
            f.truncate()

    def cmd_encode(self, cmd):
        return r_command[cmd]

    def handle_exflag(self, flg):
        if flg not in self.exflags:
            if not self.exflags:
                self.exflags[flg] = exflag_base
            else:
                self.exflags[flg] = max(self.exflags.values()) + 1
            self.exflags_changed = True
        return self.exflags[flg]

    def encode_flag(self, flg):
        if flg in r_flags:
            return r_flags[flg]
        else:
            return self.handle_exflag(flg)

    def get_pdict(self, v, tp):
        #print(v, tp)
        need_strippting = ("TextId", "Align", "ScriptFlagId", "ImageShowType", "ImageHideType", "BackgroundData", "NpcBustData", "NpcFacialExpressionId", "NpcBustPositionId", "EventImageData", "CevData", "CevPositionId", "EnemyData", "EnemyGraphicData", "EnemyAppearType", "EnemyDisappearType", "MusicResourceData", "SoundResourceData", "VideoResourceData", "EffectData", "FacilityId", "ItemData", "DungeonId", "SectorData", "DungeonEntranceId", "MapSymbolType", "QuestData", "QuestState", "ConfirmedEncounterData", "CityEncounterData", "ConfirmedDropData", "ItemInventoryType", "DirectionType", "GraphicsSortOrderId", "ScenarioWindowPositionType", "LuminanceLevel", "TransitionType", "BaseClassId", "AchievementData", "AfterAnnihilatedType", "BelongingsInventoryType", "AdditionalContentsId", "ExpressionArgument")
        pat = re.compile("(?<=\()[\s]*(?P<id>[^\s^)]+)")
        if tp == "String":
            #出力の際に付与されるので前後の引用符を外す
            v = v[1:-1]
        elif tp in need_strippting:
            mat = pat.search(v)
            #TextId(ID)のような形式からIDを抜き出す
            #IDベタ書きの場合はそのまま使用
            if mat:
                if tp == "ScriptFlagId" or v.startswith("flag("):
                    v = self.encode_flag(mat.groupdict()["id"])
                else:
                    v = mat.groupdict()["id"]
                #v = mat.groupdict()["id"]
            #if tp == "ScriptFlagId" or v.startswith("flag("):
            #if tp == "ScriptFlagId":
                #v = self.encode_flag(v)
        elif tp == "ExpressionOperator":
            v = r_operator[v]
        elif tp == "ExpressionValueType":
            v = r_expval_t[v]
        return {
            "rawData": v,
            "ParameterType": r_parameter_t[tp],
            "rawType": parameter_cnv[tp]
        }

    def parse_expression(self, param):
        #ExpressionIntとして扱われるパラメータはあくまで演算結果であるので、ここで演算子とその引数をエンコードする
        #_ifコマンドを例に取るとExpressionIntの形式は概ね以下の通り
        #_if:ScriptFlag:flag(ALWAYS)
        #_if:!:ScriptFlag:flag(ALWAYS)
        #_if:15:=:1
        #_if:Progress:=:11
        #_if:ScriptFlag:flag(STAY_LUKI_REACTOR):|:ScriptFlag:flag(STAY_HANBA_REACTOR):|:ScriptFlag:flag(STAY_HAIJUZI_REACTOR)
        l = []
        while param:
            v = param.pop(0)
            try:
                np = param[0]
            except IndexError:
                np = None
            if v in r_operator:
                #ExpressionOperator
                l.append(self.get_pdict(v, "ExpressionOperator"))
                if np is None:
                    print("Error: nothing arfter '%s' operator." % v)
                    print(self.current_line)
                    exit(-1)
            elif v in r_expval_t:
                #ExpressionValueType
                l += self.parse_expression_value(param, expval=v)
            else:
                #ExpressionInt
                l.append(self.get_pdict(v, "ExpressionInt"))
                if np not in r_operator:
                    break
        return l

    def parse_expression_value(self, param, expval=None):
        #ExpressionValueTypeを引数リストに基づいてエンコードする
        if expval is None:
            expval = param.pop(0)
        l = [self.get_pdict(expval, "ExpressionValueType")]
        expval = int(l[0]["rawData"])

        arglist = commandlist.expval_args[expval]
        if arglist is None:
            return l
        elif len(param) < len(arglist):
            print("Error: length param(%d) < arglist(%d)" % (len(param), len(arglist)))
            print(self.current_line)
            exit(-1)

        for tp in arglist:
            l.append(self.get_pdict(param.pop(0), tp))
        return l

    def parse_by_list(self, param, arglist):
        #引数リストを使ったパラメータのエンコード
        l = []
        #print(param)
        #print(arglist)
        for tp in arglist:
            if not param:
                print("Error: param is empty.")
                print(self.current_line)
                print(arglist)
                exit(-1)
            #ExpressionIntはExpressionValueType+引数に変更できることに注意
            #便宜上commandlist.command_argsはExpressionValueType+引数を取るようなコマンドであっても引数をExpressionInt扱いにしている
            if tp == "ExpressionInt":
                l += self.parse_expression(param)
                continue
            elif tp == ("ExpressionArgument", "ExpressionValueType"):
                #到達するはずのないコード
                print("Error: %s used independently(%s)", (tp, param.pop(0)))
                print(self.current_line)
                exit(-1)
            else:
                l.append(self.get_pdict(param.pop(0), tp))
        if param:
            print("Error: length missmatch between param and arglist")
            print(arglist, param)
            print(self.current_line)
        return l

    def parse_excommand_params(self, param):
        #拡張コマンドのパラメータのエンコード
        #自由に定義できるためここでは正確な引数リストの定義不能
        #Stringで確定している第一引数以外は適当に引数リストを作ることに
        #そのため、条件式はうまくエンコードできないため、C#側で対応する必要がある
        arglist = ["String"]
        l = param[1:]
        while l:
            p = l.pop(0)
            if p in r_expval_t:
                arglist.append("ExpressionValueType")
                a = commandlist.expval_args[p]
                #ExpressionValueTypeが引数を取るならその分も引数リストに追加してパラメータから減ずる
                if a:
                    if len(l) < len(a):
                        print("Error: length missmatch between param and argument list.")
                        print(self.current_line)
                        exit(-1)
                    arglist += a
                    l = l[len(a):]
            elif p in r_operator:
                arglist.append("ExpressionOperator")
            elif p.startswith("flag"):
                arglist.append("ScriptFlagId")
            elif p.split("(")[0] in r_parameter_t:
                arglist.append(p.split("(")[0])
            elif p in ("True", "true", "False", "false"):
                arglist.append("Bool")
            else:
                try:
                    #Float
                    float(p)
                    arglist.append("Float")
                except ValueError:
                    try:
                        #Int
                        int(p)
                        arglist.append("Int")
                    except ValueError:
                        #String
                        arglist.append("String")
        return self.parse_by_list(param, arglist)

    def parse_params(self, cmd, param, lineno):
        #パラメーターのエンコード
        if param:
            self.current_line = "[%s]%s:%s" % (lineno, cmd, ":".join(param))
        else:
            self.current_line = "[%s]%s" % (lineno, cmd)
        #print(self.current_line)

        if cmd == "_load_enemy_line":
            #可変長引数: ラインID(0/1), EnemyData, EnemyData, ...
            arglist = ["Int"] + ["EnemyData"] * (len(param) - 1)
            return self.parse_by_list(param, arglist)
        elif cmd == "_excmd":
            #可変長引数: "拡張コマンド名", param1, param2, ...
            return self.parse_excommand_params(param)
        else:
            try:
                arglist = commandlist.command_args[cmd]
            except KeyError:
                if cmd in r_command:
                    print("NotImplemented: %s command's parameter is unknown." % cmd)
                else:
                    print("Error: %s is unknown command." % cmd)
                exit(-1)
            return self.parse_by_list(param, arglist)

    def compile_script(self, script):
        #スクリプト本体のコンパイルを行う
        o = []
        cmd = ""
        lineno = 0
        param = []
        #print("script\n", script)
        for tok in Lexer().input(script).do():
            #print("tok: %s(%s)" % (tok.value, tok.type))
            if not tok:
                o.append({"commandId": cmd, "lineNumber": lineno, "parameters": param})
                break
            elif tok.type == "COMMAND":
                #cmd = self.cmd_encode(tok.value)
                cmd = tok.value
                lineno = tok.lineno + LINE_BASE
                param = []
                o.append({"commandId": cmd, "lineNumber": lineno, "parameters": param})
            elif tok.type == "SEP":
                pass
            elif tok.type == "PARAM":
                param.append(tok.value)
        #print(o)
        for d in o:
            d["parameters"] = self.parse_params(d["commandId"], d["parameters"], d["lineNumber"])
            d["commandId"] = self.cmd_encode(d["commandId"])
        return o


def compiler(raw_scr, odir, ex_flag_path=""):
    if not os.path.exists(raw_scr):
        print("%s is not exist." % raw_scr)
        return
    if odir != "stdout" and (not os.path.exists(odir) or not os.path.isdir(odir)):
        print("%s must be directory." % odir)
        return

    buf = open(raw_scr, "rt", encoding="utf-8").read()
    #複数のスクリプトファイルを一個ずつに分解する
    pat = re.compile(r"(?P<type>replace-all|insert:\d+|replace:\d+-\d+).*?key\s*:\s*(?P<key>\S+).*?(?P<script>.+?)", re.S)
    l = []
    mat = pat.search(buf)
    d = mat.groupdict()
    buf = buf[mat.span()[1]:]
    while True:
        mat = pat.search(buf)
        if not mat:
            d["script"] = buf
            l.append(d)
            break
        else:
            d["script"] = buf[:mat.span()[0]]
            l.append(d)
        d = mat.groupdict()
        buf = buf[mat.span()[1]:]
    if len(l) == 0:
        print("injection type not found.")
        return

    c = Compiler(ex_flag_path)
    for d in l:
        if d["type"].startswith("replace:"):
            l_from, l_to = d["type"][8:].split("-")
            if int(l_from) > int(l_to):
                print("replace linenumber invalid(from:%s > to%s)" % (l_from, l_to))
                return
        o = "%s\n%s" % (d["type"], json.dumps({"key": d["key"], "value" : {"commands": c.compile_script(d["script"])}}))
        if odir == "stdout":
            pprint.pp(o)
        else:
            opath = os.path.join(odir, "%s.%s.esc" % (d["key"], d["type"].replace(":", "：")))
            with open(opath, "wt") as f:
                f.write(o)


if __name__ == "__main__":
    #c = Compiler()
    #s = """
    #_if:ItemListDecidedItemId:=:ItemId:1007
        #_change_script:"GoldenHourglass"
    #_endif
    #"""
    #pprint.pp(c.compile_script(s))
    #exit()
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help", "/?"):
        print("CommandCompiler.py <in> <out_dir> [--ex-flagpath=flagpath]")
        exit()
    raw_scr = sys.argv[1]
    odir = sys.argv[2]
    ex_flag_path = ""
    if len(sys.argv) > 3:
        for a in sys.argv[3:]:
            if a.startswith("--ex-flagpath="):
                ex_flag_path = a.split("=", maxsplit=2)[1]
            else:
                print("invalid argument : %s" % a)
                exit()
    compiler(raw_scr, odir, ex_flag_path=ex_flag_path)

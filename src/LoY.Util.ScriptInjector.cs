using System;
using System.IO;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* 外部ファイルをゲームスクリプトとして交換・挿入できるようにする
 * スクリプトファイルはscriptdata_assets_all.bundleに格納されている
 *
 * CommandReverseCompiler.py
 *      スクリプトの逆コンパイルを行う
 *      動作確認やゲーム内スクリプトを読んで参考にするのに使う
 * CommandCompiler.py
 *      スクリプトのコンパイルを行う
 *      コンパイルを行わないとゲーム内で使用できるようにはならない
 * commandlist.py
 *      コンパイル/逆コンパイルのためのコマンド定義
 *      イベントフラグ一覧もあるので必要なら参照のこと
 * compare.py
 *      コンパイラ/逆コンパイラのテストコマンド
 *      元のスクリプトとこれを逆コンパイル->コンパイルしたものが同一かどうか比較する
 *      ScriptDataContainer.bytesを食わせて全部通ればOK
 */
class ScriptInjector
{
    static ScriptDataContainer ptr = null;
    static ScriptDataContainer original_code = null;
    static ScriptDataContainer replaces_all = null;
    static Dictionary<string, List<ReplaceLines>> replaces_partial = null;
    static Dictionary<string, List<InsertCommand>> inserts = null;
    public static Dictionary<string, DisplayString> textids = null;
    public static Dictionary<int, bool> exflags = null;
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1901;
    public static readonly string TextIDResouceID = "ScriptInjector.textids";
    public static readonly string ExFlagResouceID = "ScriptInjector.exflags";

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ScriptInjector", false,
                "スクリプトを外部から挿入できるようにする\n"+
                "詳細はReadme.txt参照のこと"
            );
        ConfigEntry<bool> show_script_source = cfg.Bind(
                "Const", "ShowScriptSource", false,
                "スクリプトをコンソールに出力する"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ScriptInjector]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][ScriptInjector]enable");
            LoYUtilPlugin.ev_load += load_scripts;
            LoYUtilPlugin.ev_load += load_textids;
            LoYUtilPlugin.ev_load += load_exflags;
            LoYUtilPlugin.ev_reload += reload;
            LoYUtilPlugin.ev_reload += load_textids;
            LoYUtilPlugin.ev_reload += load_exflags;

            LoYUtilPlugin.mgr.add_flag(FlagId, true);

            var org = Util.get_method(typeof(ScriptEngine), "DeserializeAsync");
            var hook = typeof(ScriptInjector).GetMethod("DeserializeAndImplementAsync");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(SessionFlagAccessorScripts), "IsOnScriptFlag");
            hook = typeof(ScriptInjector).GetMethod("IsOnExScriptFlag");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(SessionFlagAccessorScripts), "SetScriptFlag");
            hook = typeof(ScriptInjector).GetMethod("SetExScriptFlag");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(ScriptCommand), "GetParameterDisplayString");
            hook = typeof(ScriptInjector).GetMethod("ExternalDisplayString");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            //if(show_script_source.Value || true)
            if(show_script_source.Value)
            {
                org = Util.get_method(typeof(ScriptEngine), "CallScript");
                hook = typeof(ScriptInjector).GetMethod("print_scrname");
                hm.Patch(org, prefix: new HarmonyMethod(hook));

                var ass = Assembly.GetAssembly(typeof(ScriptEngine)).GetType("Experience.ScriptEvent.ScriptEngine+Executor");
                org = ass.GetMethod("Request", Util.BINDING_ALL);
                hook = typeof(ScriptInjector).GetMethod("print_script");
                hm.Patch(org, prefix: new HarmonyMethod(hook));
            }
        }
    }

    /* ScriptCommand.GetParameterDisplayStringで取得できるテキストを追加
     * 同じTextIDの場合、こちらが優先されることに注意
     */
    public static bool ExternalDisplayString(ScriptCommand __instance, ref DisplayString __result, int parameterIndex)
    {
        string parameter = __instance.GetParameter<string>(parameterIndex);
        __result = LoYUtilPlugin.mgr.TextId(parameter);
        return __result == null ? true : false;
    }

    /* LoYUtilResource\exflags.eflのフラグリストを読み込む
     * フォーマットは超単純でFlagName1:FlagID1,FlagName2:FlagID2,...
     */
    public static void load_exflags()
    {
        if(exflags == null)
        {
            exflags = new Dictionary<int, bool>();
            LoYUtilPlugin.mgr.add_data(ExFlagResouceID, exflags);
        }
        else
            exflags.Clear();
        string path = Path.Combine(LoYUtilPlugin.rsrc_path, "exflags.efl");
        foreach(var p in File.ReadAllText(path).Split(','))
        {
            //異常に短すぎるものは無視
            if(p.Length <= 2)
                continue;
            string[] buf = p.Trim().Split(':');
            //実際、フラグ名(buf[0])は要らない
            if(buf.Length == 2)
            {
                int i = int.Parse(buf[1]);
                if(exflags.ContainsKey(i))
                    Console.Write("[ScriptInjector::load_exflags()]ID:\"{0}\"/{1} is already exist.", buf[0], buf[1]);
                else
                    exflags[i] = false;
            }
            else
                Console.Write("[ScriptInjector::load_exflags()]invalid text:\"{0}\"", p);
        }
    }

    /* LoYUtilResourceフォルダから*.tidテキストを読み込む
     * フォーマットはTextID1:SOME_TEXT,\nTextID2:SOME_TEXT,\n...
     */
    public static void load_textids()
    {
        if(textids == null)
        {
            textids = new Dictionary<string, DisplayString>();
            LoYUtilPlugin.mgr.add_data(TextIDResouceID, textids);
        }
        else
            textids.Clear();
        char[] trim = {'\r', '\n'};
        foreach(var f in Directory.GetFiles(LoYUtilPlugin.rsrc_path, "*.tid", SearchOption.AllDirectories))
        {
            foreach(var ln in File.ReadAllText(f).Split(','))
            {
                //行が\r\nのみの時など短かすぎる行(空行等)は無視
                if(ln.Length <= 2)
                    continue;
                string[] buf = ln.Trim(trim).Split(':');
                if(buf.Length == 2)
                    if(textids.ContainsKey(buf[0]))
                        Console.Write("[ScriptInjector::load_textids]ID:\"{0}\" is already exist.", buf[0]);
                    else
                        textids[buf[0]] = DisplayString.Generate(buf[1]);
                else
                    Console.Write("[ScriptInjector::load_textids]invalid text:\"{0}\"", ln);
            }
        }
        //foreach(var p in textids)
            //Console.Write("{0}: {1}", p.Key, p.Value);
    }

    /* LoYUtilResourceフォルダから*.escスクリプトを読み込む */
    public static void load_scripts()
    {
        if(replaces_all == null)
        {
            replaces_all = new ScriptDataContainer();
            replaces_partial = new Dictionary<string, List<ReplaceLines>>();
            inserts = new Dictionary<string, List<InsertCommand>>();
        }
        else
        {
            replaces_all = new ScriptDataContainer();
            replaces_partial.Clear();
            inserts.Clear();
        }
        foreach(var f in Directory.GetFiles(LoYUtilPlugin.rsrc_path, "*.esc", SearchOption.AllDirectories))
        {
            string[] buf = File.ReadAllText(f).Split(new Char[]{'\n'}, 2);
            string inj_type = buf[0].Trim();
            string json = buf[1];
            ScriptDataContainer.DataPair dp = JsonUtility.FromJson<ScriptDataContainer.DataPair>(json);
            if(dp.Value.Length == 0)
            {
                Console.Write($"[ScriptInjector::load_scripts]{f} is empty script??");
                continue;
            }
            //シンプルにスクリプトを置き換え
            if(inj_type == "replace-all")
            {
                //Console.Write("replace all: {0}", dp.Key);
                if(replaces_all.Contains(dp.Key))
                    Console.Write($"[ScriptInjector::load_scripts]{dp.Key} is already exist in replace_all.");
                else
                    replaces_all.Add(dp.Key, dp.Value);
            }
            //指定行のコマンドを置換
            else if(inj_type.StartsWith("replace:"))
            {
                string[] t = inj_type.Trim().Split(":");
                t = t[1].Split("-");
                int from = int.Parse(t[0]);
                int to = int.Parse(t[1]);
                //Console.Write("replace partial: {0}@{1}to{2}", dp.Key, from, to);
                if(from > to)
                {
                    Console.Write($"[ScriptInjector::load_scripts]Error: invalid replace linenumber order : from({from}) > to({to})");
                    continue;
                }
                else if(!replaces_partial.ContainsKey(dp.Key))
                    replaces_partial[dp.Key] = new List<ReplaceLines>{new ReplaceLines(){from=from, to=to, sc=dp.Value}};
                else
                    replaces_partial[dp.Key].Add(new ReplaceLines(){from=from, to=to, sc=dp.Value});
            }
            //指定行の前にコマンドを挿入
            else if(inj_type.StartsWith("insert:"))
            {
                int lineno = int.Parse(inj_type.Split(":")[1]);
                //Console.Write("insert: {0}@{1}", dp.Key, lineno);
                if(!inserts.ContainsKey(dp.Key))
                    inserts[dp.Key] = new List<InsertCommand>{new InsertCommand(){lineno=lineno, sc=dp.Value}};
                else
                    inserts[dp.Key].Add(new InsertCommand(){lineno=lineno, sc=dp.Value});
            }
            else
            {
                Console.Write($"[ScriptInjector::load_scripts]unrecognize injection type : {inj_type}");
                //Console.Write("[ScriptInjector::load_scripts]unrecognized injection type : {0}", BitConverter.ToString(Encoding.ASCII.GetBytes(inj_type)));
            }
        }
        //insertとreplace内のリストは逆順にソートしておかないと挿入の際にバグる
        foreach(var l in inserts.Values)
            if(l.Count > 1)
                l.Sort((a, b) => b.lineno - a.lineno);
        foreach(var l in replaces_partial.Values)
            if(l.Count > 1)
                l.Sort((a, b) => b.from - a.from);
    }

    /* F5キーでスクリプトのリロードを行う */
    public static void reload()
    {
        //script not loaded yet.
        if(ptr == null)
            return;
        Console.Write("[ScriptInjector] reloading...");
        writeback_original();
        load_scripts();
        injection(ptr);
    }

    /* オリジナルのスクリプトをスクリプトのコンテナに書き戻してやる
     * シャローコピーすると二回目以降のリロードがうまく動かなくなるのでオブジェクトの作り直しから
     */
    public static void writeback_original()
    {
        //ScriptDataContainer.DataContainer org = (ScriptDataContainer.DataContainer)Util.get_field(typeof(ScriptDataContainer), "container").GetValue(original_code);
        //ptr.Merge(org);
        ScriptDataContainer.DataContainer org = new ScriptDataContainer.DataContainer();
        foreach(var n in original_code.Names)
        {
            ScriptSource s = new ScriptSource();
            List<ScriptCommand> cmds = new List<ScriptCommand>();
            foreach(var cmd in original_code[n])
                cmds.Add(cmd);
            s.SetCommands(cmds);
            org[n] = s;
        }
        //新規追加されたスクリプトは中身を空にしておく…必要はなかった
        //foreach(var n in replaces_all.Names)
            //if(!original_code.Contains(n))
                //org[n] = new ScriptSource();
        ptr.Merge(org);
    }

    /* 元のコードをスクリプトのリロードのために保管しておく
     * シャローコピーすると二回目以降のリロードがうまく動かなくなるのでオブジェクトの作り直しから
     */
    public static void copy_original(ScriptDataContainer scriptDataContainer)
    {
        original_code = new ScriptDataContainer();
        ScriptDataContainer.DataContainer org = new ScriptDataContainer.DataContainer();
        //新規追加されたスクリプト以外を保存する
        //replace-allの場合はDataContainerを作り直すのでシャローコピー
        foreach(var n in replaces_all.Names)
            if(scriptDataContainer.Contains(n))
                org[n] = scriptDataContainer[n];
        foreach(var n in replaces_partial.Keys)
        {
            ScriptSource s = new ScriptSource();
            List<ScriptCommand> cmds = new List<ScriptCommand>();
            foreach(var cmd in scriptDataContainer[n])
                cmds.Add(cmd);
            s.SetCommands(cmds);
            org[n] = s;
        }
        foreach(var n in inserts.Keys)
        {
            ScriptSource s = new ScriptSource();
            List<ScriptCommand> cmds = new List<ScriptCommand>();
            foreach(var cmd in scriptDataContainer[n])
                cmds.Add(cmd);
            s.SetCommands(cmds);
            org[n] = s;
        }
        original_code.Merge(org);
    }

    /* コマンドの注入 */
    public static void injection(ScriptDataContainer scriptDataContainer)
    {
        //リロードに備えてオリジナルのスクリプトをコピーしておく
        if(original_code == null)
            copy_original(scriptDataContainer);
        //スクリプトの置き換え、あるいは新規に注入
        foreach(var n in replaces_all.Names)
        {
            Console.Write("[ScriptInjector::injection()]replace-all: {0}", n);
            ScriptDataContainer.DataContainer dc = new ScriptDataContainer.DataContainer();
            dc[n] = replaces_all[n];
            scriptDataContainer.Merge(dc);
        }
        //指定行のコマンドを置換
        foreach(var d in replaces_partial)
        {
            ScriptDataContainer.DataContainer dc = new ScriptDataContainer.DataContainer();
            ScriptSource sc = new ScriptSource();
            foreach(var v in d.Value)
            {
                List<ScriptCommand> cmds = new List<ScriptCommand>();
                int inj_from = v.from;
                int inj_to = v.to;
                ScriptSource inj_cmd = v.sc;
                Console.Write("[ScriptInjector::injection()]replace partial: {0}@{1}to{2}", d.Key, inj_from, inj_to);
                int cmd_ln;
                foreach(var cmd in scriptDataContainer[d.Key])
                {
                    cmd_ln = cmd.LineNumber;
                    //行番号が指定範囲内ならコマンドを挿入
                    if(cmd_ln >= inj_from && inj_cmd != null)
                    {
                        foreach(var inj in inj_cmd)
                            cmds.Add(inj);
                        inj_cmd = null;
                    }
                    //行番号が指定範囲内ならスキップ
                    if(!(inj_from <= cmd_ln && cmd_ln <= inj_to))
                        cmds.Add(cmd);
                }
                //指定範囲がスクリプト内に存在しない場合は末尾に足す
                if(inj_cmd != null)
                    foreach(var inj in inj_cmd)
                        cmds.Add(inj);
                sc.SetCommands(cmds);
                dc[d.Key] = sc;
                scriptDataContainer.Merge(dc);
            }
        }
        //指定行にコマンドを挿入
        foreach(var d in inserts)
        {
            ScriptDataContainer.DataContainer dc = new ScriptDataContainer.DataContainer();
            ScriptSource sc = new ScriptSource();
            foreach(var v in d.Value)
            {
                List<ScriptCommand> cmds = new List<ScriptCommand>();
                int inj_line = v.lineno;
                ScriptSource inj_cmd = v.sc;
                Console.Write("[ScriptInjector::injection()]insert: {0}@{1}", d.Key, inj_line);
                int cmd_ln;
                foreach(var cmd in scriptDataContainer[d.Key])
                {
                    cmd_ln = cmd.LineNumber;
                    //指定行直前にコマンドを挿入
                    if(cmd_ln >= inj_line && inj_cmd != null)
                    {
                        foreach(var inj in inj_cmd)
                            cmds.Add(inj);
                        inj_cmd = null;
                    }
                    cmds.Add(cmd);
                }
                //指定行がスクリプト内に存在しない場合は末尾に足す
                if(inj_cmd != null)
                    foreach(var inj in inj_cmd)
                        cmds.Add(inj);
                sc.SetCommands(cmds);
                dc[d.Key] = sc;
                scriptDataContainer.Merge(dc);
            }
        }
    }

    /* スクリプトのロードをフックしてコマンドを注入する */
    public static async void __internal__DeserializeAndImplementAsync(ScriptEngine __instance, byte[] bytes, LoadingTask loadingTask)
    {
        Console.Write("[ScriptInjector::__internal__DeserializeAndImplementAsync]Deserialize and inject scripts.");
        ScriptDataContainer scriptDataContainer = await Task.Run<ScriptDataContainer>(() => JsonLoader.LoadFromMemory<ScriptDataContainer>(bytes));
        injection(scriptDataContainer);
        __instance.SetScriptDataContainer(scriptDataContainer);
        Console.Write("[ScriptInjector::__internal__DeserializeAndImplementAsync]Deserialize done.");
        ptr = scriptDataContainer;
        loadingTask.IsLoading = false;
    }

    /* DeserializeAsyncのスクリプト読み込み処理をまるまる乗っ取る
     * Asyncな処理なので変則的な書き方になった
     */
    public static bool DeserializeAndImplementAsync(ScriptEngine __instance, byte[] bytes, LoadingTask loadingTask)
    {
        __internal__DeserializeAndImplementAsync(__instance, bytes, loadingTask);
        return false;
    }

    /* スクリプトからフラグを読み込む処理に拡張フラグの値を返す
     * 一度読んだフラグは以後セーブデータに入るので、ここで値の調整は不要
     */
    public static bool IsOnExScriptFlag(ScriptFlagId id, ref bool __result)
    {
        //Console.Write("[IsOnExScriptFlag]{0}:{1}", id, __result);
        if(Database.Session.Flags.ScriptFlag.ContainsKey(id))
            return true;
        if(LoYUtilPlugin.mgr.is_enable && LoYUtilPlugin.mgr.contains_flag(id))
            __result = LoYUtilPlugin.mgr.get_flag(id);
        else if(exflags.ContainsKey((int)id))
            __result = exflags[(int)id];
        //Console.Write("[IsOnExScriptFlag]\t->{0}", __result);
        return false;
    }

    /* 拡張フラグの状態書きに行くときにこちらのクラスの辞書にも反映させておく
     * 実際、ゲームのフラグストレージはデフォルトで存在しないフラグだろうが問題なく受け付けるので、
     * 事実上不要であるような気がする
     */
    public static void SetExScriptFlag(ScriptFlagId id, bool isOn)
    {
        //Console.Write("[SetExScriptFlag]{0}/{1}", id, isOn);
        if(exflags.ContainsKey((int)id))
            exflags[(int)id] = isOn;
    }

    /* 読み込みスクリプト名を表示 */
    public static void print_scrname(string scriptName)
    {
        Console.Write(scriptName);
    }

    /* 読み込みスクリプトのコマンドを表示 */
    public static void print_script(object context)
    {
        //internal classのリフレクションは少しめんどい
        var ass = Assembly.GetAssembly(typeof(ScriptEngine)).GetType("Experience.ScriptEvent.ScriptContext");
        //Util.print_all(ass);
        //UnityEngine.Debug.Log(ass);
        var m = Util.get_method(ass, "get_Source");
        //UnityEngine.Debug.Log(m);
        ScriptSource s = (ScriptSource)m.Invoke(context, new object[]{});
        foreach(ScriptCommand c in s)
        {
            ScriptCommandParameterData[] p = (ScriptCommandParameterData[])c.Parameters;
            ScriptCommandId cmd = c.CommandId;
            string l = "";
            for(int i = 0; i < p.Length; ++i)
                l += p[i].Parameter + ", ";
            //末尾の", "を切り詰める
            if(l.Length >= 2)
                l = l.Substring(0, l.Length - 2);
            Console.Write("[{0}]{1}:{2}", c.LineNumber, cmd, l);
        }
    }


    public class ReplaceLines
    {
        public int from, to;
        public ScriptSource sc;
    }

    public class InsertCommand
    {
        public int lineno;
        public ScriptSource sc;
    }
}

}
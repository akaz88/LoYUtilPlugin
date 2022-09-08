using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.ScriptEvent;
using Experience.UIs;


namespace LoYUtil
{

/* MOD情報等の橋渡し */
class ResourceManager
{
    public static HarmonyMethod extext = new HarmonyMethod(Util.get_method(typeof(ResourceManager), "ExText"));

    public static Manager enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ResourceManager", false,
                "MODで使用するフラグ等の管理"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ResourceManager]disable");
        else
            Console.Write("[LoYUtilPlugin][ResourceManager]enable");
        return new Manager(cfg, enabled.Value);
    }

    /* ScriptInjectorのロードした追加テキストを返す */
    public static void ExText(ref DisplayString __result)
    {
        DisplayString s = LoYUtilPlugin.mgr.TextId(__result.Id);
        if(s != null)
            __result = s;
    }
}


public class Manager
{
    private Dictionary<int, bool> mod_flags = new Dictionary<int, bool>();
    private Dictionary<string, object> mod_datas = new Dictionary<string, object>();
    public bool is_enable = false;
    public static readonly int FLAG_DEFINED = 1059;

    public Manager(ConfigFile cfg, bool enabled)
    {
        is_enable = enabled;
        if(!enabled)
            return;
    }

    public Dictionary<int, bool> get_flag_dict()
    {
        if(!this.is_enable)
            return null;
        return this.mod_flags;
    }

    public void add_flag(int flag, bool state=false)
    {
        if(!this.is_enable)
            return;
        //ゲーム本編のフラグは1059まで定義されているので、それ以降の値を使うよう注意
        if(flag <= FLAG_DEFINED)
            Console.Write($"[ResourceManager::add_flag]flag({flag}) is already used in game.");
        if(this.mod_flags.ContainsKey(flag))
            Console.Write($"[ResourceManager::add_flag]flag({flag}) is already registered.");
        else
            this.mod_flags[flag] = state;
    }

    public void add_flag(ScriptFlagId id, bool state)
    {
        if(!this.is_enable)
            return;
        this.add_flag((int)id, state);
    }

    /* お約束：追加後のデータは必ずClear()して初期化するか、change_dataで反映させること
     * きちんと手順をふまないとぬるぽになったり変な挙動をする
     * 使用例：mgr.add_data("some_id", some_data)
     */
    public void add_data(string id, object data)
    {
        if(!this.is_enable)
            return;
        if(!this.mod_datas.ContainsKey(id))
            this.mod_datas[id] = data;
    }

    public bool get_flag(ScriptFlagId id)
    {
        return this.get_flag((int)id);
    }

    public bool get_flag(int id)
    {
        Console.Write($"get_flag: is_enable:{this.is_enable}, id:{id}, Contains:{this.mod_flags.ContainsKey(id)}, Value:{this.mod_flags.GetValueOrDefault(id, false)}");
        if(!this.is_enable || !this.mod_flags.ContainsKey(id))
            return false;
        return this.mod_flags[id];
    }

    public void set_flag(ScriptFlagId id, bool state)
    {
        this.set_flag((int)id, state);
    }

    public void set_flag(int id, bool state)
    {
        if(!this.is_enable)
            return;
        if(this.mod_flags.ContainsKey(id))
            this.mod_flags[id] = state;
    }

    public bool contains_flag(int id)
    {
        if(!this.is_enable)
            return false;
        return this.mod_flags.ContainsKey(id);
    }

    public bool contains_flag(ScriptFlagId id)
    {
        return this.contains_flag((int)id);
    }

    public DisplayString TextId(string id)
    {
        //Console.Write("[TextId]{0}", id);
        if(!this.is_enable || id == null || id == "")
            return null;
        if(!this.mod_datas.ContainsKey("ScriptInjector.textids"))
            return null;
        Dictionary<string, DisplayString> d = (Dictionary<string, DisplayString>)this.mod_datas["ScriptInjector.textids"];
        if(!d.ContainsKey(id))
            return null;
        if(d[id].Text.Contains("{"))
        {
            string s = d[id].Text;
            //"{}"で囲われた文字列の置き換えを行う
            while(s.Contains("{"))
            {
                int start = s.IndexOf("{");
                int len = s.IndexOf("}", start) - start + 1;
                string key = s.Substring(start, len);
                string repl = "[None]";
                //主人公のプレイヤーIDは常に1
                //主人公の名前から役職を省いたものを返す
                //<player.name>との違いは後ろに役職がつかないこと
                if(key == "{HERO_NAME}")
                    repl = Database.Session.Players.FindPlayerByPlayerId(1).NickName.TrimEnd(new char[]{'課', '部', '長'});
                //ゲーム本来の機能で<player.fullname>を使えばいいんで廃止
                //else if(key == "{HERO_FULLNAME}")
                    //repl = Database.Session.Players.FindPlayerByPlayerId(1).FullName;
                //主人公の役職
                else if(key == "{HERO_POST}")
                    if(SessionFlagAccessorScripts.IsOnScriptFlag(ScriptFlagId.S49_00_03))
                        repl = "部長";
                    else
                        repl = "課長";
                //TextIDを再帰的に使えるようにする
                //循環参照にならないように注意
                else if(key.StartsWith("{TID@"))
                    repl = this.TextId(key.Substring(5, key.Length - "{TID@}".Length)).Text;
                s = s.Replace(key, repl);
            }
            return DisplayString.Generate(s);
        }
        return d[id];
    }

    public void add_excommand(string key, ExternalCommand.ExCommand cmd)
    {
        if(!this.is_enable)
            return;
        Dictionary<string, ExternalCommand.ExCommand> excommand = (Dictionary<string, ExternalCommand.ExCommand>)this.mod_datas["ExternalCommand.excommand"];
        if(excommand == null)
        {
            Console.Write("[add_excommand]Error: excommand dictionary is not registered.");
            return;
        }
        else if(excommand.ContainsKey(key))
        {
            Console.Write("[add_excommand]Error: {0} is already registered to excommand.", key);
            return;
        }
        excommand[key] = cmd;
    }
}

}
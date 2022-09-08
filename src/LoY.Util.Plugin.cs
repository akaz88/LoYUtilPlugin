using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Collections;
using System.Collections.Generic;
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.SaveLoad;

namespace LoYUtil
{

[BepInPlugin("LoY.Util.Plugin", "LoY Utility Plug-In", "0.0.0.1")]
public class LoYUtilPlugin : BaseUnityPlugin
{
    static string id = "LoY.Util.Plugin";
    static ConfigFile cfg;
    public static string rsrc_path;
    public static Manager mgr = null;
    public static event Action ev_load;
    public static event Action ev_load_later;
    public static event Action ev_reload;
    public static event Func<IEnumerator> ev_update;
        //deligate cheat sheat
        //https://atmarkit.itmedia.co.jp/fdotnet/dotnettips/730dlgttype/dlgttype.html

    public void Awake()
    {
        Harmony hm = new Harmony(id);
        cfg = Config;
        rsrc_path = Path.Combine(Paths.BepInExRootPath, "LoYUtilResource");
        Console.Write("[LoYUtilPlugin]patching...");

        mgr = ResourceManager.enable(hm, cfg);
        BootScreenFix.enable(hm, cfg);
        TitleTextIndicator.enable(hm, cfg);
        EagleEyeCheat.enable(hm, cfg);
        //YAMinimapBorder.enable(hm, cfg);
            //どうにかする予定は特にない
        AndStayBack.enable(hm, cfg);
        LRSelect.enable(hm, cfg);
        MultiItemSelect.enable(hm, cfg);
        ChooseDifficulty.enable(hm, cfg);
        ScriptInjector.enable(hm, cfg);
        ExpDebugPrint.enable(hm, cfg);
        EnemyInjector.enable(hm, cfg);
        FastRepeat.enable(hm, cfg);
        ItemInjector.enable(hm, cfg);
        DungeonInjector.enable(hm, cfg);
        ImageInjector.enable(hm, cfg);
        ExternalCommand.enable(hm, cfg);
        SoftReset.enable(hm, cfg);
        Bugfix.enable(hm, cfg);

        //ev_load();
        //GameInitializer.Phase.SystemInitializationに移動

        //ゲームの起動後でないとロードされていないデータを読むのに使う
        var org = Util.get_method(typeof(GameInitializer), "SetReady");
        var hook = typeof(LoYUtilPlugin).GetMethod("load_later");
        hm.Patch(org, prefix: new HarmonyMethod(hook));
    }

    public void Update()
    {
        //F5キーでスクリプト等のリロード
        if(Input.GetKeyDown(KeyCode.F5))
            ev_reload();
        StartCoroutine(ev_update());
        //ソフトリセット：Selectを押しながらStartでセーブデータをロードする
        //if(SingletonMonoBehaviour<Gamepad>.Instance != null && Gamepad.GetKeyState(GamepadKey.Select).Holding && Gamepad.GetKeyState(GamepadKey.Start).Pressed)
            //StartCoroutine(SoftReset());
    }

    IEnumerator __SoftReset()
    {
        Console.Write("SoftReset");
        var inst = SingletonMonoBehaviour<SaveLoadController>.Instance;
        int slot = (int)Util.get_value(inst, "loadingSlotNumber");
        if(slot == SaveLoadController.SaveSlotNumberInvalid)
            yield break;
        bool is_loading = true;
        inst.LoadSessionData(
            slot,
            0,
            new SaveLoadController.LoadSessionDataFinishCallback(
                (result, no, nav, fid) =>{
                    Console.Write($"{result}, {no}, {nav}, {fid}");
                    if(result == StorageResultCode.SUCCESS)
                        is_loading = false;
                }
            )
        );
        while(is_loading)
            yield return null;
        Console.Write("done.");
    }

    public static void load_later(GameInitializer.Phase phase)
    {
        if(phase == GameInitializer.Phase.SystemInitialization)
            ev_load();
        else if(phase == GameInitializer.Phase.AssetLoading)
            ev_load_later();
    }
}


public class Util
{
    private static readonly BindingFlags BINDING_BASE = BindingFlags.InvokeMethod | BindingFlags.Instance | BindingFlags.Static;
    public static readonly BindingFlags BINDING_PUBLIC = BINDING_BASE | BindingFlags.Public;
    public static readonly BindingFlags BINDING_NONPUBLIC = BINDING_BASE | BindingFlags.NonPublic;
    public static readonly BindingFlags BINDING_ALL = BINDING_PUBLIC | BINDING_NONPUBLIC;

    /* デバッグ用に呼び出し元をprintする */
    public static void print_stack(int max = 0)
    {
        int i = 0;
        List<string> l = new List<string>();
        try
        {
            while(true)
            {
                //StackFrame[0]がUtil.print_stack()なので、それ以前を参照しなければならない
                StackFrame fr = new StackFrame(++i);
                l.Add(string.Format("{0}::{1}()", fr.GetMethod().ReflectedType.FullName, fr.GetMethod().Name));
                if(i == max)
                    break;
            }
        }
        catch
        {;}
        Console.WriteLine(string.Join("\n\t-> ", l));
    }

    /* 主によくわからんメソッドのフック用に適当に引数と返り値を全部ダンプする
     * staticクラスに使ったら落ちたりもした
     */
    public static void print_result(object __instance, object[] __args, object __result)
    {
        Console.Write("[Util.print_result]");
        if(__instance != null)
        {
            Console.Write(__instance.GetType());
            Console.Write(__instance);
        }
        if(__args != null)
        {
            foreach(var o in __args)
            {
                Console.Write(o.GetType());
                Console.Write(o);
            }
        }
        if(__result != null)
        {
            Console.Write(__result.GetType());
            Console.Write(__result);
        }
    }

    public static void set_static_value(Type cls, string fname, object value)
    {
        get_field(cls, fname).SetValue(null, value);
    }

    public static void set_static_value(object inst, string fname, object value)
    {
        set_static_value(inst.GetType(), fname, value);
    }

    public static void set_value(object inst, string fname, object value)
    {
        //Console.Write("[set_value]{0}, {1}, {2}, {3}", inst.GetType(), fname, value, get_field(inst.GetType(), fname));
        get_field(inst.GetType(), fname).SetValue(inst, value);
    }

    public static object get_value(object inst, string fname)
    {
        //Console.Write("[get_value]{0}, {1}, {2}", inst.GetType(), fname, get_field(inst.GetType(), fname));
        return get_field(inst.GetType(), fname).GetValue(inst);
    }

    public static FieldInfo get_field(Type cls, string fname)
    {
        //Console.Write("{0}, {1}, {2}", cls, fname, cls.GetField(fname, BINDING_ALL));
        return cls.GetField(fname, BINDING_ALL);
    }

    public static FieldInfo get_field(object cls, string fname)
    {
        return cls.GetType().GetField(fname, BINDING_ALL);
    }

    public static bool has_property(object cls, string pname)
    {
        return cls.GetType().GetProperty(pname, BINDING_ALL) != null ? true : false;
    }

    public static MethodInfo get_method(Type cls, string fname)
    {
        return cls.GetMethod(fname, BINDING_ALL);
    }

    public static MethodInfo get_method(object cls, string fname)
    {
        return get_method(cls.GetType(), fname);
    }

    public static MethodInfo get_method(Type cls, Type[] tps, string fname)
    {
        return cls.GetMethod(fname, BINDING_ALL, null, tps, null);
    }

    public static MethodInfo get_method(object cls, Type[] tps, string fname)
    {
        return get_method(cls.GetType(), tps, fname);
    }

    //staticメソッド用
    public static object invoke(Type tp, string fname, object[] args)
    {
        return get_method(tp, fname).Invoke(null, args);
    }

    public static object invoke(object cls, string fname, object[] args)
    {
        return get_method(cls, fname).Invoke(cls, args);
    }

    public static object invoke(object cls, string fname)
    {
        return invoke(cls, fname, new object[]{});
    }

    //ポリモーフィズム対策
    public static object invoke(object cls, Type[] tps, string fname, object[] args)
    {
        return get_method(cls, tps, fname).Invoke(cls, args);
    }

    //基底クラスのメソッドを呼び出すときに使う
    public static object invoke(Type tp, object cls, string fname, object[] args)
    {
        return get_method(tp, fname).Invoke(cls, args);
    }

    public static void print_methods(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetMethods(BINDING_PUBLIC))
            l.Add(string.Format("Public   : {0}", m.ToString()));
        foreach(var m in cls.GetMethods(BINDING_NONPUBLIC))
            l.Add(string.Format("NonPublic: {0}", m.ToString()));
        l.Sort();
        l.Insert(0, "Methods:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    public static void print_fields(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetFields(BINDING_PUBLIC))
            l.Add(string.Format("Public   : {0}", m.ToString()));
        foreach(var m in cls.GetFields(BINDING_NONPUBLIC))
            l.Add(string.Format("NonPublic: {0}", m.ToString()));
        l.Sort();
        l.Insert(0, "Fields:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    public static void print_members(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetMembers(BINDING_PUBLIC))
            l.Add(string.Format("Public    : {0}", m.ToString()));
        foreach(var m in cls.GetMembers(BINDING_NONPUBLIC))
            l.Add(string.Format("NonPublic : {0}", m.ToString()));
        l.Sort();
        l.Insert(0, "Members:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    public static void print_properties(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetProperties(BINDING_PUBLIC))
            l.Add(string.Format("Public   : {0}", m.ToString()));
        foreach(var m in cls.GetProperties(BINDING_NONPUBLIC))
            l.Add(string.Format("NonPublic: {0}", m.ToString()));
        l.Sort();
        l.Insert(0, "properties:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    public static void print_nested(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetNestedTypes(BINDING_PUBLIC))
            l.Add(string.Format("Public   : {0}", m.ToString()));
        foreach(var m in cls.GetNestedTypes(BINDING_NONPUBLIC))
            l.Add(string.Format("NonPublic: {0}", m.ToString()));
        l.Sort();
        l.Insert(0, "NestedTypes:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    public static void print_interfaces(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetInterfaces())
            l.Add(m.ToString());
        l.Sort();
        l.Insert(0, "InterFaces:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    public static void print_all(Type cls)
    {
        Console.WriteLine("All:{0}", cls);
        print_members(cls);
        print_methods(cls);
        print_fields(cls);
        print_properties(cls);
        print_nested(cls);
        print_interfaces(cls);
    }
}


public class TableBuilder
{
    /* MODリソースフォルダからpath文字列に合致するJSONファイルを読み込んでインスタンス化、
     * そのリストを返す
     */
    public static void build_list_by_json<T>(ref List<T> l, string path)
    {
        if(l == null)
            l = new List<T>();
        else
            l.Clear();
        //Console.Write("[build_dict_by_json]{0}", path);
        foreach(var f in Directory.GetFiles(LoYUtilPlugin.rsrc_path, path, SearchOption.AllDirectories))
        {
            //Console.Write("[build_dict_by_json]{0}", f);
            string buf = File.ReadAllText(f);
            T data = JsonUtility.FromJson<T>(buf);
            l.Add(data);
        }
    }

    /* 同ScriptObject版 */
    public static void build_solist_by_json<T>(ref List<T> l, string path) where T: ScriptableObject
    {
        if(l == null)
            l = new List<T>();
        else
            l.Clear();
        //Console.Write("[build_dict_by_json]{0}", path);
        foreach(var f in Directory.GetFiles(LoYUtilPlugin.rsrc_path, path, SearchOption.AllDirectories))
        {
            //Console.Write("[build_dict_by_json]{0}", f);
            string buf = File.ReadAllText(f);
            T data = (T)ScriptableObject.CreateInstance(typeof(T));
            JsonUtility.FromJsonOverwrite(buf, data);
            //T data = (T)JsonUtility.FromJson(buf, typeof(T));
            l.Add(data);
        }
    }

    /* build_list_by_json()で作ったリストとゲームのデータテーブルから新たなデータテーブルを作成する
     * データテーブルはゲームのロード完了後でないとロードされていないことに注意
     */
    public static void build_table<TTable, T>(ref TTable db, List<T> l) where TTable: DataTable<T> where T: IDataRecord, IIdentifiable<int>, new()
    {
        //ScriptableObjectを作るためのお作法
        db =  (TTable)ScriptableObject.CreateInstance(typeof(TTable));
        TTable tbl = Database.Table.Get<TTable>();
        T[] records = (T[])tbl.GetType().BaseType.GetField("records", Util.BINDING_ALL).GetValue(tbl);

        int n = records.Length;
        foreach(var v in l)
            n = v.GetId() >= n ? v.GetId() + 1 : n;

        T[] array = new T[n + 0];
        records.CopyTo(array, 0);
        //Console.Write("[__generic_table]{0}({1}): {2}({3}/{4})", db.GetType(), tbl.GetType(), n, array.Length, records.Length);

        //指定IDまで空きがあるとDataTable<T>::EnumerateValidDataが落ちるので適当なデータで埋めておく
        if(n > records.Length)
            for(int i = records.Length; i < n; ++i)
                array[i] = records[0];

        foreach(var v in l)
        {
            //Console.Write("[__generic_table]{0}", v.GetId());
            array[v.GetId()] = v;
        }
        tbl.GetType().BaseType.GetField("records", Util.BINDING_ALL).SetValue(db, array);
    }
}


}
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Collections;
using System.Collections.Generic;


namespace LoYUtil
{

/* デバッグ用のあれこれを出力したりクラスのメンバーをあれこれしたりする便利なやつ */
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

    /* クラスんのstaticメンバーを書き換える */
    public static void set_static_value(Type cls, string fname, object value)
    {
        get_field(cls, fname).SetValue(null, value);
    }

    public static void set_static_value(object inst, string fname, object value)
    {
        set_static_value(inst.GetType(), fname, value);
    }

    /* クラスのメンバーを書き換える */
    public static void set_value(object inst, string fname, object value)
    {
        //Console.Write("[set_value]{0}, {1}, {2}, {3}", inst.GetType(), fname, value, get_field(inst.GetType(), fname));
        get_field(inst.GetType(), fname).SetValue(inst, value);
    }

    /* クラスのメンバーを返す
     * objectで返すのでキャストは呼び出し側でやる
     */
    public static object get_value(object inst, string fname)
    {
        //Console.Write($"[Util][get_value]{inst.GetType()}, {fname}, {get_field(inst.GetType(), fname)}");
        return get_field(inst.GetType(), fname).GetValue(inst);
    }

    /* 基底クラスのメンバーを返す
     * objectで返すのでキャストは呼び出し側でやる
     */
    public static object get_baseclass_value(object inst, string fname)
    {
        return get_baseclass_field(inst, fname).GetValue(inst);
    }

    /* クラスのフィールドを返す */
    public static FieldInfo get_field(Type cls, string fname)
    {
        //Console.Write("{0}, {1}, {2}", cls, fname, cls.GetField(fname, BINDING_ALL));
        return cls.GetField(fname, BINDING_ALL);
    }

    public static FieldInfo get_field(object cls, string fname)
    {
        return cls.GetType().GetField(fname, BINDING_ALL);
    }

    /* 基底クラスのフィールドを返す */
    public static FieldInfo get_baseclass_field(Type cls, string fname)
    {
        return cls.BaseType.GetField(fname, BINDING_ALL);
    }

    public static FieldInfo get_baseclass_field(object cls, string fname)
    {
        return get_baseclass_field(cls.GetType(), fname);
    }

    /* クラスが指定された名前のプロパティを持つかどうか検査する */
    public static bool has_property(object cls, string pname)
    {
        return cls.GetType().GetProperty(pname, BINDING_ALL) != null ? true : false;
    }

    /* クラスのメソッドを返す */
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

    /* クラスのstaticメソッドを実行する
     * 例:Util.invoke(type, function_name, new object[]{arg1, ...})
     */
    public static object invoke(Type tp, string fname, object[] args)
    {
        return get_method(tp, fname).Invoke(null, args);
    }

    /* クラスメソッドを実行する */
    public static object invoke(object cls, string fname, object[] args)
    {
        return get_method(cls, fname).Invoke(cls, args);
    }

    public static object invoke(object cls, string fname)
    {
        return invoke(cls, fname, new object[]{});
    }

    /* 指定された引数を持つクラスメソッドを実行する
    　* ポリモーフィズム対策
     * 例:Util.invoke(class_object, new Type[]{arg_type1, ...}, function_name, new object[]{arg1, ...})
    　*/
    public static object invoke(object cls, Type[] tps, string fname, object[] args)
    {
        return get_method(cls, tps, fname).Invoke(cls, args);
    }

    /* 基底クラスのメソッドを実行する
     * 例:Util.invoke(base_class_type, class_object, function_name, new object[]{arg1, ...})
    　*/
    public static object invoke(Type tp, object cls, string fname, object[] args)
    {
        return get_method(tp, fname).Invoke(cls, args);
    }

    /* クラスのメソッド一覧を出力 */
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

    /* クラスのフィールド一覧を出力 */
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

    /* クラスのメンバー一覧を出力 */
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

    /* クラスのプロパティ一覧を出力 */
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

    /* クラスのnested type一覧を出力 */
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

    /* クラスのインターフェース一覧を出力 */
    public static void print_interfaces(Type cls)
    {
        List<string> l = new List<string>();
        foreach(var m in cls.GetInterfaces())
            l.Add(m.ToString());
        l.Sort();
        l.Insert(0, "InterFaces:");
        Console.WriteLine(string.Join("\n\t", l));
    }

    /* メソッドとかいろいろ一通り出力 */
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

}
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

namespace LoYUtil
{

/* ゲームデータテーブルを上書きするためのテーブル作成用のメソッド集 */
public class TableBuilder
{
    /* MODリソースフォルダからpathパターン文字列に合致するJSONファイルを読み込んでインスタンス化する */
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
     *
     * このメソッドでは上のbuild_list/solist_by_jsonで作ったリストから
     * DataTable<T>型のデータテーブル(ItemDataTable等)を作成する
     * DataTable<T>.Defaultへのフックでゲーム本来のデータテーブルではなくここで作ったデータテーブルを返すことでゲーム上のデータを上書きするようにして使う
     */
    public static void build_table<TTable, T>(ref TTable db, List<T> l) where TTable: DataTable<T> where T: IDataRecord, IIdentifiable<int>, new()
    {
        //ScriptableObjectを作るためのお作法
        db =  (TTable)ScriptableObject.CreateInstance(typeof(TTable));
        TTable tbl = Database.Table.Get<TTable>();
        //T[] records = (T[])tbl.GetType().BaseType.GetField("records", Util.BINDING_ALL).GetValue(tbl);
        T[] records = (T[])Util.get_baseclass_value(tbl, "records");

        int n = records.Length;
        foreach(var v in l)
            n = v.GetId() >= n ? v.GetId() + 1 : n;

        T[] array = new T[n + 0];
        records.CopyTo(array, 0);
        //Console.Write("[__generic_table]{0}({1}): {2}({3}/{4})", db.GetType(), tbl.GetType(), n, array.Length, records.Length);

        //途中にnullがあるとDataTable<T>::EnumerateValidDataで落ちるので適当なデータで埋めておく
        if(n > records.Length)
            for(int i = records.Length; i < n; ++i)
                array[i] = records[0];

        foreach(var v in l)
            array[v.GetId()] = v;

        //TTableの基底クラスであるDataTable<T>のレコードを書き換える
        tbl.GetType().BaseType.GetField("records", Util.BINDING_ALL).SetValue(db, array);
    }
}

}
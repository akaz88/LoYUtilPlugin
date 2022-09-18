using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.Battle;
using Experience.Dungeons;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* ダンジョン関連のデータを追加する
 * [TODO]:出口/Exitが反映できない問題の修正
 */
class DungeonInjector
{
    static Dictionary<string, string> AssetTable = null;
    static List<SectorData> SectorDataList = null;
    static List<RandomEncounterData> RandomEncounterDataList = null;
    static List<DungeonData> DungeonDataList = null;
    static Dictionary<string, string> DngmapDict = null;
    //ゲーム内ではID:205まで定義
    static SectorDataTable ExSectorDataTable = null;
    //ゲーム内ではID:102まで定義
    static RandomEncounterDataTable ExRandomEncounterDataTable = null;
    //ゲーム内ではID:20まで定義
    static DungeonDataTable ExDungeonDataTable = null;
    static bool MapDataResourceTableDirty = false;
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1904;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "DungeonInjector", false,
                "アイテムを追加できるようにする"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][DungeonInjector]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][DungeonInjector]enable");
            LoYUtilPlugin.ev_load += load;
            LoYUtilPlugin.ev_load_later += load_later;

            LoYUtilPlugin.mgr.add_flag(FlagId, true);

            var org = Util.get_method(typeof(SectorDataTable), "get_Default");
            var hook = typeof(DungeonInjector).GetMethod("SectorDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(TableDatabase), "get_Sector");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(RandomEncounterDataTable), "get_Default");
            hook = typeof(DungeonInjector).GetMethod("RandomEncounterDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(DungeonDataTable), "get_Default");
            hook = typeof(DungeonInjector).GetMethod("DungeonDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(DungeonDataExtensions), "SetupSortedDungeonIds");
            hook = typeof(DungeonInjector).GetMethod("SetupSortedExDungeonIds");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(MapDataResourceTable), "get_Count");
            hook = typeof(DungeonInjector).GetMethod("ResetReference");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(MapDataResourceTable), "get_Item");
            hook = typeof(DungeonInjector).GetMethod("SetDirty");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(MapDataResourceTable), "SetupReference");
            hook = typeof(DungeonInjector).GetMethod("InsertReference");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(DungeonTableSet), "Initialize");
            hook = typeof(DungeonInjector).GetMethod("InsertAtInitialize");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(SectorData), "get_Name");
            hm.Patch(org, postfix: ResourceManager.extext);

            org = Util.get_method(typeof(DungeonData), "get_Name");
            hm.Patch(org, postfix: ResourceManager.extext);
        }
    }

    /* 改造したテーブルを返す */
    public static bool SectorDataTableDefault(ref SectorDataTable __result)
    {
        if(ExSectorDataTable == null)
            return true;
        __result = ExSectorDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool RandomEncounterDataTableDefault(ref RandomEncounterDataTable __result)
    {
        if(ExRandomEncounterDataTable == null)
            return true;
        __result = ExRandomEncounterDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool DungeonDataTableDefault(ref DungeonDataTable __result)
    {
        if(ExDungeonDataTable == null)
            return true;
        __result = ExDungeonDataTable;
        return false;
    }

    /* メニューの地図帳に追加ダンジョンを反映させる */
    public static bool SetupSortedExDungeonIds(ref DungeonId[] ___sortedDungeonIdArray)
    {
        if(___sortedDungeonIdArray != null)
            return false;
        DungeonDataTable tbl = DungeonDataTable.Default;
        ___sortedDungeonIdArray = new DungeonId[tbl.Length];
        for(int i = 0; i < tbl.Length; i++)
            ___sortedDungeonIdArray[i] = tbl[i].Id;
        return false;
    }

    /* マップデータのカウントを行う前にマップデータを更新させる */
    public static void ResetReference(MapDataResourceTable __instance)
    {
        if(MapDataResourceTableDirty)
            Util.invoke(__instance, "SetupReference");
    }

    /* マップアイテムを返す前にマップデータを更新させる */
    public static void SetDirty(string mapName, ref bool ___dirtyFlag)
    {
        //Console.Write("[SetDirty]{0}", mapName);
        if(MapDataResourceTableDirty)
            ___dirtyFlag = false;
    }

    /* マップデータテーブルに読み込んだデータを挿入する */
    public static void InsertReference(ref List<MapDataResource> ___resources, Dictionary<string, MapDataResource> ___references)
    {
        if(!MapDataResourceTableDirty || DngmapDict == null || DngmapDict.Count == 0)
            return;

        Dictionary<string, object> d = new Dictionary<string, object>();
        foreach(var e in ___resources)
            if(!d.ContainsKey(AssetTable[e.Assets.ToString()]))
                d[AssetTable[e.Assets.ToString()]] = e.Assets;

        //実質的なdngmap.jsonのインジェクション
        foreach(var p in DngmapDict)
        {
            MapDataResource data = create_map_data_resouce(p.Key, p.Value, d);
            if(data == null)
                continue;
            int i = ___resources.FindIndex(delegate(MapDataResource m){return m.MapName == data.MapName;});
            if(i != -1)
                ___resources[i] = data;
            else
                ___resources.Add(data);
        }
        DngmapDict.Clear();
        MapDataResourceTableDirty = false;
    }

    /* マップリソース初期化の際に各テーブルの生成と挿入を行う */
    public static void InsertAtInitialize(DungeonTableSet __instance, MapDataResourceTable resources, ref DungeonInfo[] ___dungeons)
    {
        if(!MapDataResourceTableDirty)
            return;
        load_later();
        Util.invoke(resources, "SetupReference");
        int max = 0;
        foreach(IGrouping<DungeonId, SectorData> grouping in from x in Database.Table.Sector group x by x.DungeonId)
            max = (int)grouping.Key > max ? (int)grouping.Key : max;
        ___dungeons = new DungeonInfo[max + 1];

        //DungeonTableSet.Dungeonsをセットし直さないとラジオが受信できない
        var tp = Assembly.GetAssembly(typeof(DungeonTableSet)).GetType("Experience.Dungeons.DungeonTableSet+DungeonTable");
        var cls = Activator.CreateInstance(tp, Util.BINDING_ALL, null, null, null);
        Util.invoke(cls, "set_Owner", new object[]{__instance});
        Util.invoke(cls, "set_Values", new object[]{___dungeons});
        Util.invoke(__instance, "set_Dungeons", new object[]{cls});
    }

    public static void load()
    {
        init_table();
        //Console.Write("[DungeonInjector][load]");
        TableBuilder.build_list_by_json(ref SectorDataList, "*.SectorData.json");
        TableBuilder.build_list_by_json(ref RandomEncounterDataList, "*.RandomEncounterData.json");
        TableBuilder.build_list_by_json(ref DungeonDataList, "*.DungeonData.json");
        //dngmapファイルはファイルの中身だけロードしといて後でインスタンス化する
        load_dngmaps();
        MapDataResourceTableDirty = true;
    }

    public static void load_later()
    {
        TableBuilder.build_table(ref ExSectorDataTable, SectorDataList);
        //ExSectorDataTable = Database.Table.Get<SectorDataTable>();
        TableBuilder.build_table(ref ExRandomEncounterDataTable, RandomEncounterDataList);
        TableBuilder.build_table(ref ExDungeonDataTable, DungeonDataList);
    }

    /* .dngmap.jsonファイルをロード
     * ロードしたJSONはInsertReferenceでcreate_map_data_resouceによりインスタンス化されるため、ここではファイルを読むだけ
     */
    public static void load_dngmaps()
    {
        if(DngmapDict == null)
            DngmapDict = new Dictionary<string, string>();
        else
            DngmapDict.Clear();
        foreach(var f in Directory.GetFiles(LoYUtilPlugin.rsrc_path, "*.dngmap.json", SearchOption.AllDirectories))
        {
            Console.Write($"[load_dngmaps]{f}");
            DngmapDict[Path.GetFileName(f)] = File.ReadAllText(f);
        }
    }

    /* InsertReferenceから呼ばれて、load()で読み込んでおいたdngmapをインスタンス化
     * アセットバンドルからのロードは難しいため、既にロードしてある既定のマップのリソースから拝借する
     * MapDataResource.assetPackageにはオブジェクトや床設定が個別に割り当て可能だが、
     * 実際はモデルアセットが全てに優先されるため、設定に意味はなかった
     */
    public static MapDataResource create_map_data_resouce(string filename, string buf, Dictionary<string, object> asset_dict)
    {
        char[] trim = {'"', ' ', '\r', '\n', ',', '\t'};

        MapDataResource data = MapDataResource.CreateDummy();
        JsonUtility.FromJsonOverwrite(buf, data);
        data.name = filename;
        Util.invoke(data, "OnEnable");

        //assetPackage内に記述されたアセットパッケージを読んで既存のアセットパッケージから適切なものを使用する
        int idx = buf.IndexOf("assetPackage");
        idx = buf.IndexOf("{", idx) + 1;
        string ap = buf.Substring(idx, buf.IndexOf("}", idx) - idx);
        foreach(var ln in ap.Split('\n'))
        {
            string[] p = ln.Split(':');
            if(p.Length != 2)
                continue;
            string key = p[0].Trim(trim);
            string val = p[1].Trim(trim);
            if(key == "m_FileID" || key == "m_PathID")
                continue;
            //不正なアセット名 or キーワード
            if(!asset_dict.ContainsKey(val) || key != "package")
            {
                Console.Write("[create_map_data_resouce]Error: {0}", filename);
                Console.Write("[create_map_data_resouce]{0} is not valid asset or keyword({0}:{1}).", key, val);
                return null;
            }
            data.Assets = (DungeonAssetPackage)asset_dict[val];
            break;
        }
        if(data.Assets == null)
        {
            Console.Write("[create_map_data_resouce]Error: {0}", filename);
            Console.Write("[create_map_data_resouce]cannnot find valid asset package setting.");
            return null;
        }

        //マップオブジェクトのSettingに指定されたアセットパッケージから適切なオブジェクトを入れる
        foreach(var e in data.MapObjectEntries)
        {
            string objname = e.Name.Split('_')[0];
            var mo = data.Assets.MapObjectAsset;
            for(int i = 0; i < mo.Count; ++i)
            {
                if(String.Compare(mo[i].name, objname, true) == 0)
                {
                    e.Setting = mo[i];
                    break;
                }
                if(i == mo.Count - 1)
                {
                    Console.Write("[create_map_data_resouce]Error: {0}", filename);
                    Console.Write("[create_map_data_resouce]Error: object {0}({1}) did not found in {2}.", objname, e.Name, mo.name);
                    return null;
                }
            }
        }
        //dump_data(data);
        return check_data(data);
    }

    /* MapDataResourceの情報を適当にダンプ */
    public static void dump_data(MapDataResource data)
    {
        Console.Write("[dump_data]{0}", data);
        Console.Write("[dump_data]MapName: {0}", data.MapName);
        Console.Write("[dump_data]Size: {0}x{1}", data.Width, data.Height);
        Console.Write("[dump_data]Asset");
        Console.Write("[dump_data]\tTile: {0}", data.TileAsset);
        Console.Write("[dump_data]\tMapObject: {0}", data.MapObjectAsset);
        Console.Write("[dump_data]\tModelAssetReference: {0}", data.Assets.ModelAsset);
        Console.Write("[dump_data]Blocks counts: {0}", data.Blocks.ToArray().Length);
        Console.Write("[dump_data]MapObjectEntries");
        foreach(var e in data.MapObjectEntries)
            Console.Write("[dump_data]\t{0}({1},{2}): {3}/(facing:{4})", e.Name, e.Point.X, e.Point.Y, e.Type, e.Facing);
    }

    /* MapDataResourceの簡易検査 */
    public static MapDataResource check_data(MapDataResource data)
    {
        if(data == null)
        {
            Console.Write("[check_data]Error: resource is null");
            return null;
        }
        if(!data.IsAssetValid)
        {
            Console.Write("[check_data]Error: IsAssetValid == false");
            return null;
        }
        int bclen = data.Blocks.ToArray().Length;
        if(data.Width * data.Height != bclen)
        {
            Console.Write("[check_data]Error: Width({0}) * Height({1}) != Blocks.Length({2})", data.Width, data.Height, bclen);
            return null;
        }
        foreach(var b in data.Blocks)
        {
            if(b == null)
            {
                Console.Write("[check_data]Error: Blocks contains null");
                return null;
            }
        }
        var bm = (MapArray<MapBlockData>)Util.get_value(data, "blockMap");
        int bmlen = bm.Array.Length;
        if(bm.Width * bm.Height != bmlen)
        {
            Console.Write("[check_data]Error: blockMap.Width({0}) * blockMap.Height({1}) != blockMap.Length({2})", bm.Width, bm.Height, bmlen);
            return null;
        }
        if(bclen != bmlen)
        {
            Console.Write("[check_data]Error: Blocks.Length({0}) != blockMap.Length({1})", bclen, bmlen);
            return null;
        }
        Point x = Point.Zero;
        for(int h = 0; h < data.Height; ++h)
        {
            x.Y = h;
            for(int w = 0; w < data.Width; ++w)
            {
                x.X = w;
                if(data[x] == null)
                {
                    Console.Write("[check_data]Error: blockMap({0}, {1}) == null", x.X, x.Y);
                    return null;
                }
            }
        }
        MapObjectEntry[] entries = (MapObjectEntry[])data.MapObjectEntries;
        for(int i = 0; i < entries.Length ; ++i)
        {
            MapObjectEntry e = entries[i];
            if(e == null)
            {
                Console.Write("[check_data]Error: MapObjectEntries[{0}] == null", i);
                return null;
            }
            if(e.Setting == null)
            {
                Console.Write("[check_data]Error: MapObjectEntries[{0}].Setting == null", i);
                return null;
            }
            if(e.Definition == null)
            {
                Console.Write("[check_data]Error: MapObjectEntries[{0}].Definition == null", i);
                return null;
            }
            if(e.Components.Length != e.Definition.Components.Length)
            {
                Console.Write("[check_data]Error: MapObjectEntries[{0}].Components.Length({1}) != Definition.Components.Length({2})", i, e.Components.Length, e.Definition.Components.Length);
                return null;
            }
            for(int j = 0; j < e.Components.Length; ++j)
            {
                MapObjectComponent c = e.Components[j];
                if(c == null)
                {
                    Console.Write("[check_data]Error: MapObjectEntries[{0}].Components[{1}] == null", i, j);
                    return null;
                }
                if(c.Definition == null)
                {
                    Console.Write("[check_data]Error: MapObjectEntries[{0}].Components[{1}].Definition == null", i, j);
                    return null;
                }
                if(c.Definition.Type != e.Definition.Components[j].Type)
                {
                    Console.Write("[check_data]Error: MapObjectEntries[{0}].Components[{1}].Definition.Type({2}) != MapObjectEntries[{0}].Definition.Components[{1}].Type({3})", i, j, c.Definition.Type, e.Definition.Components[j].Type);
                    return null;
                }
            }
        }

        return data;
    }

    /* 既定のアセットを変換するためのテーブルを準備する */
    public static void init_table()
    {
        AssetTable = new Dictionary<string, string>()
        {
            {"Castle_01_Package (Experience.Dungeons.DungeonAssetPackage)", "Castle_01_Package"},
            {"Castle_02_Package (Experience.Dungeons.DungeonAssetPackage)", "Castle_02_Package"},
            {"Castle_03_Package (Experience.Dungeons.DungeonAssetPackage)", "Castle_03_Package"},
            {"Castle_04_Package (Experience.Dungeons.DungeonAssetPackage)", "Castle_04_Package"},
            {"Castle_05_Package (Experience.Dungeons.DungeonAssetPackage)", "Castle_05_Package"},
            {"Castle_06_Package (Experience.Dungeons.DungeonAssetPackage)", "Castle_06_Package"},
            {"Forest_01_Package (Experience.Dungeons.DungeonAssetPackage)", "Forest_01_Package"},
            {"Forest_02_Package (Experience.Dungeons.DungeonAssetPackage)", "Forest_02_Package"},
            {"Forest_03_Package (Experience.Dungeons.DungeonAssetPackage)", "Forest_03_Package"},
            {"Forest_04_Package (Experience.Dungeons.DungeonAssetPackage)", "Forest_04_Package"},
            {"Forest_05_Package (Experience.Dungeons.DungeonAssetPackage)", "Forest_05_Package"},
            {"Forest_06_Package (Experience.Dungeons.DungeonAssetPackage)", "Forest_06_Package"},
            {"Shrine_01_Package (Experience.Dungeons.DungeonAssetPackage)", "Shrine_01_Package"},
            {"Shrine_04_Package (Experience.Dungeons.DungeonAssetPackage)", "Shrine_04_Package"},
            {"Tunnel_01_Package (Experience.Dungeons.DungeonAssetPackage)", "Tunnel_01_Package"},
            {"Tunnel_05_Package (Experience.Dungeons.DungeonAssetPackage)", "Tunnel_05_Package"},
            {"[a16875e3186fad241aec43654f401c8a]", "CastleModel_01"},
            {"[be1594cf5c8967e478c257469f61dfc8]", "CastleModel_02"},
            {"[65f0fe75ccf98e4439d6e84c1c9853c4]", "CastleModel_03"},
            {"[c0916c2c4d4c742429a7ff41cd8c9aa9]", "CastleModel_04"},
            {"[e6152a9ef883f1d41bc352a1715166b9]", "CastleModel_05"},
            {"[33ad12a24657cb3479076b38dea65551]", "CastleModel_06"},
            {"[196a33fda5258154f84a71b9e18e383f]", "ForestModel_01"},
            {"[fad79e7962651904da711c4f9c2b5c10]", "ForestModel_02"},
            {"[d63a3a63ca3ad244dab94203830e2735]", "ForestModel_03"},
            {"[5b76390e4971c9540bfa970525838d43]", "ForestModel_04"},
            {"[9571067dbe3f48948962ad0d2cc137a4]", "ForestModel_05"},
            {"[d500c4d2ce2353a46be9c6ebc5415186]", "ForestModel_06"},
            {"[e96375aaf0c49b34aa5df5912394cd82]", "ShrineModel_01"},
            {"[32117d4e3a2264c43b4bcbb50be438d2]", "ShrineModel_04"},
            {"[d8af45e35edaa9042826d6618a6a4e0b]", "TunnelModel_01"},
            {"[7b8acd52fb5d2d3428c31f40ef62f96c]", "TunnelModel_05"},
            {"CastleTiles (Experience.Dungeons.DungeonTileAsset)", "CastleTiles"},
            {"ForestTiles (Experience.Dungeons.DungeonTileAsset)", "ForestTiles"},
            {"ShrineTiles (Experience.Dungeons.DungeonTileAsset)", "ShrineTiles"},
            {"TunnelTiles (Experience.Dungeons.DungeonTileAsset)", "TunnelTiles"},
            {"CastleObjects (Experience.Dungeons.MapObjectAsset)", "CastleObjects"},
            {"ForestObjects (Experience.Dungeons.MapObjectAsset)", "ForestObjects"},
            {"ShrineObjects (Experience.Dungeons.MapObjectAsset)", "ShrineObjects"},
            {"TunnelObjects (Experience.Dungeons.MapObjectAsset)", "TunnelObjects"}
        };
    }
}

}